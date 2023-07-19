{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.s3.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.dev;
in
  import (projectPath "/observes/common/auto-conf") {
    inherit inputs makeTemplate env;
    bins = [];
    name = "observes-singer-target-s3-env-dev";
  }
