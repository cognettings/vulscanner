resource "aws_api_gateway_method" "unsafe_gateway" {
  rest_api_id = aws_api_gateway_rest_api.test.id
  resource_id = aws_api_gateway_resource.test.id
  http_method = "ANY"
}

resource "aws_api_gateway_method" "safe_gateway" {
  rest_api_id = aws_api_gateway_rest_api.test.id
  resource_id = aws_api_gateway_resource.test.id
  http_method = "GET"
}