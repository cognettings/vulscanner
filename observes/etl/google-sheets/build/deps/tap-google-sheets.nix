{
  lib,
  makes_inputs,
  nixpkgs,
}: let
  root = makes_inputs.projectPath makes_inputs.observesIndex.tap.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit nixpkgs;
  };
  utils = import ./bin_utils.nix;
in
  utils.wrap_binary {
    name = "wrapped-tap-google-sheets";
    binary = "${pkg.pkg}/bin/tap-google-sheets";
    inherit nixpkgs;
  }
