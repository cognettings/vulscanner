data "aws_caller_identity" "current" {}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "main" {
  for_each = toset([
    "observes_1",
    "observes_2",
    "observes_3",
    "observes_4",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}

data "aws_iam_role" "observes_redshift_cluster" {
  name = "observes_redshift_cluster"
}

data "aws_iam_role" "observes_redshift_scheduler" {
  name = "observes_redshift_scheduler"
}
