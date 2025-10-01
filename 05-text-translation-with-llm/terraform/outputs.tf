# API Gateway URL for accessing the translation service
output "api_gateway_url" {
  description = "Base URL for the translation API"
  value       = "https://${aws_api_gateway_rest_api.translation_api.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_stage.api_stage.stage_name}"
}

# Complete translation endpoint URL
output "translation_endpoint" {
  description = "Full URL for the translation endpoint"
  value       = "https://${aws_api_gateway_rest_api.translation_api.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_stage.api_stage.stage_name}/translate"
}

# Lambda function details
output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.translator.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.translator.arn
}

# API Gateway details
output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.translation_api.id
}

# CloudWatch log group
output "lambda_log_group" {
  description = "CloudWatch log group name for Lambda function"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

# IAM role ARN
output "lambda_execution_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_execution_role.arn
}

# Environment information
output "environment_info" {
  description = "Environment and project information"
  value = {
    project_name = var.project_name
    environment  = var.environment
    aws_region   = var.aws_region
  }
}