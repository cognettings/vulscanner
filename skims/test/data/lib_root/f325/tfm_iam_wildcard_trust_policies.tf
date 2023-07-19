resource "aws_iam_role" "vuln_role_1" {
  name = "safe_role_1"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Resource": "*",
        "Action": "*",
        "Effect": "Allow"
      }
    ]
  }
  EOF
}

resource "aws_iam_role" "vuln_role_2" {
  name = "vuln_role_1"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "*"
        ],
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role" "safe_role_1" {
  name = "safe_role_1"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": "arn:aws:codecommit::111111111111:test"
      }
    ]
  }
  EOF
}
