{
  outputs,
  inputs,
  makeScript,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.etl.dynamo.bin}"
    ];
    source = [
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-dynamo-run";
  entrypoint = ./entrypoint.sh;
}
