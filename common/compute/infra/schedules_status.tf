resource "aws_iam_policy" "lambda_loggning" {
  name = "lambda_loggning"
  policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {
          Sid    = "lambdaCloudWatchAccess"
          Effect = "Allow"
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
          ]
          Resource = [
            "arn:aws:logs:${var.region}:${data.aws_caller_identity.main.account_id}:*"
          ]
        },
        {
          Sid      = "lambdaInvocation"
          Effect   = "Allow"
          Action   = ["lambda:InvokeFunction"]
          Resource = ["arn:aws:lambda:*:*:function:*"]
        },
      ]
    }
  )
}

resource "aws_iam_role" "lambda_assume_policies" {
  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {
          Sid    = "AssumeRolePolicy",
          Effect = "Allow",
          Principal = {
            Service = ["lambda.amazonaws.com"],
          },
          Action = "sts:AssumeRole",
        },
      ],
    }
  )
  name = "lambda_assume_policies"
  tags = {
    "Name"               = "lambda_assume_policies"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_batch_attach_policy" {
  role       = aws_iam_role.lambda_assume_policies.name
  policy_arn = aws_iam_policy.lambda_loggning.arn
}

resource "aws_cloudwatch_event_rule" "batch_status_change" {
  name = "batch_status_change"
  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
  })
}

data "archive_file" "main" {
  depends_on       = []
  output_file_mode = "0666"
  output_path      = "${path.module}/batch_job_handler.zip"
  source_dir       = "${path.module}/batch_job_handler"
  type             = "zip"
}

resource "aws_lambda_function" "bath_jobs_status_change" {
  depends_on       = [data.archive_file.main]
  filename         = data.archive_file.main.output_path
  function_name    = "bath_jobs_status_change"
  handler          = "handler.handle"
  role             = aws_iam_role.lambda_assume_policies.arn
  runtime          = "python3.10"
  source_code_hash = data.archive_file.main.output_base64sha256
  architectures    = ["arm64"]
  timeout          = 60

  layers = [
    # https://api.klayers.cloud/api/v2/p3.10/layers/latest/us-east-1/
    "arn:aws:lambda:${var.region}:770693421928:layer:Klayers-p310-requests:1",
  ]

  tracing_config {
    mode = "Active"
  }
  tags = {
    "Name"               = "bath_jobs_status_change"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "bath_jobs_status_change" {
  target_id = "bath_jobs_status_change"
  rule      = aws_cloudwatch_event_rule.batch_status_change.name
  arn       = aws_lambda_function.bath_jobs_status_change.arn
  # role_arn  = aws_iam_role.lambda_batch.arn
}

resource "aws_lambda_permission" "main" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bath_jobs_status_change.function_name
  principal     = "events.amazonaws.com"

  source_arn = aws_cloudwatch_event_rule.batch_status_change.arn
}
