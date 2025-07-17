# Configure the AWS provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Create VPC
# This is the main container for all AWS networking resources"
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  # Allows instances to have DNS hostnames
  enable_dns_hostnames = true

  # Enables DNS resolution within the VPC
  enable_dns_support = true

  # Control if instances run on shared or dedicated hardware
  instance_tenancy = "default"

  # Disable ipv6 support (default)
  assign_generated_ipv6_cidr_block = false

  # Do not monitor IP address usage (default)
  enable_network_address_usage_metrics = false

  tags = {
    Name = "main-vpc"
  }
}

# Create Internet Gateway
# This allows communication between VPC and the internet
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

# Create public subnet
# This subnet will have direct internet access via the Internet Gateway
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  # Auto-assign public IP to instances
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
    Type = "Public"
  }
}

# Data source to get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# Create route table for public subnet
# Route tables control where network traffic is directed
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # Route for internet access (0.0.0.0/0 means all traffic)
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-rt"
  }
}

# Associate the route table with the public subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Create security group
# Acts as a virtual firewall controlling inbound and outbound traffic
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP traffic from anywhere
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS traffic from anywhere
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH from anywhere (in production restrict this)
  ingress {
    description = "HTTPS"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port = 0
    to_port   = 0
    # -1 means all protocols
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-security-group"
  }
}

# Get the default security group for VPC
data "aws_security_group" "default" {
  vpc_id = aws_vpc.main.id
  name   = "default"
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.web.id
}

output "internet_gateway_id" {
  description = "ID of the internet gateway"
  value       = aws_internet_gateway.main.id
}

output "default_network_acl_id" {
  description = "ID of the default network ACL (created automatically by AWS)"
  value       = aws_vpc.main.default_network_acl_id
}

output "default_route_table_id" {
  description = "ID of the default network ACL (created automatically by AWS)"
  value       = aws_vpc.main.default_route_table_id
}

output "default_security_group_id" {
  description = "ID of the default security group (created automatically by AWS)"
  value       = data.aws_security_group.default.id
}
