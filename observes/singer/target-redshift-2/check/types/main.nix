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
  check = pkg.check.types;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-singer-target-redshift-check-types";
    entrypoint = "";
  }
