# AWS Mini-Projects

This repository contains a collection of small, serverless projects built using AWS Serverless Application Model (SAM). Each project demonstrates a different aspect of building serverless applications on AWS, from simple API endpoints to more complex image processing and data management solutions.

## Projects

### [01-hello_world_sam](./01-hello_world_sam/)

A minimal AWS Serverless Application Model (SAM) application that demonstrates a basic Lambda function exposed as an HTTP API endpoint. This project implements a simple "Hello World" API using AWS Lambda and API Gateway, where the Lambda function responds to HTTP GET requests with a plain text "Hello World!" message.

### [02-serverless-counter](./02-serverless-counter/)

A serverless application that manages a counter using AWS Lambda and DynamoDB. The application provides REST API endpoints for incrementing, resetting, and retrieving a counter value. It leverages AWS Lambda for serverless compute, DynamoDB for state storage, and API Gateway for HTTP API endpoints.

### [03-encode-string](./03-encode-string/)

A serverless AWS Lambda function that converts text messages into pixelated square matrix representations. The service encodes text as binary data, arranges it in a square grid format, and generates a PNG image output. It uses a Docker container for deployment and integrates with HTTP API Gateway.

### [04-most-used-colors](./04-most-used-colors/)

A sophisticated serverless API that analyzes uploaded images and intelligently extracts the five most dominant colors using advanced machine learning techniques (K-means++ clustering). This project demonstrates how to build a production-ready image processing service on AWS Lambda with containerized deployment, handling image validation, processing, and returning dominant colors in JSON format. 