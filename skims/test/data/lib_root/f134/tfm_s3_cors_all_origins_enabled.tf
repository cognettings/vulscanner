resource "aws_s3_bucket_cors_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]
  }

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["https://s3-website-test.hashicorp.com"]
  }
}