data "archive_file" "main" {
  depends_on       = []
  output_file_mode = "0666"
  output_path      = "${path.module}/src.zip"
  source_dir       = "${path.module}/src"
  type             = "zip"
}

resource "aws_lambda_function" "main" {
  depends_on       = [data.archive_file.main]
  filename         = data.archive_file.main.output_path
  function_name    = var.name
  handler          = "handler.handle"
  role             = aws_iam_role.main.arn
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
  environment {
    variables = {
      BETTER_UPTIME_API_TOKEN = var.better_uptime_api_token
      GITLAB_API_TOKEN        = var.gitlab_api_token
    }
  }

  tags = var.tags
}
