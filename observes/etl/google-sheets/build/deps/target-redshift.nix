{
  lib,
  makes_inputs,
  nixpkgs,
}: let
  root = makes_inputs.projectPath makes_inputs.observesIndex.target.redshift_2.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit (makes_inputs) observesIndex projectPath;
    inherit nixpkgs;
  };
  utils = import ./bin_utils.nix;
in
  utils.wrap_binary {
    name = "wrapped-target-redshift";
    binary = "${pkg.pkg}/bin/target-redshift";
    inherit nixpkgs;
  }
