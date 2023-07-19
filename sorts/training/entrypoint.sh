# shellcheck shell=bash

function main {
  export AWS_DEFAULT_REGION="us-east-1"

  : \
    && aws_login "prod_sorts" "3600" \
    && sops_export_vars 'sorts/secrets.yaml' \
      'REDSHIFT_DATABASE' \
      'REDSHIFT_HOST' \
      'REDSHIFT_PASSWORD' \
      'REDSHIFT_PORT' \
      'REDSHIFT_USER' \
    && pushd sorts \
    && python3.11 training/redshift/db.py init-db \
    && echo "[INFO] Initializing training..." \
    && python3.11 training/sagemaker_provisioner.py \
    && echo "[INFO] Evaluating resulting artifacts..." \
    && python3.11 training/evaluate_results.py train \
    && popd \
    || return 1
}

main "${@}"
