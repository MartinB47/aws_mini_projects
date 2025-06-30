import base64, json
from src.encode import encode_message_to_matrix, plot_image


def respond_png(img_bytes: bytes):
    """Return a PNG image as base64-encoded response for AWS Lambda.

    Args:
        img_bytes (bytes): The PNG image bytes to encode and return

    Returns:
        dict: AWS Lambda response with base64-encoded PNG image
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/png"},
        "isBase64Encoded": True,
        "body": base64.b64encode(img_bytes).decode(),
    }


def lambda_handler(event, _):
    """AWS Lambda handler that converts text message to QR-like matrix image."""
    # Read text payload
    body = event.get("body", "")
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode()

    # Parse and validate JSON payload from request body
    # The payload must contain a "message" field with the text to encode
    try:
        parsed_body = json.loads(body)
        message = parsed_body.get("message", "")
        if not message:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing 'message' field in JSON payload"}
                ),
            }
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Invalid JSON payload. Expected JSON with 'message' field"}
            ),
        }

    # Encode the validated message into a binary matrix representation
    matrix = encode_message_to_matrix(message)

    # Convert matrix to PNG bytes
    png_buffer = plot_image(matrix)
    img_bytes = png_buffer.getvalue()

    # Return the image as base64 in the response
    return respond_png(img_bytes)
