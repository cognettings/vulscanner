# shellcheck shell=bash

function main {
  aws_login "prod_integrates" "3600" \
    && source __argIntegratesBackEnv__/template "prod" \
    && pushd '__argIntegratesSrc__' \
    && python server_async/__init__.py \
    && popd || return
}

main "${@}"
