# shellcheck shell=bash

alias tap-mailchimp="observes-singer-tap-mailchimp-bin"

function start_etl {
  local mailchimp_creds

  mailchimp_creds=$(mktemp) \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Exporting secrets' \
    && export_notifier_key \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      mailchimp_api_key \
      mailchimp_dc \
    && {
      echo '{'
      echo "\"api_key\":\"${mailchimp_api_key}\","
      echo "\"dc\":\"${mailchimp_dc}\""
      echo '}'
    } > "${mailchimp_creds}" \
    && echo '[INFO] Running tap' \
    && tap-mailchimp stream \
      --creds-file "${mailchimp_creds}" \
      --all-streams \
    | tap-json \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'mailchimp' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'mailchimp'
}

start_etl
