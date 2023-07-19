# shellcheck shell=bash

function main {
  : \
    && { DAEMON=true dynamodb & } \
    && { DAEMON=true opensearch & } \
    && wait \
    && if [ "${DAEMON-}" = "true" ]; then
      { integrates-streams consumer dev & }
    else
      integrates-streams consumer dev
    fi

}

main "${@}"
