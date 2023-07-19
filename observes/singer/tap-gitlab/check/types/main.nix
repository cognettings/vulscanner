{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.gitlab.root;
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
    name = "observes-singer-tap-gitlab-check-types";
    entrypoint = "";
  }
