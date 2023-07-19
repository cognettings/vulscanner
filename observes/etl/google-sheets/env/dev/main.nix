{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.dev;
  bins = pkg.bin_deps;
in
  import (projectPath "/observes/common/auto-conf") {
    inherit inputs makeTemplate env bins;
    name = "observes-etl-google-sheets-env-dev";
  }
