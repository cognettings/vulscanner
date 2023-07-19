variable "betterUptimeApiToken" {}
variable "gitlabApiToken" {}
variable "gitlabRunnerToken" {}
variable "region" {
  default = "us-east-1"
}

# Reused infrastructure from other services

data "aws_caller_identity" "main" {}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}

data "aws_subnet" "main" {
  for_each = toset([
    "ci_1",
    "ci_2",
    "ci_3",
    "ci_4",
    "ci_5",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}
