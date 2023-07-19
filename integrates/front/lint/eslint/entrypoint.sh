# shellcheck shell=bash

function main {
  : && pushd integrates/front \
    && copy __argSetupIntegratesFrontDevRuntime__ ./node_modules \
    && tsc -p tsconfig.json \
    && ./node_modules/.bin/eslint . \
    && popd \
    || return 1
}

main "$@"
