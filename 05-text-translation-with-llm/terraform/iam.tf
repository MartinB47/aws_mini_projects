#-----------------------------------------------------------------------------
# IAM Role and Policies for Lambda Function
# Following principle of least privilege
#-----------------------------------------------------------------------------

# IAM role that Lambda function will assume
resource "aws_iam_role" "lambda_execution_role" {
  name = "${local.name_prefix}-lambda-execution-role"

  # Trust policy allowing Lambda service to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(local.common_tags, {
    Name        = "${local.name_prefix}-lambda-execution-role"
    Description = "Execution role for translation Lambda function"
  })
}

# Attach basic Lambda execution policy (for CloudWatch logs)
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_execution_role.name
}

# Custom policy for Bedrock access
resource "aws_iam_role_policy" "bedrock_access" {
  name = "${local.name_prefix}-bedrock-access"
  role = aws_iam_role.lambda_execution_role.id

  # Policy allowing specific Bedrock model invocation
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = [
          "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/${var.bedrock_model_id}",
          "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/anthropic.claude-*"
        ]
      }
    ]
  })
}

#-----------------------------------------------------------------------------
# Lambda Permissions
# Allow API Gateway to invoke Lambda function
#-----------------------------------------------------------------------------
resource "aws_lambda_permission" "api_gateway_invoke" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.translator.function_name
  principal     = "apigateway.amazonaws.com"

  # Specific permission for this API Gateway
  source_arn = "${aws_api_gateway_rest_api.translation_api.execution_arn}/*/*"
}


