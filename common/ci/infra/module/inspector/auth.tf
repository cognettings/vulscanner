resource "aws_iam_policy" "main" {
  name = var.name
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

resource "aws_iam_role" "main" {
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
  name = var.name

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_lambda_permission" "main" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}
