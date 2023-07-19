# shellcheck shell=bash

function main {
  local dir="common/test/mr"

  : && pushd "${dir}" \
    && copy __argNodeModules__ ./node_modules \
    && tsc -p tsconfig.json \
    && ./node_modules/.bin/eslint . \
    && popd \
    || return 1
}

main "$@"
