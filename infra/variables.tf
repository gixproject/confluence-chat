variable "region" {
  description = "Value for the AWS region"
  default     = "us-east-1"
}

variable "availability_zone" {
  description = "Value for the AWS availability zone"
  default     = "us-east-1b"
}

variable "environment" {
  description = "Value to define the current environment for all resources"
}

variable "project_source" {
  description = "Value for the project files destination"
}

variable "confluence_host" {}
variable "confluence_email" {}
variable "confluence_token" {}
