{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.db_snapshot.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-service-db-snapshot-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
