{
  inputs,
  makeTemplate,
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
  makeTemplate {
    name = "observes-singer-target-redshift-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
