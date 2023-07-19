# shellcheck shell=bash

function redshift_env_vars {
  sops_export_vars 'observes/secrets/prod.yaml' \
    REDSHIFT_DATABASE \
    REDSHIFT_HOST \
    REDSHIFT_PORT \
    REDSHIFT_USER \
    REDSHIFT_PASSWORD
}

function json_db_creds {
  local target="${1}"
  redshift_env_vars \
    && jq -n \
      --arg n "${REDSHIFT_DATABASE}" \
      --arg h "${REDSHIFT_HOST}" \
      --arg p "${REDSHIFT_PORT}" \
      --arg u "${REDSHIFT_USER}" \
      --arg pw "${REDSHIFT_PASSWORD}" \
      '{dbname: $n, host: $h, port: $p, user: $u, password: $pw}' \
      > "${target}"
}

function export_notifier_key {
  sops_export_vars 'observes/secrets/prod.yaml' \
    bugsnag_notifier_key
}
