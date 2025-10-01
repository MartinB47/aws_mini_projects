# Project Configuration
project_name = "text-translation-with-llm"
environment  = "dev"

# AWS Configuration
aws_region = "us-east-1"

# Lambda Configuration
lambda_runtime     = "python3.11"
lambda_timeout     = 30
lambda_memory_size = 512

# Bedrock Configuration
bedrock_model_id = "anthropic.claude-3-haiku-20240307-v1:0"

# API Gateway Configuration
api_gateway_stage_name = "v1"

# Monitoring Configuration
log_retention_days = 14