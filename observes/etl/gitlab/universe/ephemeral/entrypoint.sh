# shellcheck shell=bash

alias gitlab-etl="observes-etl-gitlab-ephemeral"

function start_etl {
  aws_login "prod_observes" "3600" \
    && redshift_env_vars \
    && export_notifier_key \
    && gitlab-etl \
      'gitlab_ci_issues' \
      '20741933' \
      "${UNIVERSE_API_TOKEN}"
}

start_etl
