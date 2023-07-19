# shellcheck shell=bash

alias tap-delighted="observes-singer-tap-delighted-bin"

function start_etl {

  aws_login "prod_observes" "3600" \
    && echo '[INFO] Exporting secrets' \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      delighted_api_key \
      bugsnag_notifier_key \
    && echo '[INFO] Running tap' \
    && tap-delighted stream \
      --api-key "${delighted_api_key}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'delighted' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'delighted'
}

start_etl
