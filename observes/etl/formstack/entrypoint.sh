# shellcheck shell=bash

alias tap-formstack="observes-singer-tap-formstack-bin"

function start_etl {
  local formstack_creds

  formstack_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && export_notifier_key \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      analytics_auth_formstack \
    && echo '[INFO] Generating secret files' \
    && echo "${analytics_auth_formstack}" > "${formstack_creds}" \
    && redshift_env_vars \
    && echo '[INFO] Running tap' \
    && mkdir ./logs \
    && tap-formstack \
      --auth "${formstack_creds}" \
      --conf ./observes/conf/formstack.json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'formstack' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'formstack'
}

start_etl
