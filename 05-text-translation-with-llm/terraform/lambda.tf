# CloudWatch Log Group for Lambda Function
# Create this first to ensure proper log capture from the start
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.name_prefix}-translator"
  retention_in_days = var.log_retention_days

  tags = merge(local.common_tags, {
    Name        = "${local.name_prefix}-lambda-logs"
    Description = "Log group for translation Lambda function"
  })
}

# Lambda Function Package Creation
# Creates deployment package from source code

# Create a zip file from the Lambda source code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/src"
  output_path = "${path.module}/lambda_function.zip"

  # Ensure the zip is recreated when source files change
  excludes = [
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    "tests/"
  ]
}

# Lambda Function
# Core compute component for translation processing
resource "aws_lambda_function" "translator" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "${local.name_prefix}-translator"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  # Source code hash for deployment updates
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  # Environment variables for Lambda function
  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
      LOG_LEVEL        = var.environment == "prod" ? "INFO" : "DEBUG"
      ENVIRONMENT      = var.environment
    }
  }

  # Explicit dependency on CloudWatch log group
  depends_on = [
    aws_cloudwatch_log_group.lambda_logs,
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]

  tags = merge(local.common_tags, {
    Name        = "${local.name_prefix}-translator"
    Description = "Lambda function for text translation using Bedrock"
  })
}
