{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit (inputs) nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "tap-google-sheets";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ''
      tap-google-sheets "$@"
    '';
  }
