variable "host" {}
variable "port" {}

terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.59.0"
    }
  }
}

provider "aws" {
  endpoints {
    dynamodb = "http://${var.host}:${var.port}"
  }
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}


resource "aws_dynamodb_table" "skims_sca" {
  name                        = "skims_sca"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "pk"
  range_key                   = "sk"
  deletion_protection_enabled = true

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  global_secondary_index {
    name            = "gsi_sk"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "skims_sca"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}
