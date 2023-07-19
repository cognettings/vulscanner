resource "aws_dynamodb_table" "terraform_state_lock" {
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "LockID"
  name                        = "terraform_state_lock"
  deletion_protection_enabled = true

  attribute {
    name = "LockID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "terraform_state_lock"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
