# API Gateway REST API
# HTTP interface for the translation service

# Main API Gateway REST API resource
resource "aws_api_gateway_rest_api" "translation_api" {
  name        = "${local.name_prefix}-api"
  description = "REST API for text translation service using AWS Bedrock"

  # API configuration
  endpoint_configuration {
    types = ["REGIONAL"]
  }

  # Enable request validation
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "execute-api:Invoke"
        Resource  = "*"
      }
    ]
  })

  tags = merge(local.common_tags, {
    Name        = "${local.name_prefix}-api"
    Description = "API Gateway for translation service"
  })
}

# API Gateway resource for translation endpoint
resource "aws_api_gateway_resource" "translate_resource" {
  rest_api_id = aws_api_gateway_rest_api.translation_api.id
  parent_id   = aws_api_gateway_rest_api.translation_api.root_resource_id
  path_part   = "translate"
}

# POST method for translation requests
resource "aws_api_gateway_method" "translate_post" {
  rest_api_id   = aws_api_gateway_rest_api.translation_api.id
  resource_id   = aws_api_gateway_resource.translate_resource.id
  http_method   = "POST"
  authorization = "NONE"

  # Request parameters
  request_parameters = {
    "method.request.header.Content-Type" = true
  }
}

# Integration between API Gateway and Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.translation_api.id
  resource_id = aws_api_gateway_resource.translate_resource.id
  http_method = aws_api_gateway_method.translate_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.translator.invoke_arn
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_method.translate_post,
    aws_api_gateway_integration.lambda_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.translation_api.id

  # Force new deployment on configuration changes
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.translate_resource.id,
      aws_api_gateway_method.translate_post.id,
      aws_api_gateway_integration.lambda_integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway stage
resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.translation_api.id
  stage_name    = var.api_gateway_stage_name

  # Enable logging and monitoring
  xray_tracing_enabled = true

  tags = merge(local.common_tags, {
    Name        = "${local.name_prefix}-api-stage-${var.api_gateway_stage_name}"
    Description = "API Gateway stage for ${var.environment} environment"
  })
}
