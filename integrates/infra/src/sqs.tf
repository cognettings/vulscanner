resource "aws_sqs_queue" "integrates_tasks" {
  name                      = "integrates_tasks"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  tags = {
    "Name"               = "integrates_tasks"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_tasks_dev" {
  name                      = "integrates_tasks_dev"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  tags = {
    "Name"               = "integrates_tasks_dev"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_clone" {
  name                      = "integrates_clone"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.integrates_dead_queue.arn
    maxReceiveCount     = 3
  })
  tags = {
    "Name"               = "integrates_clone"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_refresh" {
  name                      = "integrates_refresh"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.integrates_dead_queue.arn
    maxReceiveCount     = 3
  })
  tags = {
    "Name"               = "integrates_refresh"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_rebase" {
  name                      = "integrates_rebase"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.integrates_dead_queue.arn
    maxReceiveCount     = 3
  })
  tags = {
    "Name"               = "integrates_rebase"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_report" {
  name                      = "integrates_report"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.integrates_dead_queue.arn
    maxReceiveCount     = 3
  })
  tags = {
    "Name"               = "integrates_report"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
resource "aws_sqs_queue" "integrates_report_soon" {
  name                      = "integrates_report_soon"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.integrates_dead_queue.arn
    maxReceiveCount     = 3
  })
  tags = {
    "Name"               = "integrates_report_soon"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_sqs_queue" "integrates_streams_dlq" {
  name                      = "integrates_streams_dlq"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10

  tags = {
    "Name"               = "integrates_streams_dlq"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_sqs_queue" "integrates_dead_queue" {
  name                      = "integrates_dead_queue"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10
  fifo_queue                = false

  tags = {
    "Name"               = "integrates_dead_queue"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
