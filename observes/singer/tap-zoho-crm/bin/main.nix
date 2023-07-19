{
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.zoho_crm.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeScript {
    name = "tap-zoho-crm";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "tap-zoho-crm \"\${@}\"";
  }
