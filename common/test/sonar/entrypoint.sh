# shellcheck shell=bash

function main {
  export SONAR_HOST_URL="https://sonarcloud.io/"
  export SONAR_USER_HOME=".sonar"

  : \
    && aws_login "dev" "3600" \
    && sops_export_vars "common/secrets/dev.yaml" \
      "SONAR_TOKEN" \
    && sonar-scanner
}

main "${@}"
