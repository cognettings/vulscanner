# shellcheck shell=bash

function job_code_upload {
  local group="${1}"
  export AWS_DEFAULT_REGION="us-east-1"

  aws_login "prod_observes" "3600" \
    && ensure_gitlab_env_vars \
      INTEGRATES_API_TOKEN \
      SERVICES_API_TOKEN \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      'bugsnag_notifier_code_etl' \
    && export bugsnag_notifier_key="${bugsnag_notifier_code_etl}" \
    && echo "[INFO] Working on ${group}" \
    && use_git_repo_services \
    && rm -rf -- "groups" \
    && mkdir "groups" \
    && echo "[INFO] Cloning ${group}" \
    && CI=true \
      CI_COMMIT_REF_NAME='trunk' \
      melts --init pull-repos --group "${group}" \
    && chown -R "${USER}" ./groups \
    && ls -la \
    && echo "[INFO] Uploading ${group}" \
    && shopt -s nullglob \
    && observes-etl-code upload-code \
      --arm-token "${INTEGRATES_API_TOKEN}" \
      --namespace "${group}" \
      --mailmap '.groups-mailmap' \
      "groups/${group}/"* \
    && success-indicators compound-job \
      --job 'code_upload' \
      --child "${group}" \
    && shopt -u nullglob \
    && rm -rf "groups/${group}/"
}

job_code_upload "${@}"
