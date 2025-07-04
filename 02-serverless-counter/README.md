# Serverless Counter Application

A serverless application that manages a counter using AWS Lambda and DynamoDB. The application provides REST API endpoints for incrementing, resetting, and retrieving a counter value.

## Architecture

- **AWS Lambda**: Python 3.13 runtime for serverless compute
- **DynamoDB**: NoSQL database for storing counter state
- **API Gateway**: HTTP API for REST endpoints
- **SAM**: Serverless Application Model for infrastructure as code

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/counter` | Retrieve current counter value |
| POST | `/counter/increment` | Increment counter by 1 |
| POST | `/counter/reset` | Reset counter to 0 |

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.13

## Deployment

### Initial Deployment

```bash
sam build
sam deploy --guided
```

Follow the interactive prompts to configure:
- Stack name: `serverless-counter`
- AWS Region: `us-east-1`
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Disable rollback: `N`
- Authentication: `y` (for no authentication)
- Save arguments to configuration file: `Y`

### Subsequent Deployments

```bash
sam build && sam deploy
```

## Testing

### Get Counter Value

```bash
curl -X GET https://{api-id}.execute-api.{region}.amazonaws.com/counter
```

### Increment Counter

```bash
curl -X POST https://{api-id}.execute-api.{region}.amazonaws.com/counter/increment
```

### Reset Counter

```bash
curl -X POST https://{api-id}.execute-api.{region}.amazonaws.com/counter/reset
```

Replace `{api-id}` and `{region}` with the actual values from your deployment outputs.

## Response Format

All endpoints return JSON responses:

```json
{
  "count": 3
}
```

## Project Structure

```
02-serverless-counter/
├── src/
│   └── app.py              # Lambda function implementation
├── template.yaml           # SAM template
└── README.md              # This file
```

## Infrastructure

The application creates the following AWS resources:

- **DynamoDB Table**: Stores counter data with `id` as the primary key
- **Lambda Function**: Processes API requests and manages counter operations
- **API Gateway**: HTTP API with three routes
- **IAM Role**: Permissions for Lambda to access DynamoDB

## Cleanup

To remove all deployed resources:

```bash
sam delete
```