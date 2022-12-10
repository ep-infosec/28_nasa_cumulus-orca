## Terraform Requirements
terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.63.0, < 4.0.0"
    }
  }
}