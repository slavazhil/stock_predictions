resource "aws_apigatewayv2_api" "apigtw" {
  name          = "${var.project_name}_http_api"
  protocol_type = "HTTP"
  target        = aws_lambda_function.lmbd.arn
  route_key     = "GET /"
}

resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lmbd.function_name
  principal     = "apigateway.amazonaws.com"
  # The "/*/*" portion grants access from any method on any resource
  # within the API Gateway REST API.
  source_arn = "${aws_apigatewayv2_api.apigtw.execution_arn}/*/*"
}

output "api_url" {
  value = aws_apigatewayv2_api.apigtw.api_endpoint
}