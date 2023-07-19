# shellcheck shell=bash

alias target-redshift="observes-target-redshift"

function start_etl {
  local db_creds="${1}"
  local zoho_creds="${2}"
  local target_schema="${3}"
  local job_name="${4}"

  tap-zoho-crm stream "${zoho_creds}" "${db_creds}" \
    | tap-csv \
    | tap-json \
      > .singer \
    && target-redshift \
      --auth "${db_creds}" \
      --schema-name "${target_schema}" \
      --drop-schema \
      --old-ver \
      < .singer \
    && success-indicators single-job \
      --job "${job_name}"
}

start_etl "${@}"
