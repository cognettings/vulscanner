# shellcheck shell=bash

function job_code_upload_all_groups {
  local groups_file
  export AWS_DEFAULT_REGION="us-east-1"

  groups_file=$(mktemp)

  list_groups "${groups_file}" \
    && while read -r group; do
      echo "[INFO] Submitting: ${group}" \
        && __argCodeEtlUpload__ "${group}" \
        || return 1
    done < "${groups_file}"
}

job_code_upload_all_groups
