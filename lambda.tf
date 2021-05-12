resource "aws_lambda_function" "lmbd" {
    function_name = "${var.project_name}_lambda"
    role = aws_iam_role.role.arn
    memory_size = 5120
    timeout = 30
    package_type = "Image"
    image_uri = "062087429298.dkr.ecr.us-east-1.amazonaws.com/stock_predictions@sha256:d4f393ac90b36807e444be4d6d2be03353df1055e66eb2bd53276a6d55d3a0b2"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "role" {
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  name               = "${var.project_name}_lambda_role"
}

resource "aws_iam_role_policy_attachment" "basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.role.name
}
