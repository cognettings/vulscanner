# shellcheck shell=bash

function migration {
  local namespace="${1}"

  aws_login "prod_observes" "3600" \
    && redshift_env_vars \
    && observes-etl-code migration calculate-fa-hash \
      "${namespace}" \
      --source "code" "commits" \
      --target "code" "migrated"
}

migration "${@}"
