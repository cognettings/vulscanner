# shellcheck shell=bash

function clone_services_repository {
  local group="${1}"

  : \
    && CI='true' \
      CI_COMMIT_REF_NAME='trunk' \
      melts --init pull-repos --group "${group}"
}

function list_subscriptions {
  local file

  use_git_repo_services >&2 \
    && file="$(mktemp)" \
    && ls -1 groups > "${file}" \
    && popd 1>&2 \
    && echo "${file}"
}

function forces_projects {
  local groups

  mapfile -t groups < "$(list_subscriptions)" \
    && use_git_repo_services >&2 \
    && melts misc --filter-groups-with-forces "${groups[*]}" \
    && popd >&2 \
    || return 1
}

function get_forces_token {
  local group="${1}"

  melts misc --get-forces-token "${group}"
}
