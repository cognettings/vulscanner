{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.dynamo.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.s3.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  replace = {
    __argMultifileConf__ = ./multifile_conf.json;
  };
  name = "observes-etl-dynamo-parallel-phase-1";
  entrypoint = ./entrypoint.sh;
}
