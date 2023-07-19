#!/bin/bash

# Set the AWS access key ID and secret access key as environment variables
export AWS_ACCESS_KEY_ID=AKIA0000000000000000
export AWS_SECRET_ACCESS_KEY=my-secret-access-key

# Use the AWS CLI to list all S3 buckets
aws s3 ls
