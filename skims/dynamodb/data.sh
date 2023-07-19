# shellcheck shell=bash

function prepare_table_data {
  local out="${1}"
  local table_name="${2}"
  local design_path="${3}"
  local i=0

  : \
    && jq -c \
      "{${table_name}: [.DataModel[].TableFacets[] | select(.FacetName) | {PutRequest: {Item: .TableData[]}}]}" \
      "${design_path}" > "${out}/database-design" \
    && items_len=$(jq ".${table_name} | length" "${out}/database-design") \
    && echo "${table_name} items qy: ${items_len}" \
    && while [ $((i * 25)) -lt "$items_len" ]; do
      local ilow=$((i * 25)) \
        && local ihigh=$(((i + 1) * 25)) \
        && jq -c "{${table_name}: .${table_name}[$ilow:$ihigh]}" \
          "${out}/database-design" \
          > "${out}/database-design-${table_name}${i}.json" \
        && i=$((i + 1))
    done
}

function main {
  local out="skims/dynamodb/.data"

  : \
    && rm -rf "${out}" \
    && mkdir -p "${out}" \
    && echo '[INFO] Populating tables from database designs...' \
    && prepare_table_data "${out}" "skims_sca" "__argSkimsDbDesign__"
}

main "${@}"
