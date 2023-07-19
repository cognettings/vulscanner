{
  inputs,
  isLinux,
  isDarwin,
  makeScript,
  outputs,
  projectPath,
  ...
}: let
  libcPackage =
    if isDarwin
    then inputs.nixpkgs.clang
    else inputs.nixpkgs.musl;
in
  makeScript {
    replace = {
      __argAirsNpm__ = outputs."/airs/npm";
      __argAirsSecrets__ = projectPath "/airs/secrets";
    };
    entrypoint = ./entrypoint.sh;
    name = "airs-build";
    searchPaths = {
      rpath = [libcPackage];
      bin = [
        inputs.nixpkgs.findutils
        inputs.nixpkgs.gnugrep
        inputs.nixpkgs.gnused
        inputs.nixpkgs.nodejs-18_x
        inputs.nixpkgs.utillinux
      ];
      source = [
        outputs."/common/utils/aws"
        outputs."/airs/npm/runtime"
        outputs."/airs/npm/env"
        outputs."/common/utils/sops"
      ];
    };
  }
