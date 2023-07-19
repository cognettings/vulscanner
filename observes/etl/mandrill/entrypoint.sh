# shellcheck shell=bash

function start_etl {
  echo '[INFO] Exporting secrets' \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      mandrill_api_key \
    && redshift_env_vars \
    && echo '[INFO] Running tap' \
    && tap-mandrill stream "activity" \
      --api-key "${mandrill_api_key}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'mandrill' \
      --truncate \
      < .singer
}

start_etl
