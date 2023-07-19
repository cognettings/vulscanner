{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.mixpanel.root;
in
  makeTemplate {
    name = "observes-singer-tap-mixpanel-env-runtime";
    searchPaths = {
      rpath = [
        inputs.nixpkgs.gcc.cc.lib
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-singer-tap-mixpanel-env-runtime";
          searchPathsBuild.bin = [inputs.nixpkgs.gfortran];
          sourcesYaml = ./pypi-sources.yaml;
          withCython_0_29_24 = true;
          withSetuptools_67_7_2 = true;
          withWheel_0_40_0 = true;
        })
        outputs."/observes/common/singer-io/env/runtime"
      ];
    };
  }
