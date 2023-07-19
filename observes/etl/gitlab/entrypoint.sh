# shellcheck shell=bash

function start_etl {
  local schema="${1}"
  local project="${2}"
  local state="${3}"
  local token="${4}"
  export AWS_DEFAULT_REGION="us-east-1"

  echo "[INFO] Gitlab ETL for ${project}" \
    && echo "[INFO] MRs ETL started" \
    && echo '[INFO] Running tap' \
    && tap-gitlab stream \
      "mrs_closed" \
      "mrs_merged" \
      --project "${project}" \
      --api-key "${token}" \
      --max-pages 250 \
      --state "${state}" \
    | tap-json > .singer \
    && echo '[INFO] Running target' \
    && target-redshift only-append \
      --schema-name "${schema}" \
      --s3-state "${state}" \
      --truncate \
      < .singer \
    && echo "[INFO] Jobs ETL started" \
    && tap-gitlab stream \
      "pipe_jobs_success" \
      "pipe_jobs_failed" \
      "pipe_jobs_canceled" \
      "pipe_jobs_skipped" \
      "pipe_jobs_manual" \
      --project "${project}" \
      --api-key "${token}" \
      --max-pages 10 \
      --state "${state}" \
      > .singer_2 \
    && echo '[INFO] Running target' \
    && target-redshift only-append \
      --schema-name "${schema}" \
      --s3-state "${state}" \
      --truncate \
      < .singer_2
}

start_etl "${@}"
