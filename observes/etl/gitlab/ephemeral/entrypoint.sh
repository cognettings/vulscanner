# shellcheck shell=bash

function start_etl {
  local schema="${1}"
  local project="${2}"
  local api_key="${3}"
  export AWS_DEFAULT_REGION="us-east-1"

  echo '[INFO] Starting ephemeral ETL' \
    && echo '[INFO] Running tap' \
    && tap-gitlab stream "issues" "members" \
      --project "${project}" \
      --api-key "${api_key}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name "${schema}" \
      --truncate \
      < .singer \
    && rm .singer
}

start_etl "${@}"
