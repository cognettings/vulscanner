{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "google-sheets-etl";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "google-sheets-etl \"\${@}\"";
  }
