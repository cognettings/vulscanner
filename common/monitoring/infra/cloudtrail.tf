resource "aws_cloudtrail" "master_cloudtrail" {
  name                          = "master-cloudtrail"
  s3_bucket_name                = aws_s3_bucket.master_cloudtrail_bucket.id
  s3_key_prefix                 = "cloudtrail"
  include_global_service_events = true
  enable_log_file_validation    = true
  enable_logging                = true
  is_multi_region_trail         = true

  tags = {
    "Name"               = "cloudtrail"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

/**
 * S3 Bucket for storing CloudTrail logs access logs
 */
resource "aws_s3_bucket" "cloudtrail_access_log_bucket" {
  bucket        = "common-cloudtrail-access-log-bucket"
  force_destroy = true

  tags = {
    "Name"               = "S3 Cloudtrail Access Logs"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "cloudtrail_access_log_bucket_acl" {
  bucket = aws_s3_bucket.cloudtrail_access_log_bucket.id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_public_access_block" "cloudtrail_access_log_bucket" {
  bucket = aws_s3_bucket.cloudtrail_access_log_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

/**
 * S3 bucket for storing CloudTrail logs
 */
resource "aws_s3_bucket" "master_cloudtrail_bucket" {
  bucket        = "common-master-cloudtrail-bucket"
  force_destroy = true

  tags = {
    "Name"               = "S3 Master Cloudtrail"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_versioning" "master_cloudtrail_bucket_versioning" {
  bucket = aws_s3_bucket.master_cloudtrail_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "master_cloudtrail_bucket_logging" {
  bucket = aws_s3_bucket.master_cloudtrail_bucket.id

  target_bucket = aws_s3_bucket.cloudtrail_access_log_bucket.id
  target_prefix = "log/"
}

resource "aws_s3_bucket_public_access_block" "master_cloudtrail_bucket" {
  bucket = aws_s3_bucket.master_cloudtrail_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "cloudtrail_policy" {
  statement {
    sid    = "AWSCloudTrailAclCheck"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.master_cloudtrail_bucket.arn]
  }

  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.master_cloudtrail_bucket.arn}/cloudtrail/AWSLogs/${data.aws_caller_identity.main.account_id}/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }
}

resource "aws_s3_bucket_policy" "cloudtrail_policy" {
  bucket = aws_s3_bucket.master_cloudtrail_bucket.id
  policy = data.aws_iam_policy_document.cloudtrail_policy.json
}
