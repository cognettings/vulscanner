{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.dynamo.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    entrypoint = ''
      tap-dynamo "$@"
    '';
    searchPaths = {
      bin = [
        env
      ];
    };
    name = "observes-singer-tap-dynamo-bin";
  }
