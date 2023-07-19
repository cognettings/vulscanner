data "aws_caller_identity" "main" {}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
variable "region" {
  default = "us-east-1"
}

# Reused infrastructure

data "aws_iam_role" "main" {
  for_each = toset([
    "dev",
    "prod_airs",
    "prod_common",
    "prod_docs",
    "prod_integrates",
    "prod_melts",
    "prod_observes",
    "prod_skims",
    "prod_sorts",
  ])

  name = each.key
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "clone" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_clone"]
  }
}
data "aws_subnet" "main" {
  for_each = toset([
    "batch_main_1",
    "batch_main_2",
    "batch_main_3",
    "batch_main_4",
    "batch_main_5",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}


data "terraform_remote_state" "terraform_schedules_output" {
  backend = "s3"

  config = {
    "bucket"         = "fluidattacks-terraform-states-prod"
    "dynamodb_table" = "terraform_state_lock"
    "key"            = "schedules-status.tfstate"
    "region"         = "us-east-1"
  }
}
