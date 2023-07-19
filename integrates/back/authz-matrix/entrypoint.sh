# shellcheck shell=bash

function main {
  source __argIntegratesBackEnv__/template dev \
    && pushd integrates \
    && python3 back/deploy/permissions_matrix/matrix.py \
    && popd \
    || return 1
}

main "${@}"
