resource "aws_s3_bucket_policy" "b" {
  bucket = aws_s3_bucket.b.id

  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Id": "MYBUCKETPOLICY",
    "Statement": [
      {
        "Sid": "IPAllow",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": "arn:aws:s3:::my_tf_test_bucket/*",
        "Condition": {
            "IpAddress": {"aws:SourceIp": "8.8.8.8/32"},
            "Bool": {"aws:SecureTransport": "False"}
        }
      }
    ]
  }
  POLICY
}


resource "aws_s3_bucket_policy" "b" {
  name = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "MYBUCKETPOLICY"
    Statement = [
      {
        Sid    = "IPAllow"
        Action = "s3:*"
        Effect = "Allow"
        Condition = {
          Bool = { "aws:SecureTransport" = "False" }
        }
      },
    ]
  })
}
