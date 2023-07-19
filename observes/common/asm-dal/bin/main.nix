{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.asm_dal.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "asm-dal";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = ''
      asm-dal "$@"
    '';
  }
