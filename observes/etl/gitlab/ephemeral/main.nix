{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
    ];
  };
  name = "observes-etl-gitlab-ephemeral";
  entrypoint = ./entrypoint.sh;
}
