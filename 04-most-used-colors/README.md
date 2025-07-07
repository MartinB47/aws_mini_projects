# Most Used Colors - AWS Lambda API

A sophisticated serverless API that analyzes uploaded images and intelligently extracts the five most dominant colors using advanced machine learning techniques. This project demonstrates how to build a production-ready image processing service on AWS Lambda with containerized deployment.

## Overview

This API transforms the complex task of color analysis into a simple, scalable web service. When you upload an image, the system processes it through a carefully tuned K-means++ clustering algorithm to identify the most representative colors in the image. The result is a clean JSON response containing the top five dominant colors in RGB format, ready for use in design applications, data visualization, or any project requiring color palette extraction.

The service is built entirely on AWS serverless infrastructure, meaning it automatically scales to handle any number of requests without requiring server management. The containerized approach ensures consistent performance across different environments and makes deployment straightforward.

## How It Works

The color analysis process begins when an image is uploaded as a base64-encoded string. The system first validates the input to ensure it contains valid image data, then decodes and processes the image using the Pillow library for robust image handling.

Once the image is loaded, it's converted to RGB format to ensure consistent color space processing. The system then extracts every pixel's RGB values and reshapes them into a two-dimensional array suitable for machine learning algorithms.

The core of the analysis uses K-means++ clustering, an advanced variant of the traditional K-means algorithm that provides more reliable and consistent results. This algorithm groups similar colors together by finding five optimal cluster centers that best represent the color distribution in the image. The K-means++ initialization method ensures the algorithm starts with well-distributed initial points, leading to better final results.

After clustering, the system extracts the centroid (average color) of each cluster, which represents the dominant color for that group. These centroids are then normalized to ensure all RGB values fall within the valid 0-255 range, and returned as the final result.

## Technical Architecture

The application leverages AWS Lambda for serverless compute, eliminating the need for traditional server infrastructure. The Lambda function runs inside a custom Docker container that includes all necessary dependencies, ensuring consistent behavior across different environments.

API Gateway provides the HTTP interface, handling request routing, authentication, and response formatting. The containerized approach allows us to include complex dependencies like NumPy for numerical computing, Pillow for image processing, and scikit-learn for the clustering algorithm without hitting Lambda's deployment package size limits.

The system allocates 1024 MB of memory to handle image processing efficiently, with a 60-second timeout to accommodate larger images. The fixed random seed ensures reproducible results, making the API suitable for applications requiring consistent color analysis.

## Key Features

The API provides comprehensive input validation to handle various edge cases gracefully. It accepts images in multiple formats including JPEG, PNG, and other common image types supported by Pillow. The base64 encoding requirement ensures reliable data transmission while maintaining compatibility with web applications.

The K-means++ algorithm offers superior performance compared to standard K-means clustering, particularly for color analysis tasks. The algorithm automatically handles images with varying color distributions, from monochromatic images to complex multi-colored photographs.

The containerized deployment approach provides several advantages. It ensures all dependencies are properly isolated and versioned, eliminates "works on my machine" issues, and allows for easy scaling and deployment across different AWS regions.

## Dependencies

The application relies on NumPy for efficient numerical operations and array manipulation, which is essential for processing large images quickly. Pillow handles all image format conversions and provides robust image loading capabilities. Scikit-learn implements the K-means++ clustering algorithm with optimized performance for large datasets.

## Getting Started

### Prerequisites

Before deploying the application, ensure you have the AWS CLI properly configured with appropriate credentials and permissions. The SAM CLI must be installed for building and deploying the Lambda function. Docker is required for containerized deployment and should be running on your system.

### Local Development and Testing

To test the application locally, first install the required dependencies using pip and the provided requirements file. The testing framework includes a script that generates various test images with known color distributions, allowing you to verify the algorithm's accuracy.

The local testing process involves generating test images with specific color patterns, invoking the Lambda function locally using SAM CLI, and visualizing the results using the included color visualization script. This comprehensive testing approach ensures the API works correctly before deployment.

```bash
# Build
sam build

# Install dependencies
pip install -r requirements.txt

# Generate test images
python tests/create_test_images.py

# Test with sample images
sam local invoke ColorAnalysisFunction -e tests/events/rgb_stripes_event.json

# Test with your own image
echo "{\"body\":\"$(base64 -i your_image.jpeg)\"}" \
  | sam local invoke ColorAnalysisFunction -e -
```

### Deployment Process

Deployment requires AWS CLI configuration, SAM CLI installation, and a running Docker daemon. The SAM build process creates a Docker container with all dependencies, pushes it to Amazon ECR, and deploys the Lambda function with the appropriate configuration.

The guided deployment process automatically creates the necessary AWS resources including the Lambda function, API Gateway, and IAM roles. Subsequent deployments can be performed with simple build and deploy commands, making the development cycle efficient.

```bash
# Build and deploy
sam build
sam deploy --guided
```

The deployment process will build the Docker container, push it to ECR automatically, deploy the Lambda function, and create the API Gateway endpoint with the appropriate configuration.

## API Integration

The API exposes a single POST endpoint that accepts JSON requests containing base64-encoded image data. The response format provides an array of RGB color values representing the five most dominant colors in the uploaded image.

Integration is straightforward using standard HTTP clients. The curl example demonstrates how to encode an image, send it to the API, and save the response for further processing. The included visualization script can then display the extracted colors as a color palette for immediate visual feedback.

### Endpoint

```
POST /analyze-colors
```

### Request Format

```json
{
  "body": "base64_encoded_image_string"
}
```

### Response Format

```json
{
  "colors": [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [128, 128, 128],
    [255, 255, 255]
  ]
}
```

### Example Usage

```bash
curl -X POST \
  https://{api-id}.execute-api.{region}.amazonaws.com/prod/analyze-colors \
  -H "Content-Type: application/json" \
  -d "{\"body\": \"$(base64 -i your_image.jpeg)\"}" \
  -o colors_result.json

# Visualize the colors
python visualize_colors.py colors_result.json
```

### How to Find Your API Endpoint

If you have lost or forgotten your deployed API Gateway endpoint URL, you can retrieve it using the AWS CLI with the following command:

```bash
aws cloudformation describe-stacks --stack-name most-used-colors --query "Stacks[0].Outputs" --output table
```

Look for the output value corresponding to your API endpoint in the results.

## Algorithm Implementation Details

The color extraction process follows a carefully designed pipeline that ensures both accuracy and performance. Image processing begins with format conversion to ensure consistent color space handling, followed by pixel extraction that preserves the original image's color information.

The K-means++ clustering algorithm operates on the extracted pixel data, using ten different initializations to find the optimal clustering solution. This multi-initialization approach significantly improves the quality of results compared to single-run clustering.

Centroid extraction provides the final color values by calculating the mean RGB values within each cluster. Color normalization ensures all output values are valid RGB integers, making the results immediately usable in web applications and design tools.

## Use Cases and Applications

This API serves various applications including design automation, where it can extract brand colors from logos or product images. Data visualization projects can use it to generate color schemes from relevant imagery, while e-commerce platforms might analyze product photos to suggest complementary colors.

The serverless architecture makes it particularly suitable for applications with variable load patterns, as it automatically scales to handle traffic spikes without additional configuration. The containerized approach also makes it easy to deploy in different environments or integrate into larger microservice architectures.