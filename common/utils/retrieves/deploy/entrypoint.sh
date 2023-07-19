# shellcheck shell=bash

function main {
  : && pushd common/utils/retrieves \
    && copy __argSetupRetrievesDevRuntime__ ./node_modules \
    && aws_login "prod_common" "3600" \
    && sops_export_vars __argSecretsProd__ "AZURE_ACCESS_TOKEN" \
    && ./node_modules/.bin/rimraf dist \
    && ./node_modules/.bin/webpack-cli --mode production --config ./webpack/extension.config.js \
    && pushd webview-ui \
    && copy __argSetupRetrievesWebviewRuntime__ ./node_modules \
    && ./node_modules/typescript/bin/tsc -p . \
    && ./node_modules/vite/bin/vite.js build \
    && popd \
    && ./node_modules/.bin/vsce publish \
      -p "${AZURE_ACCESS_TOKEN}" \
      --allow-missing-repository \
      --skip-duplicate \
      minor \
    && popd \
    || return 1
}

main "$@"
