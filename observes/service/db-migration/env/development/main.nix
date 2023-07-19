{
  inputs,
  makeTemplate,
  projectPath,
  fetchNixpkgs,
  ...
}: let
  root = projectPath inputs.observesIndex.service.db_migration.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  import (projectPath "/observes/common/auto-conf") {
    inherit inputs makeTemplate env;
    bins = [];
    name = "observes-service-db-migration-env-development";
  }
