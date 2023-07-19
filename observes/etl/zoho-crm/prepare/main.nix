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
      outputs."${inputs.observesIndex.tap.zoho_crm.bin}"
    ];
  };
  name = "observes-etl-zoho-crm-prepare";
  entrypoint = ./entrypoint.sh;
}
