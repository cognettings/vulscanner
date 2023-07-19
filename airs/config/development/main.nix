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
      __argAirsSecrets__ = projectPath "/airs/secrets";
      __argAirsNpm__ = outputs."/airs/npm";
    };
    entrypoint = ./entrypoint.sh;
    name = "airs-config-development";
    searchPaths = {
      rpath = [
        libcPackage
      ];
      bin =
        [
          inputs.nixpkgs.utillinux
        ]
        ++ inputs.nixpkgs.lib.optionals inputs.nixpkgs.stdenv.isDarwin [
          (inputs.makeImpureCmd {
            cmd = "open";
            path = "/usr/bin/open";
          })
        ];
      source = [
        outputs."/common/utils/aws"
        outputs."/airs/npm/env"
        outputs."/airs/npm/runtime"
        outputs."/common/utils/sops"
      ];
    };
  }
