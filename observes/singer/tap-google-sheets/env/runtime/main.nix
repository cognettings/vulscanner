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
  makeTemplate {
    name = "observes-tap-google-sheets-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
