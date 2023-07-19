# shellcheck shell=bash

alias tap-announcekit="observes-singer-tap-announcekit-bin"

function start_etl {

  aws_login "prod_observes" "3600" \
    && echo '[INFO] Exporting secrets' \
    && redshift_env_vars \
    && sops_export_vars 'observes/secrets/prod.yaml' \
      announcekit_user \
      announcekit_passwd \
      announcekit_fluid_proj \
      bugsnag_notifier_key \
    && export ANNOUNCEKIT_USER="${announcekit_user}" \
    && export ANNOUNCEKIT_PASSWD="${announcekit_passwd}" \
    && echo '[INFO] Running tap' \
    && tap-announcekit stream 'ALL' \
      --project "${announcekit_fluid_proj}" \
      > .singer \
    && echo '[INFO] Running target' \
    && target-redshift destroy-and-upload \
      --schema-name 'announcekit' \
      --truncate \
      < .singer \
    && success-indicators single-job \
      --job 'announcekit'
}

start_etl
