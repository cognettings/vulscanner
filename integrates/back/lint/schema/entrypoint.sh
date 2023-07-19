# shellcheck shell=bash

function lint_schema {
  local schema_path="${1}"

  : \
    && graphql-schema-linter \
      --except 'relay-page-info-spec' \
      "${schema_path}" \
    || return 1
}

function lint_breaking_changes {
  local schema_path="${1}"

  : \
    && git fetch origin trunk \
    && graphql-inspector diff \
      "git:origin/trunk:${schema_path}" \
      "git:HEAD:${schema_path}" \
      --rule suppressRemovalOfDeprecatedField \
    || return 1
}

function main {
  local schema_path="integrates/back/src/api/**/*.graphql"
  local assumption_flag="- assume-api-breaking-change"

  : \
    && lint_schema "${schema_path}" \
    && if ! lint_breaking_changes "${schema_path}"; then
      if [[ ${CI_COMMIT_MESSAGE} == *"${assumption_flag}"* ]]; then
        warn "Assuming the risk of a breaking change. Good luck, see you in help!" \
          && return 0
      else
        info "Changes to the API schema must be backward-compatible per our policy:" \
          && info "https://docs.fluidattacks.com/development/products/integrates#public-oath" \
          && info "Review your changes to ensure compatibility or alternatively assume the risk" \
          && info "by including ${assumption_flag} in the commit message." \
          && info "If you haven't changed any .graphql files, this branch may be outdated." \
          && return 1
      fi
    fi \
    || return 1
}

main "${@}"
