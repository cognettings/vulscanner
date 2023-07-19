{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.delighted.root;
in
  makeTemplate {
    name = "observes-singer-tap-delighted-env-runtime";
    searchPaths = {
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-singer-tap-delighted-env-runtime";
          searchPathsBuild.bin = [inputs.nixpkgs.gcc];
          sourcesYaml = ./pypi-sources.yaml;
          withSetuptools_67_7_2 = true;
          withWheel_0_40_0 = true;
        })
        outputs."/observes/common/paginator/env/runtime"
        outputs."/observes/common/singer-io/env/runtime"
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
