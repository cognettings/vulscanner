{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.service.success_indicators.bin}"
      outputs."${inputs.observesIndex.tap.formstack.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-formstack";
  entrypoint = ./entrypoint.sh;
}
