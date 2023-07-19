# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab"

function start_etl {
  aws_login "prod_observes" "3600" \
    && redshift_env_vars \
    && export_notifier_key \
    && gitlab-etl \
      'gitlab-ci' \
      '20741933' \
      's3://observes.state/gitlab_etl/product_state.json' \
      "${UNIVERSE_API_TOKEN}"
}

start_etl
