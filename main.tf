provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

variable "project_name" {
  default = "stock_predictions"
}