# shellcheck shell=bash

export AWS_DEFAULT_REGION="us-east-1"

db-snapshot "${@}"
