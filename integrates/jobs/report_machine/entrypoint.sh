# shellcheck shell=bash

function main {
  aws_login "prod_integrates" "3600" \
    && source __argIntegratesBackEnv__/template "${1}" \
    && python __argMain__ "${2}" \
    && return
}

main "${@}"
