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
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
    ];
    source = [
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-gitlab";
  entrypoint = ./entrypoint.sh;
}
