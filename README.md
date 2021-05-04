# Prerequisites

1. AWS CLI
2. Terraform CLI
3. Docker

# Build and host a Docker container

Build the Docker image from the Dockerfile
`docker build -t stock_predictions .`

Authenticate to Amazon ECR (Elastic Container Registry)
`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com`

Create a repository
`aws ecr create-repository --repository-name stock_predictions --image-scanning-configuration scanOnPush=true --region us-east-1`

Tag the docker image 
`docker tag stock_predictions:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/stock_predictions:latest`

Push the image
`docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/stock_predictions:latest`

# Deploy lambda from the docker image

Make sure `profile = "default"` in `main.tf` matches you AWS CLI profile name.

In `lambda.tf` update `image_uri = "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/stock_predictions@sha256:<SHA_256>"`

Run `terraform init && terraform apply`
Copy url from the output `api_url = <API_URL>`

# Result

Open your browser and enter: 
`<API_URL>/?ticker=TSLA&interval=d`

where `interval` can be `d` for days or `h` for hours.

# Clean up

To delete infrastructure run`terraform destroy`