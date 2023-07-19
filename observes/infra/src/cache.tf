resource "aws_s3_bucket" "observes_cache" {
  bucket = "observes.cache"

  tags = {
    "Name"               = "observes.cache"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

# Bucket logging
resource "aws_s3_bucket_logging" "observes_cache_logs" {
  bucket = aws_s3_bucket.observes_cache.id

  target_bucket = "common.logging"
  target_prefix = "log/observes.cache"
}

#Bucket versioning
resource "aws_s3_bucket_versioning" "observes_cache_versioning" {
  bucket = aws_s3_bucket.observes_cache.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_acl" "observes_cache" {
  bucket = aws_s3_bucket.observes_cache.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "observes_cache" {
  bucket = aws_s3_bucket.observes_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

#Bucket public access
resource "aws_s3_bucket_public_access_block" "observes_cache" {
  bucket = aws_s3_bucket.observes_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
