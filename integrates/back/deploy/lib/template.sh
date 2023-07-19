# shellcheck shell=bash

function is_int {
  local input="${1}"
  local regex="^[0-9]+$"

  if [[ ${input} =~ ${regex} ]]; then
    return 0
  else
    return 1
  fi
}

function hpa_desired_replicas {
  local name="${1}"
  local namespace="${2}"

  kubectl get hpa -n "${namespace}" -o yaml \
    | yq -r ".items[] | select(.metadata.name==\"${name}\") | .status.desiredReplicas"
}

function hpa_replicas {
  local name="${1}"
  local namespace="${2}"
  local replicas

  : \
    && replicas="$(hpa_desired_replicas "${name}" "${namespace}")" \
    && if is_int "${replicas}" && test "${replicas}" != "0"; then
      echo "${replicas}"
    else
      echo 1
    fi
}

function apply_manifest {
  local manifest="${1}"

  : \
    && info "Applying: ${manifest}" \
    && envsubst -no-unset -no-empty -i "${manifest}" | kubectl apply -f -
}

function b64 {
  echo -n "${1}" | base64 --wrap=0
}

function report_deployment_checkly {
  local product="${1}"

  : \
    && info "Announcing deployment to Checkly" \
    && curl "https://api.checklyhq.com/check-groups/${CHECKLY_CHECK_ID}/trigger/${CHECKLY_TRIGGER_ID}?deployment=true&repository=${product}&sha=${CI_COMMIT_SHA}" \
      --request "GET"
}

function report_deployment {
  local product="${1}"

  report_deployment_checkly "${product}"
}

function rollout {
  local name="${1}"
  local namespace="${2}"

  : \
    && info "Rolling out update" \
    && kubectl rollout status \
      "deploy/${name}" \
      -n "${namespace}" \
      --timeout="30m"
}
