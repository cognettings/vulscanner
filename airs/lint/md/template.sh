# shellcheck shell=bash

function check_md_blog_categories {
  local target="${1}"
  local valid_categories=(
    attacks
    development
    interview
    opinions
    philosophy
    politics
  )

  check_md_tag_exists "${path}" 'category' \
    && grep -Po '(?<=^category: ).+$' "${target}" \
    | sed -E 's|,\s*|\n|g' \
      > list \
    && mapfile -t categories < list \
    && for category in "${categories[@]}"; do
      if ! echo "${valid_categories[*]}" | grep -q "${category}"; then
        abort "[ERROR] Tag: ${category}, is not valid: ${target}, pick one from: ${valid_categories[*]}"
      fi
    done
}

function check_md_blog_patterns {
  local target="${1}"
  declare -A msgs=(
    [source_unsplash]='The cover image is not from unsplash'
    [subtitle_length_limit]='Subtitles must not exceed 55 characters'
    [title_length_limit]='Title must not exceed 35 characters'
  )
  declare -A patterns=(
    [source_unsplash]='(?<=^source: )((?!https://unsplash).*$)'
    [subtitle_length_limit]='(?<=^subtitle: ).{56,}'
    [title_length_limit]='^title: .{36,}'
  )

  for test in "${!patterns[@]}"; do
    if pcregrep -MH "${patterns[${test}]}" "${target}"; then
      abort "[ERROR] ${msgs[${test}]}: ${target}"
    fi
  done
}

function check_md_blog_tags {
  local target="${1}"
  local valid_tags=(
    blue-team
    cloud
    code
    company
    compliance
    credential
    cryptography
    cybersecurity
    devsecops
    exploit
    hacking
    machine-learning
    malware
    pentesting
    red-team
    risk
    security-testing
    social-engineering
    software
    training
    trend
    vulnerability
    vulnserver
    web
    windows
  )

  check_md_tag_exists "${path}" 'tags' \
    && grep -Po '(?<=^tags: ).+$' "${target}" \
    | sed -E 's|,\s*|\n|g' \
      > list \
    && mapfile -t tags < list \
    && for tag in "${tags[@]}"; do
      if ! echo "${valid_tags[*]}" | grep -q "${tag}"; then
        abort "[ERROR] Tag: ${tag}, is not valid: ${target}, pick one from: ${valid_tags[*]}"
      fi
    done
}

function check_md_keywords_casing {
  local target="${1}"
  local msg="Keywords must be: Like This"

  { grep -Po '(?<=^keywords: ).*' "${target}" || true; } \
    | sed -E 's|,\s*|\n|g;s| |\n|g' \
      > list \
    && mapfile -t words < list \
    && for word in "${words[@]}"; do
      if test "$(echo "${word}" | grep -cPv '^[A-ZÁÉÍÓÚÑ]+[a-záéíóúñ]*$')" -gt 0 && ! test "$(grep -cP "^${word}$" __argAcceptedKeywordsFile__)" -gt 0; then
        abort "[ERROR] ${msg}: ${word}: ${target}"
      fi
    done
}

function check_md_lix {
  local target="${1}"
  local max_lix="${2}"
  local msg="Document Lix must be under ${max_lix}"
  local lix

  if check_empty_md "${target}"; then
    return 0
  else
    lix="$(
      sed '/^```/,/^\```/{/^```/!{/^\```/!d}}' "${target}" \
        | sed 's|](https://.*)|]|g' \
        | sed 's|](http://.*)|]|g' \
        | sed 's|<div.*>||g' \
        | sed 's|<p.*>||g' \
        | sed 's|</div.*>||g' \
        | sed 's|</p.*>||g' \
        | sed '/^---/,/^\---/{/^---/!{/^\---/!d}}' \
        | sed 's|Figure [0-9].||g' \
        | sed 's|](../.*)|]|g' \
        | sed 's|](./.*)|]|g' \
        | sed 's|](/.*)|]|g' \
        | style \
        | grep -oP '(?<=Lix: )[0-9]+'
    )" \
      && if test "${lix}" -gt "${max_lix}"; then
        abort "[ERROR] ${msg}, current: ${lix}: ${target}"
      fi
  fi
}

function check_md_main_title {
  local target="${1}"
  local msg='The main title have to be in frontmatter'
  local words

  words="$(
    sed '/^```/,/^\```/{/^```/!{/^\```/!d}}' "${target}" \
      | grep -Pc '^#\s.*$' || true
  )" \
    && check_md_tag_exists "${path}" 'title' \
    && if test "${words}" -gt '0'; then
      abort "[ERROR] ${msg}: ${target}"
    fi
}

function check_md_max_columns {
  local target="${1}"
  local msg='File must be at most 80 columns'

  if grep -v '^:' "${target}" \
    | grep -v '\(link:\|image::\|https://\|http://\)' \
    | grep -P "^.{81,}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_md_min_keywords {
  local target="${1}"
  local min_keywords='5'
  local msg="File must contain at least ${min_keywords} keywords"

  keywords="$(
    { grep -Po '^keywords:.*' "${target}" || true; } \
      | tr ',' '\n' \
      | wc -l
  )" \
    && if test "${keywords}" -lt "${min_keywords}"; then
      abort "[ERROR] ${msg}: ${target}"
    fi
}

function check_md_fluid_attacks_name {
  local target="${1}"
  local msg='Fluid Attacks must be spelled as Fluid Attacks'

  if pcregrep \
    -e '\bfluid attacks' \
    -e '\bFLUID Attacks' \
    -e '\bfluidsignal(?!\.formstack)' \
    -e '\bFluidsignal Group' \
    -e '\bfluid(?!.)' \
    -e '\bFluid(?! Attacks)' \
    -e '\bFLUID(?!.)' \
    -e '\bFLUIDAttacks' \
    "${target}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_md_arm_name {
  local target="${1}"
  local msg='Attack Resistance Management platform must be spelled as Attack Resistance Management platform'

  if pcregrep \
    -e '\bATTACK RESISTANCE MANAGEMENT PLATFORM' \
    -e '\bAttack Resistance Management Platform' \
    -e '\battack resistance management platform' \
    -e '\bATTACKS RESISTANCE MANAGEMENT PLATFORM' \
    -e '\bAttacks Resistance Management Platform' \
    -e '\bAttacks Resistance Management platform' \
    "${target}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_md_words_case {
  local target="${1}"
  local words=(
    'AsciiDoc'
    'bWAPP'
    'CEH'
    'COBOL'
    'C Sharp'
    'GlassFish'
    'HTML'
    'Java'
    'JavaScript'
    'Linux'
    'MySQL'
    'OpenSSL'
    'OSCP'
    'OSWP'
    'OWASP'
    'Red Hat'
    'RPG'
    'Scala'
    'SQLi'
  )
  local msg='Spelling'
  local file_words

  file_words="$(
    sed '/^```/,/^\```/{/^```/!{/^\```/!d}}' "${target}" \
      | sed 's/```.*//'
  )" \
    && for word in "${words[@]}"; do
      case_insensitive="$(echo "${file_words}" | grep -ioP "( |^)${word}( |$)" || true)" \
        && case_sensitive="$(echo "${file_words}" | grep -oP "( |^)${word}( |$)" || true)" \
        && if test "${case_insensitive}" != "${case_sensitive}"; then
          abort "[ERROR] ${msg}: ${word}: ${target}"
        fi \
        || return 1
    done
}

function check_md_patterns {
  local target="${1}"
  declare -A msgs=(
    [image_alt_without_new_lines]='Images must not contain new lines in alt description'
    [caption_forbidden_titles]='Captions must not contain "image", "table" or "figure"'
    [description_char_range]='Descriptions must be in the 50-250 character range'
    [image_alt_name]='Images must have an alt description'
    [local_relative_paths]='Local URLs must use relative paths'
    [numbered_references]='References must be numbered'
    [only_external_images]='Only images uploaded to Cloudinary or an external free source are allowed'
    [only_autonomic_com]='Use autonomicmind.com'
    [slug_ends_with_slash]=':slug: tag must end with a slash /'
    [slug_max_chars]='Slug length has a maximum of 44 characters'
    [title_length_limit]='Title must not exceed 100 characters'
    [title_no_double_quotes]='Do not use double quotes (") in titles'
  )
  declare -A patterns=(
    [image_alt_without_new_lines]='\!\[.*\n.*?\]'
    [caption_forbidden_titles]='^\.(image|table|figure) \d+'
    [description_char_range]='(?<=^description: )(.{0,49}|.{251,})$'
    [image_alt_name]='^\!\[\]'
    [local_relative_paths]='\]\(http(s)?://fluidattacks.com'
    [numbered_references]='^## Referenc.+\n\n[a-zA-Z]'
    [only_external_images]='\!\[.*\]?\(\.\.\/'
    [only_autonomic_com]='autonomicmind.co(?!m)'
    [slug_ends_with_slash]='^slug:.*[a-z0-9-]$'
    [slug_max_chars]='^slug: .{44,}'
    [title_length_limit]='^title: .{100,}'
    [title_no_double_quotes]='^title:{1,6} .*"'
  )

  for test in "${!patterns[@]}"; do
    if pcregrep -MH "${patterns[${test}]}" "${target}"; then
      abort "[ERROR] ${msgs[${test}]}: ${target}"
    fi
  done
}

function check_md_tag_exists {
  local target="${1}"
  local tag="${2}"
  local msg="Tag must exists: ${2}"

  if ! grep -q "^${tag}:" "${target}"; then
    abort "[ERROR] ${msg}: ${target}"
  fi
}

function check_md_word_count {
  local target="${1}"
  local min_words="${2}"
  local max_words="${3}"
  local msg="Document must have between ${min_words} and ${max_words} words"
  local words

  if check_empty_md "${target}"; then
    return 0
  else
    words="$(
      sed '/^```/,/^\```/{/^```/!{/^\```/!d}}' "${target}" \
        | sed 's|](https://.*)|]|g' \
        | sed 's|](http://.*)|]|g' \
        | sed 's|<div.*>||g' \
        | sed 's|<p.*>||g' \
        | sed 's|</div.*>||g' \
        | sed 's|</p.*>||g' \
        | sed '/^---/,/^\---/{/^---/!{/^\---/!d}}' \
        | sed 's|Figure [0-9].||g' \
        | sed 's|](../.*)|]|g' \
        | sed 's|](./.*)|]|g' \
        | sed 's|](/.*)|]|g' \
        | style \
        | grep -oP '[0-9]+(?= words,)'
    )" \
      && if test "${words}" -lt "${min_words}" || test "${words}" -gt "${max_words}"; then
        abort "[ERROR] ${msg}: ${target} ${words}"
      fi
  fi
}

function check_empty_md {
  local target="${1}"
  local empty_msg="Document is empty"
  local md_content
  local metadata

  metadata="$(
    echo -e '---\n---'
  )" \
    && md_content="$(
      sed '/^```/,/^\```/{/^```/!{/^\```/!d}}' "${target}" \
        | sed 's|](https://.*)|]|g' \
        | sed 's|](http://.*)|]|g' \
        | sed 's|<div.*>||g' \
        | sed 's|<p.*>||g' \
        | sed 's|</div.*>||g' \
        | sed 's|</p.*>||g' \
        | sed '/^---/,/^\---/{/^---/!{/^\---/!d}}' \
        | sed 's|Figure [0-9].||g' \
        | sed 's|](../.*)|]|g' \
        | sed 's|](./.*)|]|g' \
        | sed 's|](/.*)|]|g'
    )" \
    && if test -z "${md_content}"; then
      abort "[ERROR] ${empty_msg}"
    elif test "${md_content}" != "${metadata}"; then
      return 1
    fi
}
