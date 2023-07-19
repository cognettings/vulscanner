resource "aws_iam_user_policy" "unsafe_user_policy" {
  name = "safe_role_1"
  user = aws_iam_user.lb.name

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        }
      }
    ]
  }
  EOF
}