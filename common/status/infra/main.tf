terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    betteruptime = {
      source  = "BetterStackHQ/better-uptime"
      version = "0.3.18"
    }
    checkly = {
      source  = "checkly/checkly"
      version = "1.6.5"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-status.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  region = "us-east-1"
}
provider "betteruptime" {
  api_token = var.betterUptimeApiToken
}
provider "checkly" {
  account_id = var.accountId
  api_key    = var.apiKey
}
