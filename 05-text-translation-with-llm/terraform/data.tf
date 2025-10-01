# Data sources for current AWS account and region information
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Local values for consistent resource naming
locals {
  # Consistent naming convention across all resources
  name_prefix = "${var.project_name}-${var.environment}"

  # Common tags for all resources
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Component   = "text-translation-with-llm"
  }
}