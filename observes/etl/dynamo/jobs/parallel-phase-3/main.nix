{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-dynamo-parallel-phase-3";
  entrypoint = ./entrypoint.sh;
}
