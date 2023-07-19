# shellcheck shell=bash

function main {
  : && pushd common/utils/retrieves \
    && lint_npm_deps package.json \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && tsc --noEmit -p tsconfig.json \
    && eslint . --ext ".ts" --fix \
    && popd \
    || return 1
}

main "$@"
