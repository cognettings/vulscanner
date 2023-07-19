# shellcheck shell=bash

function _clean {
  local src="${1}"
  local paths=(
    "${src}/.docusaurus"
    "${src}/build"
    "${src}/node_modules"
  )

  rm -rf "${paths[@]}"
}

function main {
  local src='docs/src'
  local action="${1:-start}"
  export env="${2:-prod}"
  export branch="${3:-default}"

  _clean "${src}" \
    && generate-criteria \
    && generate-graphs \
    && pushd "${src}" \
    && npm install \
    && npm run "${action}" \
    && popd \
    || return 1
}

main "${@}"
