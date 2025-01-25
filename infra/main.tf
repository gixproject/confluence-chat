terraform {
  backend "s3" {
    bucket = "confluence-chat"
    key    = "states/app/terraform.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      stack       = local.stack_name
      application = local.project_name
      environment = var.environment
    }
  }
}
