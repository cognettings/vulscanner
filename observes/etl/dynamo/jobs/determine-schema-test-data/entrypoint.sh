# shellcheck shell=bash

alias tap-dynamo="observes-singer-tap-dynamo-bin"

function determine_schemas {
  local tables="${1}"
  local segments="${2}"
  local max_concurrency="${3}"
  local cache_bucket="${4}"

  local schemas
  export AWS_DEFAULT_REGION="us-east-1"

  schemas=$(mktemp -d) \
    && aws_login "prod_observes" "3600" \
    && echo '[INFO] Generating secret files' \
    && echo '[INFO] Starting local dynamo...' \
    && { DAEMON=true dynamodb & } \
    && wait \
    && echo '[INFO] Local dynamo is running' \
    && export_notifier_key \
    && echo '[INFO] Determining data schemas from data...' \
    && tap-dynamo stream \
      --tables "${tables}" \
      --segments "${segments}" \
      --endpoint-url "http://localhost:8022" \
      --use-ssl "true" \
      --verify "true" \
      --max-concurrency "${max_concurrency}" \
    | tap-json \
      --date-formats '%Y-%m-%d %H:%M:%S' \
      --schema-folder "${schemas}" \
      --not-dump-records \
    && echo '[INFO] Saving schemas...' \
    && aws_s3_sync "${schemas}" "${cache_bucket}" \
    && echo '[INFO] Schemas saved!'
}

determine_schemas "${@}"
