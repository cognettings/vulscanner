
data "aws_secretsmanager_random_password" "unsafe_generator" {
  password_length            = 12
  exclude_numbers            = true
  exclude_lowercase          = true
  require_each_included_type = false
  exclude_characters         = "0123456789"
}

data "aws_secretsmanager_random_password" "safe_generator" {
  password_length            = 16
  exclude_numbers            = false
  exclude_lowercase          = false
  require_each_included_type = true
  exclude_characters         = "*_"
}