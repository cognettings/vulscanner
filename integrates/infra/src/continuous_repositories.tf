# Production
resource "aws_s3_bucket" "integrates_continuos_repositories" {
  bucket = "integrates.continuous-repositories"

  tags = {
    "Name"               = "integrates.continuous-repositories"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_logging" "integrates_continuos_repositories" {
  bucket = aws_s3_bucket.integrates_continuos_repositories.id

  target_bucket = "common.logging"
  target_prefix = "log/integrates"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "integrates_continuos_repositories" {
  bucket = aws_s3_bucket.integrates_continuos_repositories.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "integrates_continuos_repositories" {
  bucket = aws_s3_bucket.integrates_continuos_repositories.id

  versioning_configuration {
    status = "Disabled"
  }
}
