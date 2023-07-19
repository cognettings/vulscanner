# shellcheck shell=bash

function main {
  local dir="common/test/mr"

  lint_npm_deps "${dir}/package.json"
}

main "${@}"
