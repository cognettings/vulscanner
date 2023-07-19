# shellcheck shell=bash

function main {
  local out="airs/front"

  : \
    && pushd "${out}" \
    && aws_login "dev" "3600" \
    && sops_export_vars __argAirsSecrets__/dev.yaml \
      CLOUDINARY_API_SECRET \
      CLOUDINARY_API_KEY \
      CLOUDINARY_CLOUD_NAME \
      GATSBY_ALGOLIA_APP_ID \
      GATSBY_ALGOLIA_SEARCH_KEY \
      ALGOLIA_ADMIN_KEY \
      GATSBY_AUTH0_DOMAIN \
      GATSBY_AUTH0_CLIENT_ID \
      GATSBY_AUTH0_CALLBACK \
    && if test -n "${CI-}" && test "${CI_COMMIT_REF_NAME}" != "trunk"; then
      sed -i "s|pathPrefix: '/front'|pathPrefix: '/${CI_COMMIT_REF_NAME}'|g" gatsby-config.js \
        && sed -i "s|https://fluidattacks.com|https://web.eph.fluidattacks.com/${CI_COMMIT_REF_NAME}|g" gatsby-config.js
    fi \
    && copy __argAirsNpm__ 'node_modules' \
    && install_scripts \
    && if test -n "${CI-}" && test "${CI_COMMIT_REF_NAME}" != "trunk"; then
      npm run build:eph
    else
      npm run build
    fi \
    && npm run build-storybook -- -o public/storybook \
    && find content/ -name "*.adoc" -type f -delete \
    && find content/ -type d -empty -delete \
    && mv content/pages/advisories/ content/ \
    && mv content/pages/careers/ content/ \
    && copy content public \
    && rm -rf content \
    && popd \
    || return 1
}

main "${@}"
