{
  fromYaml,
  inputs,
  projectPath,
  ...
}: let
  inherit (inputs.nixpkgs) lib;
  schedules = import ./data.nix;
  sizes = fromYaml (
    builtins.readFile (
      projectPath "/common/compute/arch/sizes/data.yaml"
    )
  );
  mapToBatch = name: value:
    lib.nameValuePair
    "schedule_${name}"
    {
      allowDuplicates = true;
      inherit (value) attempts;
      attemptDurationSeconds = value.timeout;
      inherit (value) command;
      definition = value.awsRole;
      inherit (value) environment;
      inherit (value) tags;
      includePositionalArgsInName = false;
      inherit (sizes.${value.size}) memory;
      inherit (value) parallel;
      inherit (sizes.${value.size}) queue;
      vcpus = sizes.${value.size}.cpu;
    };
in {
  computeOnAwsBatch = lib.mapAttrs' mapToBatch schedules;
  imports = [
    ./parse-terraform/makes.nix
    ./test/makes.nix
  ];
}
