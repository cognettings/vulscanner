{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-sonar";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.sonar-scanner-cli
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
}
