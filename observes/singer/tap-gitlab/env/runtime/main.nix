{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.gitlab.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath;
    inherit (inputs) observesIndex nixpkgs;
  };
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-tap-gitlab-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
