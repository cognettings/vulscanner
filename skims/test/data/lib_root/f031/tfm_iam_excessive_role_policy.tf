resource "aws_iam_role" "fluid_example" {
  name = "test_role"
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role = aws_iam_role.fluid_example.name
}

resource "aws_iam_policy" "test_policy" {
  name = "test_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*"
      ],
      "Resource": "*"
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
        Effect = "Allow"
        Action = [
          "iam:Attach*"
        ],
        Resource = "arn:aws:iam:::role/test_role"
      },
    ]
  })
}

data "aws_iam_policy_document" "example" {
  statement {
    actions = [
      "iam:Attach*"
    ]

    resources = [
      "arn:aws:iam:::role/test_role",
    ]
  }
}
