{
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "machine-serve-report";
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesSrc__ = projectPath "/integrates/back/src";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/common/utils/async_sqs_consummer/env/pypi/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
