{
  inputs,
  makeTemplate,
  makePythonPypiEnvironment,
  projectPath,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "sorts-development";
    searchPathsRuntime.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    searchPathsBuild.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    sourcesYaml = ./pypi-sources.yaml;

    withSetuptools_67_7_2 = true;
    withWheel_0_40_0 = true;
  };
in
  makeTemplate {
    name = "sorts-config-development";
    searchPaths = {
      rpath = [
        inputs.nixpkgs.gcc.cc.lib
      ];
      pythonPackage = [
        (projectPath "/sorts/training")
      ];
      source = [pythonRequirements];
    };
  }
