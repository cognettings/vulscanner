# shellcheck shell=bash

function main {

  export CI_COMMIT_SHA
  export CLUSTER_ENDPOINT
  export CLUSTER_CA_CERTIFICATE
  : \
    && CI_COMMIT_SHA="$(get_commit_from_rev . HEAD)" \
    && CLUSTER_ENDPOINT="$(aws eks --region us-east-1 describe-cluster --name common-k8s | jq -r '.cluster.endpoint')" \
    && CLUSTER_CA_CERTIFICATE="$(aws eks --region us-east-1 describe-cluster --name common-k8s | jq -r '.cluster.certificateAuthority.data')"
}

main "${@}"
