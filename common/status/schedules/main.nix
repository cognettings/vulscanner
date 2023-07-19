{
  inputs,
  makeScript,
  outputs,
  projectPath,
  toFileJson,
  ...
}:
makeScript {
  replace = {
    __argData__ = toFileJson "data.json" (
      import (projectPath "/common/compute/schedule/data.nix")
    );
    __argSopsEnv__ = outputs."/secretsForEnvFromSops/commonStatusDev";
    __argSopsTerraform__ = outputs."/secretsForTerraformFromEnv/commonStatus";
  };
  entrypoint = ./entrypoint.sh;
  name = "schedules-infra";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-18_x
      inputs.nixpkgs.nodePackages_latest.npm
      inputs.nixpkgs.terraform
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };
}
