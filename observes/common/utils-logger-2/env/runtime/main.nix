{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.utils_logger_2.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-utils-logger-2-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
