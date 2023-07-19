# shellcheck shell=bash

function main {
  export AWS_DEFAULT_REGION="us-east-1"

  aws_login "prod_observes" "3600" \
    && redshift_env_vars \
    && observes-etl-code init-table "${@}"
}

main "${@}"
