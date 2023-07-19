{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.etl.code.bin}"
      outputs."${inputs.observesIndex.service.success_indicators.bin}"
      outputs."/melts"
      inputs.nixpkgs.coreutils
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-code-upload";
  entrypoint = ./entrypoint.sh;
}
