import json
import base64
import io
import re
from typing import List, Dict, Any
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# Set seeds for reproducibility
RANDOM_SEED = 47
np.random.seed(RANDOM_SEED)


def validate_base64_image(base64_string: str) -> bool:
    """Validate base64 encoded image string."""
    try:
        # Check if it's a valid base64 string
        if not re.match(r"^[A-Za-z0-9+/]*={0,2}$", base64_string):
            return False

        # Try to decode
        image_data = base64.b64decode(base64_string)

        # Try to open as image
        image = Image.open(io.BytesIO(image_data))
        image.verify()  # Verify it's a valid image

        return True
    except Exception:
        return False


def extract_colors_from_image(image_data: bytes) -> List[List[int]]:
    """Extract top 5 dominant colors using K-means++ clustering."""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert to numpy array
        pixels = np.array(image)

        # Reshape to 2D array where each row is a pixel (R,G,B)
        pixels_2d = pixels.reshape(-1, 3)

        # Apply K-means++ clustering
        kmeans = KMeans(
            n_clusters=5, init="k-means++", random_state=RANDOM_SEED, n_init=10
        )
        kmeans.fit(pixels_2d)

        # Get centroids (dominant colors)
        centroids = kmeans.cluster_centers_

        # Convert to integers and ensure valid RGB range
        dominant_colors = []
        for centroid in centroids:
            color = [int(max(0, min(255, c))) for c in centroid]
            dominant_colors.append(color)

        return dominant_colors

    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for color analysis API.

    Expected input:
    {
        "body": "base64_encoded_image_string"
    }

    Returns:
    {
        "statusCode": 200,
        "body": {
            "colors": [
                [255, 0, 0],   # RGB values
                [0, 255, 0],
                ...
            ]
        }
    }
    """
    try:
        # Parse request body
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing image data in request body"}),
            }

        base64_image = event["body"]

        # Input sanitization
        if not isinstance(base64_image, str):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Image data must be a string"}),
            }

        # Remove potential data URL prefix
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        # Validate base64 image
        if not validate_base64_image(base64_image):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid or corrupted image data"}),
            }

        # Decode base64 image
        try:
            image_data = base64.b64decode(base64_image)
        except Exception:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Failed to decode base64 image data"}),
            }

        # Extract dominant colors
        dominant_colors = extract_colors_from_image(image_data)

        # Return results
        return {"statusCode": 200, "body": json.dumps({"colors": dominant_colors})}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal server error: {str(e)}"}),
        }
