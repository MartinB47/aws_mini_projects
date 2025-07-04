# String Encoding Service

A serverless AWS Lambda function that converts text messages into pixelated square matrix representations. The service encodes text as binary data and arranges it in a square grid format, generating a PNG image output.

## Overview

This project implements a text-to-matrix encoding algorithm that:
- Converts text input to binary representation
- Arranges binary bits in a square matrix format
- Generates a visual PNG image with grid lines
- Returns the image as a base64-encoded response

## Architecture

- **AWS Lambda**: Serverless compute function
- **HTTP API Gateway**: RESTful API endpoint
- **Docker Container**: Containerized deployment

## Prerequisites

- AWS CLI configured with appropriate permissions
- AWS SAM CLI installed
- Docker installed and running

## Deployment

### Build the Application

```bash
sam build
```

### Deploy to AWS

```bash
sam deploy --guided
```

Follow the interactive prompts to configure your deployment settings. The deployment will create:
- Lambda function with container image
- HTTP API Gateway
- Required IAM roles and permissions

## Usage

### API Endpoint

The service exposes a single endpoint:
- **URL**: `https://{api-id}.execute-api.{region}.amazonaws.com/generate`
- **Method**: POST
- **Content-Type**: application/json

### Request Format

```json
{
  "message": "Your text message here"
}
```

### Response

The API returns a PNG image with:
- **Content-Type**: image/png
- **Body**: Base64-encoded PNG image data
- **Status Code**: 200 for success, 400 for errors

### Example Invocation

```bash
curl -X POST \
  https://{api-id}.execute-api.{region}.amazonaws.com/generate \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}' \
  --output encoded_message.png
```

## Error Handling

The service returns appropriate HTTP status codes:
- **200**: Successful encoding and image generation
- **400**: Invalid JSON payload or missing message field

Error responses include descriptive error messages in JSON format.

## Project Structure

```
03-encode-string/
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── template.yaml          # SAM template
└── src/
    ├── __init__.py
    ├── app.py             # Lambda handler
    └── encode.py          # Encoding logic
```

## Dependencies

- **numpy**: Numerical computing and array operations
- **matplotlib**: Image generation and plotting
- **AWS Lambda Runtime**: Python 3.12 base image

## Cleanup

To remove the deployed resources:

```bash
sam delete
```