# shellcheck shell=bash

function get_keys {
  aws ec2 describe-key-pairs | jq -r ".[][].KeyName" | grep -E "^runner"
}

function get_used_keys {
  aws ec2 describe-instances | jq -r ".[][].Instances[].KeyName" | sort | uniq -u
}

function delete_key {
  local key="${1}"

  : \
    && info "Deleting key: ${key}" \
    && aws ec2 delete-key-pair --key-name "${key}"
}

function delete_keys {
  local keys
  local used_keys

  : \
    && info "Deleting orphan keys" \
    && keys="$(get_keys)" \
    && used_keys="$(get_used_keys)" \
    && while read -r key; do
      if ! grep -q "${key}" <<< "${used_keys}"; then
        delete_key "${key}"
      else
        info "Key is being currently used: ${key}"
      fi
    done <<< "${keys}"
}

function get_running_instances {
  aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running"
}

function get_workers {
  local eval_date
  local older_than="2 days ago"

  : \
    && eval_date="$(date "+%Y-%m-%dT%H:%M.000Z" -d "${older_than}")" \
    && get_running_instances \
    | jq ".Reservations[].Instances[]" \
      | jq 'select(.KeyName // "" | contains("ci-worker"))' \
      | jq --arg eval_date "${eval_date}" 'select(.LaunchTime < $eval_date)' \
      | jq ".InstanceId" \
      | jq --slurp "."
}

function delete_workers {
  local to_delete

  : \
    && info "Deleting orphan workers" \
    && to_delete=$(get_workers) \
    && if echo "${to_delete}" | jq -e ".[]" &> /dev/null; then
      aws ec2 terminate-instances \
        --cli-input-json "{\"InstanceIds\": ${to_delete}, \"DryRun\": false}"
    fi
}

function main {
  : \
    && aws_login "prod_common" "3600" \
    && delete_workers \
    && delete_keys
}

main "${@}"
