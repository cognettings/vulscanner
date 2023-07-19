{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-scheduler";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python311
      outputs."/skims"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/skims/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
