# shellcheck shell=bash

function main {
  local action="${1:-diff}"
  export DATA=__argData__
  local config

  : \
    && if test -n "${CI-}" && test "${CI_COMMIT_REF_NAME-}" = "trunk" || test -n "${MAKES_AWS_BATCH_COMPAT-}"; then
      aws_login "prod_common" "3600"
      action="deploy"
      config=(--auto-approve)
    else
      aws_login "dev" "3600"
      config=()
    fi \
    && source __argSopsEnv__/template \
    && source __argSopsTerraform__/template \
    && pushd common/status/schedules \
    && npm install --silent \
    && if ! test -d .gen; then
      ./node_modules/.bin/cdktf get
    fi \
    && ./node_modules/.bin/cdktf "${action}" "${config[@]}" \
    && popd \
    || return 1
}

main "${@}"
