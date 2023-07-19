resource "aws_s3_bucket" "machine_data" {
  bucket = "machine.data"

  tags = {
    "Name"               = "machine.data"
    "management:area"    = "cost"
    "management:product" = "machine"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

# Bucket logging
resource "aws_s3_bucket_logging" "machine_data_logs" {
  bucket = aws_s3_bucket.machine_data.id

  target_bucket = "common.logging"
  target_prefix = "log/machine.data"
}

resource "aws_s3_bucket_acl" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


resource "aws_s3_bucket_lifecycle_configuration" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  rule {
    id     = "machine_data_cache"
    status = "Enabled"

    filter {
      prefix = "cache/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_data_configs"
    status = "Enabled"

    filter {
      prefix = "configs/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_data_results"
    status = "Enabled"

    filter {
      prefix = "results/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_celery_results_backend"
    status = "Enabled"

    filter {
      prefix = "celery_result_backend/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
}

resource "aws_s3_bucket_versioning" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket_public_access_block" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
