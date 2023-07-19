
resource "aws_s3_bucket" "test" {
  bucket = "yotto"
}

resource "aws_s3_bucket_versioning" "vuln_bucket" {
  bucket = aws_s3_bucket.test.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_versioning" "safe_bucket" {
  bucket = aws_s3_bucket.test.id

  versioning_configuration {
    status = "Enabled"
  }
}