{
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "machine-report";
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argMain__ = projectPath "/integrates/jobs/report_machine/main.py";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
