# shellcheck shell=bash

function main {
  export CI_COMMIT_REF_NAME='__CI_COMMIT_REF_NAME__'
  export CI_COMMIT_SHA='__CI_COMMIT_SHA__'
  export CI_COMMIT_SHORT_SHA='__CI_COMMIT_SHORT_SHA__'
  export INTEGRATES_DEPLOYMENT_DATE='__INTEGRATES_DEPLOYMENT_DATE__'

  mkdir -p "${out}/output" \
    && copy "${envIntegratesFront}" front \
    && pushd front \
    && copy "${envSetupIntegratesFrontDevRuntime}" node_modules \
    && npm run build \
    && npm run build-storybook -- -o ../app/storybook \
    && popd \
    && mkdir -p app/static/external/C3 \
    && copy "${envExternalC3}" app/static/external/C3 \
    && copy "${envIntegratesBackAppTemplates}" app/static \
    && echo "${out}/output/app" \
    && mv app "${out}/output/app" \
    || return 1
}

main "${@}"
