{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.csv.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.dev;
in
  import (projectPath "/observes/common/auto-conf") {
    inherit inputs makeTemplate env;
    name = "observes-singer-tap-csv-env-dev";
    bins = [];
  }
