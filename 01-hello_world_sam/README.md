# Hello World AWS SAM

A minimal AWS Serverless Application Model (SAM) application that demonstrates a basic Lambda function exposed as an HTTP API endpoint.

## Description

This project implements a simple "Hello World" API using AWS Lambda and API Gateway. The Lambda function responds to HTTP GET requests with a plain text "Hello World!" message.

## Architecture

The application consists of a single Lambda function that handles HTTP requests through API Gateway:

- **Lambda Function**: Python 3.13 runtime with a handler function that returns a simple HTTP response
- **API Gateway**: REST API that routes GET requests to the Lambda function
- **SAM Template**: CloudFormation template that defines the infrastructure as code

The Lambda function receives API Gateway events and returns responses in the format expected by API Gateway, including status code, headers, and response body.

## Project Structure

```
01-hello_world_sam/
├── src/
│   ├── __init__.py
│   └── app.py              # Lambda function handler
├── template.yaml           # SAM/CloudFormation template
└── README.md
```


## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.13 (for local testing)

## Building and Deployment

### Build the application

```bash
sam build
```

### Deploy to AWS

```bash
sam deploy --guided
```

The guided deployment will prompt for configuration values. For subsequent deployments, use:

```bash
sam deploy
```

### Verify deployment

After deployment, SAM will output the API Gateway URL. The endpoint will be available at:

```
https://{api-id}.execute-api.{region}.amazonaws.com/Prod/hello
```

## Testing

### Test locally

```bash
sam local start-api -p 3001
```

Then invoke the endpoint locally

```bash
curl http://localhost:3001/hello
```


### Test deployed endpoint

```bash
curl https://{api-id}.execute-api.{region}.amazonaws.com/Prod/hello
```

Expected response:
```
Hello World!
```

## Cleanup

To remove all deployed resources:

```bash
sam delete
```

## Configuration

The `samconfig.toml` file contains deployment configuration including stack name, region, and other AWS-specific settings. Modify this file to customize deployment parameters. 