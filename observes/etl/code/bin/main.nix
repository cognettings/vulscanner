{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) nixpkgs observesIndex;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "observes-etl-code";
    searchPaths = {
      bin = [
        env
        inputs.nixpkgs.git
      ];
    };
    entrypoint = ''
      observes-etl-code "$@"
    '';
  }
