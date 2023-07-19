resource "aws_s3_bucket_policy" "unsafe_pol1" {
  bucket = "test"

  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Id": "MYBUCKETPOLICY",
    "Statement": [
      {
        "Effect": "Allow",
        "Condition": {
          "Null": {
            "s3:x-amz-server-side-encryption": false
          }
        }
      }
    ]
  }
  POLICY
}

resource "aws_s3_bucket_policy" "unsafe_pol2" {
  bucket = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Condition = {
          Null = {
            "s3:x-amz-server-side-encryption" = false
          }
        }
      },
    ]
  })
}