{
  makePythonPypiEnvironment,
  inputs,
  makeTemplate,
  projectPath,
  outputs,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "melts-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    withSetuptools_67_7_2 = true;
    withWheel_0_40_0 = true;
    searchPathsBuild.bin = inputs.nixpkgs.lib.optionals inputs.nixpkgs.stdenv.isDarwin [
      inputs.nixpkgs.clang
      inputs.nixpkgs.darwin.cctools
    ];
  };
in
  makeTemplate {
    replace = {
      __argSrcMelts__ = projectPath "/melts";
    };
    name = "melts-config-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.git
        inputs.nixpkgs.gnutar
        inputs.nixpkgs.openssh
        inputs.nixpkgs.python311
      ];
      pythonPackage = [
        (projectPath "/melts")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        pythonRequirements
        (makeTemplate {
          replace = {
            __argSrcMeltsStatic__ = projectPath "/melts/static";
          };
          name = "melts-secrets-file";
          template = ''
            export MELTS_SECRETS='__argSrcMeltsStatic__/secrets.yaml'
          '';
        })
        outputs."/common/utils/git_self"
      ];
    };
    template = ./template.sh;
  }
