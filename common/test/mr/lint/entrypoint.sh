# shellcheck shell=bash

function main {
  local success=0

  : && if common-test-mr-lint-deps; then
    success=$((success + 1))
  fi \
    && if common-test-mr-lint-eslint; then
      success=$((success + 1))
    fi \
    && if test "${success}" -eq 2; then
      info "Congratulations! Your code comply with the suggested style"
    else
      critical "Your code doesn't comply with the suggested style"
    fi
}

main "${@}"
