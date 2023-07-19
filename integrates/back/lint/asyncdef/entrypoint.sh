# shellcheck shell=bash

function main {

  source __argIntegratesBackEnv__/template dev \
    && pushd integrates \
    && info "Linting functions async..." \
    && python back/lint/asyncdef/lint_async.py \
    && popd \
    || return 1
}

main "${@}"
