# shellcheck shell=bash

function install_scripts {
  rm -rf node_modules/sharp \
    && npm clean-install --ignore-scripts=false
}
