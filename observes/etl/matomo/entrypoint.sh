# shellcheck shell=bash

alias tap-matomo="observes-singer-tap-matomo-bin"

function job_matomo {
  echo '[INFO] Exporting secrets' \
    && mkdir ./logs \
    && export_notifier_key \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      MATOMO_API_TOKEN \
    && echo '[INFO] Running tap' \
    && tap-matomo \
      --end-date "$(date +"%Y-%m-%d")" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'matomo' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'matomo'
}

job_matomo
