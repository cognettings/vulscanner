{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit (inputs) nixpkgs;
  };
  env = pkg.env.runtime;
in
  import (projectPath "/observes/common/auto-conf") {
    inherit inputs makeTemplate env;
    bins = [];
    name = "observes-tap-google-sheets-env-dev";
  }
