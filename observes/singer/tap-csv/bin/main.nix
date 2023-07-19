{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.csv.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "tap-csv";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "tap-csv \"\${@}\"";
  }
