{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.common.singer_io.root;
in
  makeTemplate {
    name = "observes-common-singer-io-env-runtime";
    searchPaths = {
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-common-singer-io-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
          withSetuptools_67_7_2 = true;
        })
        outputs."/observes/common/purity/env/runtime"
      ];
    };
  }
