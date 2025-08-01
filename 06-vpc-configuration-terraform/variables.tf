variable "aws_region" { 
    description = "AWS region"
    type = string
    default = "us-east-1"
}

variable "vpc_cidr" {
    description = "CIDR block for VPC"
    type = string
    default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
    description = "CIDR block for the public subnet"
    type = string
    default = "10.0.1.0/24"
}