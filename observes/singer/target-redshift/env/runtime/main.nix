{
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.target.redshift.root;
in
  makeTemplate {
    name = "observes-singer-target-redshift-env-runtime";
    searchPaths = {
      pythonPackage = [
        self
      ];
      source = [
        outputs."${inputs.observesIndex.target.redshift.env.runtime}/python"
        outputs."/observes/common/postgres-client/env/runtime"
        outputs."/observes/common/singer-io/env/runtime"
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
