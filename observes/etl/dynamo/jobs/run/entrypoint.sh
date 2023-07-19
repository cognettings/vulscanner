# shellcheck shell=bash

function execute {
  local selection="${1}"

  : \
    && export_notifier_key \
    && redshift_env_vars \
    && echo "[INFO] Executing job: ${selection}" \
    && dynamo-etl run "${selection}"
}

execute "${@}"
