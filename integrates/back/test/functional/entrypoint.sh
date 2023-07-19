# shellcheck shell=bash

function main {
  local resolver_test_group="${1}"
  export BATCH_BIN
  export COVERAGE_FILE=.coverage."${resolver_test_group}"
  local populate_db=false
  local pytest_args=(
    --cov 'back/src'
    --cov-report 'term'
    --disable-warnings
    --no-cov-on-fail
    --showlocals
    --resolver-test-group "${resolver_test_group}"
    -vv
  )
  if echo "$@" | grep -q " --populate-db "; then
    populate_db="--populate-db"
  fi
  if echo "$@" | grep -q "update_snapshot"; then
    pytest_args+=(--snapshot-update)
  else
    pytest_args+=("--exitfirst")
  fi
  local needs_s3=(
    add_forces_execution
    add_git_root
    batch_dispatch
    download_vulnerability_file
    forces_executions
    group
    remove_event_evidence
    remove_evidence
    remove_files
    remove_finding
    remove_group
    remove_toe_port
    report_machine
    report_toe_lines
    subscribe_to_entity_report
    sync_git_root
    unfulfilled_standard_report_url
    update_event_evidence
    update_evidence
    update_git_root
    update_group
    refresh_toe_lines
  )

  : \
    && source __argIntegratesBackEnv__/template dev \
    && sops_export_vars integrates/secrets/development.yaml \
      TEST_SSH_KEY \
    && if [[ ${needs_s3[*]} =~ ${resolver_test_group} ]]; then
      : \
        && export AWS_S3_PATH_PREFIX="${CI_COMMIT_REF_NAME}-test-functional-${resolver_test_group}/" \
        && populate_storage "/${CI_COMMIT_REF_NAME}-test-functional-${resolver_test_group}"
    fi \
    && DAEMON=true POPULATE="${populate_db}" integrates-db \
    && BATCH_BIN="$(command -v integrates-batch)" \
    && echo "[INFO] Running tests for: ${resolver_test_group}" \
    && pushd integrates \
    && PYTHONPATH="back/src/:back/migrations/:$PYTHONPATH" \
    && pytest back/test/functional/src "${pytest_args[@]}" \
    && popd \
    || return 1
}

main "${@}"
