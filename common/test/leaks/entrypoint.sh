# shellcheck shell=bash

function main {
  local commit_msg

  : && info "Looking for leaked secrets in your commit" \
    && commit_msg="$(git --no-pager log HEAD^..HEAD)" \
    && if echo "${commit_msg}" | grep -q -- "- no-leaks-test"; then
      : && warn "You are using '- no-leaks-test'. Make sure you're not commiting any secrets." \
        && return 0
    fi \
    && if ! gitleaks --verbose detect --log-opts="HEAD...HEAD^"; then
      error "A secret was found in your commit. If this is a false positive please add '- no-leaks-test' to your commit message."
    fi
}

main "${@}"
