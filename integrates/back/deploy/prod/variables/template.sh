# shellcheck shell=bash

function main {

  export CI_COMMIT_SHA
  export CLUSTER_ENDPOINT
  export CLUSTER_CA_CERTIFICATE
  export CI_COMMIT_REF_NAME
  export REPLICAS
  export UUID

  export KUBECONFIG="/home/nixos/.kube/config"
  : \
    && CI_COMMIT_SHA="$(get_commit_from_rev . HEAD)" \
    && CI_COMMIT_REF_NAME="$(get_abbrev_rev . HEAD)" \
    && CLUSTER_ENDPOINT="$(aws eks --region us-east-1 describe-cluster --name common-k8s | jq -r '.cluster.endpoint')" \
    && CLUSTER_CA_CERTIFICATE="$(aws eks --region us-east-1 describe-cluster --name common-k8s | jq -r '.cluster.certificateAuthority.data')" \
    && REPLICAS="$(hpa_replicas "integrates-${CI_COMMIT_REF_NAME}" "prod-integrates")" \
    && UUID="$(uuidgen)"

}

main "${@}"
