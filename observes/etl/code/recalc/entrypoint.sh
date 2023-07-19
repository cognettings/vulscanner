# shellcheck shell=bash

function job_code_upload {
  local group="${1}"
  export AWS_DEFAULT_REGION="us-east-1"

  aws_login "prod_observes" "3600" \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      'bugsnag_notifier_code_etl' \
    && export bugsnag_notifier_key="${bugsnag_notifier_code_etl}" \
    && echo "[INFO] Re calculating hash for ${group}" \
    && observes-etl-code re-calc-hash \
      --namespace "${group}"
}

job_code_upload "${@}"
