terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.66.1"
    }
  }
}

data "aws_caller_identity" "main" {}

variable "better_uptime_api_token" {}
variable "gitlab_api_token" {}
variable "name" {}
variable "region" {}
variable "tags" {}

output "endpoint" {
  value = aws_apigatewayv2_stage.main.invoke_url
}
