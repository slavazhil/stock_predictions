#!/bin/bash

# RUN
# ./build_and_push_docker.sh <AWS_ACCOUNT_ID>

# Build the Docker image from the Dockerfile
docker build -t stock_predictions .
# Tag the docker image 
docker tag stock_predictions:latest $1.dkr.ecr.us-east-1.amazonaws.com/stock_predictions:latest
# Push the image
docker push $1.dkr.ecr.us-east-1.amazonaws.com/stock_predictions:latest
