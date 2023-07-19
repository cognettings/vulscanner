resource "aws_apigatewayv2_api" "main" {
  name          = var.name
  protocol_type = "HTTP"

  tags = var.tags
}

resource "aws_apigatewayv2_stage" "main" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "${var.name}-gitlab-webhook"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }

  tags = var.tags
}

resource "aws_apigatewayv2_integration" "main" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.main.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"

}

resource "aws_apigatewayv2_route" "issue" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /issue"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_apigatewayv2_route" "pipeline" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /pipeline"
  target    = "integrations/${aws_apigatewayv2_integration.main.id}"
}

resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/main/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 0
}
