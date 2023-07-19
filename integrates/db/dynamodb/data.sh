# shellcheck shell=bash

function get_git_email {
  HOME="${HOME_IMPURE}" git config user.email
}

function prepare_table_data {
  local out="${1}"
  local table_name="${2}"
  local design_path="${3}"
  local emails=("${@:4}")
  local i=0

  : \
    && jq -c \
      "{${table_name}: [.DataModel[].TableFacets[] | select(.FacetName) | {PutRequest: {Item: .TableData[]}}]}" \
      "${design_path}" > "${out}/database-design" \
    && jq "[.${table_name}[] | select(.PutRequest.Item.pk.S == \"USER#__adminEmail__\")]" "${out}/database-design" | jq -n \
      "{\"${table_name}\": [inputs] | add}" > "${out}/temp-user" \
    && for email in "${emails[@]}"; do
      sed "s/__adminEmail__/${email}/g" < "${out}/temp-user" > "${out}/temp-user1" \
        && jq -s "[.[0].${table_name} + .[1].${table_name}]" "${out}/database-design" \
          "${out}/temp-user1" | jq -c "{${table_name}:.[]}" > "${out}/database-design.tmp" \
        && mv "${out}/database-design.tmp" "${out}/database-design"
    done \
    && jq "del(.${table_name}[] | select(.PutRequest.Item.pk.S == \"USER#__adminEmail__\"))" \
      "${out}/database-design" > "${out}/database-design.tmp" \
    && mv "${out}/database-design.tmp" "${out}/database-design" \
    && items_len=$(jq ".${table_name} | length" "${out}/database-design") \
    && echo "${table_name} items qy: ${items_len}" \
    && while [ $((i * 25)) -lt "$items_len" ]; do
      local ilow=$((i * 25)) \
        && local ihigh=$(((i + 1) * 25)) \
        && jq -c "{${table_name}: .${table_name}[$ilow:$ihigh]}" "${out}/database-design" \
          > "${out}/database-design-${table_name}${i}.json" \
        && i=$((i + 1))
    done
}

function main {
  local git_email="${GITLAB_USER_EMAIL:-$(get_git_email)}"
  local out="integrates/db/.data"
  local all_emails_array

  : \
    && rm -rf "${out}" \
    && case "${EXTRA_EMAILS-}" in
      1) mapfile -t all_emails_array <<< "$(grep < __argMailMap__ -Po '(?<=\<).+?(?=\>)' | grep -E '\@fluidattacks.com' | cat - <(echo "$git_email") | sort | uniq)" ;;
      *) all_emails_array=("${git_email}") ;;
    esac \
    && mkdir -p "${out}" \
    && info 'Populating tables from database designs...' \
    && prepare_table_data "${out}" "integrates_vms" "__argIntegratesVmsDbDesign__" "${all_emails_array[@]}" \
    && prepare_table_data "${out}" "fi_async_processing" "__argAsyncProcessingDbDesign__" "${git_email}" \
    && info "Admin email for new DB: ${git_email}" \
    && info "Admin email for old DB: ${git_email}" \
    && for data in "__argDbData__/"*'.json'; do
      sed "s/__adminEmail__/${git_email}/g" "${data}" \
        > "${out}/$(basename "${data}")"
    done
}

main "${@}"
