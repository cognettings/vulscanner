# shellcheck shell=bash

function main {
  copy __argAirsFront__ out \
    && aws_login "dev" "3600" \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
    && pushd out \
    && copy __argAirsNpm__ 'node_modules' \
    && install_scripts \
    && lint_npm_deps package.json \
    && ./node_modules/.bin/tsc --noEmit -p tsconfig.json \
    && ./node_modules/.bin/eslint "$(pwd)" \
    && popd \
    && rm -rf out/ \
    || return 1
}

main "${@}"
