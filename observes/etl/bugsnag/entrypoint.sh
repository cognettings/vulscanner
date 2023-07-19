# shellcheck shell=bash

alias tap-bugsnag="observes-singer-tap-bugsnag-bin"

function start_etl {

  aws_login "prod_observes" "3600" \
    && echo '[INFO] Exporting secrets' \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      bugsnag_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Running tap' \
    && tap-bugsnag stream \
      --api-key "${bugsnag_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'bugsnag' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'bugsnag'
}

start_etl
