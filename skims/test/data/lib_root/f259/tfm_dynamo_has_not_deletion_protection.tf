resource "aws_dynamodb_table" "vuln" {
  name                        = q
  read_capacity               = 1
  write_capacity              = 1
  hash_key                    = 1
  deletion_protection_enabled = false
  attribute {
    name = as
    type = String
  }
}


resource "aws_dynamodb_table" "vuln_2" {
  name           = q
  read_capacity  = 1
  write_capacity = 1
  hash_key       = 1
  attribute {
    name = as
    type = String
  }
}


resource "aws_dynamodb_table" "secure" {
  name                        = q
  read_capacity               = 1
  write_capacity              = 1
  hash_key                    = 1
  deletion_protection_enabled = true
  attribute {
    name = as
    type = String
  }
}
