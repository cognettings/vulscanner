# shellcheck shell=bash

function rebase {
  local origin="origin"
  local trunk="trunk"

  if test -z "${CI-}"; then
    : && info "Rebasing your local branch with ${origin}/${trunk}" \
      && HOME="${HOME_IMPURE}" git pull --rebase --autostash "${origin}" "${trunk}"
  fi
}

function max_commits {
  local trunk="trunk"
  local max_commits="1"
  local commits

  : && info "Testing max commits" \
    && git fetch origin "${trunk}" &> /dev/null \
    && commits="$(git rev-list --count "remotes/origin/${trunk}..HEAD")" \
    && if test "${commits}" -gt "${max_commits}"; then
      error \
        "You are ${commits} commit(s) ahead of ${trunk}." \
        "Max allowed: ${max_commits}"
    fi
}

function git_author_syntax {
  local regex='^[A-Z][a-z]+ [A-Z][a-z]+$'
  local author

  : && info "Testing author syntax" \
    && author="$(git --no-pager log --format='%an' HEAD^!)" \
    && if ! [[ ${author} =~ ${regex} ]]; then
      error \
        "Commit author is '${author}'," \
        "Please make sure to use the following syntax:" \
        "Capitalized name, space and capitalized last name." \
        "(avoid accents and ñ)." \
        "For example: Aureliano Buendia." \
        "You can change your git user by running:" \
        "git config --global user.name 'Aureliano Buendia'"
    fi
}

function max_deltas {
  local max_deltas="150"
  local commit_msg
  local changes
  local deltas

  : && info "Testing max deltas" \
    && commit_msg="$(git --no-pager log HEAD^..HEAD)" \
    && if echo "${commit_msg}" | grep -q -- "- no-deltas-test"; then
      return 0
    fi \
    && changes="$(git --no-pager diff --numstat HEAD^..HEAD)" \
    && deltas="$(echo "${changes}" | awk '{deltas+=$1+$2} END {printf "%s\n", deltas}')" \
    && if test "${deltas}" -gt "${max_deltas}"; then
      error \
        "Commit has ${deltas} deltas." \
        "Max allowed: ${max_deltas}." \
        "Use '- no-deltas-test' if needed."
    fi
}

function modified_directories {
  local files
  local name

  : && info "Testing modified directories" \
    && files=$(mktemp) \
    && git diff-tree --no-commit-id --name-only -r HEAD > "${files}" \
    && name="$(git show --pretty=format:%s -s HEAD)" \
    && IFS="$(printf \\)" read -r commit_name _ <<< "${name}" \
    && if [ "${commit_name[0]}" == "all" ]; then
      return 0
    fi \
    && if grep "/" "${files}" | grep -Ev "^\." | grep -Ev "^${commit_name[0]}"; then
      error "File(s) do not match the product name in the commit title"
    fi
}

function main {
  : && rebase \
    && max_commits \
    && git_author_syntax \
    && max_deltas \
    && modified_directories
}

main "${@}"
