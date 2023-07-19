{
  inputs,
  makeTemplate,
  projectPath,
  fetchNixpkgs,
  ...
}: let
  root = projectPath inputs.observesIndex.service.db_migration.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.runtime;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-service-db-migration-env-runtime";
  }
