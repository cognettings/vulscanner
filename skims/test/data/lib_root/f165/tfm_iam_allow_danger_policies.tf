resource "aws_iam_policy" "test_policy" {
  name = "test_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "NotAction": [
        "ec2:Describe*"
      ],
      "NotResource": "*"
    },
    {
        "Effect": "Allow",
        "Action": [
            "iam:Attach*",
            "iam:Create*"
        ],
        "Resource": [
            "arn:aws:iam:::role/test_role"
        ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "vuln_role_1" {
  name = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect      = "Allow"
        NotResource = ["arn:aws:iam:::db/my_db"]
        NotAction   = ["iam:Attach:"]
      },
    ]
  })
}

data "aws_iam_policy_document" "vuln_policy_doc" {
  statement {
    effect = "Allow"

    not_resources = [
      "arn:aws:iam:::role/some_res",
    ]

    not_actions = [
      "s3:GetObject",
    ]
  }

  statement {
    effect = "Allow"

    resources = [
      "arn:aws:iam:::role/some_res",
    ]
  }
}
