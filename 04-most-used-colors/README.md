# Most Used Colors - AWS Lambda API

A serverless API that analyzes images and returns the top 5 most dominant colors using K-means++ clustering.

## Features

- **Serverless**: AWS Lambda with API Gateway
- **Containerized**: Docker container with numpy, PIL, and scikit-learn
- **Reproducible**: Fixed random seeds for consistent results
- **Base64 Upload**: Accepts images via base64 encoding
- **K-means++**: Uses K-means++ clustering for accurate color extraction
- **Input Validation**: Comprehensive validation and sanitization
- **CORS Enabled**: Cross-origin requests supported

## Architecture

- **Lambda Function**: Python with container image
- **API Gateway**: REST API with POST endpoint
- **Container**: Docker image with all dependencies
- **Timeout**: 10 seconds
- **Memory**: 1024 MB

## Dependencies

- `numpy` - Numerical computing
- `Pillow` - Image processing
- `scikit-learn` - K-means++ clustering

## Deployment

### Prerequisites

1. AWS CLI configured
2. SAM CLI installed
3. Docker installed and running

### Deploy to AWS

```bash
# Build and deploy
sam build
sam deploy --guided

# For subsequent deployments
sam build
sam deploy
```

The deployment will:
1. Build the Docker container
2. Push to ECR automatically
3. Deploy Lambda function
4. Create API Gateway endpoint

## API Usage

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
    [255, 0, 0],    // RGB values
    [0, 255, 0],
    [0, 0, 255],
    [128, 128, 128],
    [255, 255, 255]
  ]
}
```

### Example with curl

```bash
# Convert image to base64
base64_image=$(base64 -i your_image.jpg)

# Send request
curl -X POST \
  https://your-api-gateway-url/prod/analyze-colors \
  -H "Content-Type: application/json" \
  -d "{\"body\": \"$base64_image\"}"
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Generate test images
python tests/create_test_images.py

# Step 2: Test with sample images
sam local invoke ColorAnalysisFunction -e tests/events/rgb_stripes_event.json
sam local invoke ColorAnalysisFunction -e tests/events/gradient_event.json
sam local invoke ColorAnalysisFunction -e tests/events/solid_colors_event.json
```

## Algorithm Details

1. **Image Processing**: Converts image to RGB format
2. **Pixel Extraction**: Reshapes image to 2D array of RGB values
3. **K-means++ Clustering**: Groups similar colors into 5 clusters
4. **Centroid Extraction**: Returns the 5 cluster centroids as dominant colors
5. **Color Normalization**: Ensures RGB values are in valid range (0-255)

## Error Handling

- **400 Bad Request**: Invalid image data or format
- **500 Internal Server Error**: Processing errors

## Security Features

- Input sanitization
- Base64 validation
- Image format verification
- CORS headers for web access

## Performance Considerations

- **Memory**: 1024 MB allocated for image processing
- **Timeout**: 10 seconds maximum execution time
- **No Resizing**: Processes original image size
- **Efficient Clustering**: K-means++ with 10 initializations

## Monitoring

- CloudWatch Logs for function execution
- API Gateway metrics for request monitoring
- Lambda metrics for performance tracking 