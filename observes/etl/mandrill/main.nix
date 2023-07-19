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
      outputs."${inputs.observesIndex.tap.mandrill.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
    ];
    source = [
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-mandrill";
  entrypoint = ./entrypoint.sh;
}
