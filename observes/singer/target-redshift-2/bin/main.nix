{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.redshift_2.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "target-redshift";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "target-redshift \"\${@}\"";
  }
