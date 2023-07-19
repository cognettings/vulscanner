resource "aws_s3_bucket" "common_logging" {
  bucket = "common.logging"

  tags = {
    "Name"               = "common.logging"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

#Bucket versioning
resource "aws_s3_bucket_versioning" "common_logging_versioning" {
  bucket = aws_s3_bucket.common_logging.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_acl" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  acl = "private"
}

resource "aws_s3_bucket_lifecycle_configuration" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  rule {
    id     = "delete_logs"
    status = "Enabled"

    expiration {
      days = 180
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

#Bucket public access
resource "aws_s3_bucket_public_access_block" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
