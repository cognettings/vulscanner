{
  inputs,
  makeScript,
  projectPath,
  toFileYaml,
  ...
}: let
  config = toFileYaml "mprocs.yaml" {
    procs = {
      back.cmd = ["m" "." "/integrates/back" "dev"];
      db.cmd = ["m" "." "/integrates/db"];
      front.cmd = ["m" "." "/integrates/front"];
      storage.cmd = ["m" "." "/integrates/storage/dev"];
    };
  };
  makes = let
    lock = projectPath "/makes.lock.nix";
    src = (import lock).makesSrc;
  in
    import src {};
in
  makeScript {
    entrypoint = "mprocs --config __argConfig__";
    name = "integrates";
    replace.__argConfig__ = config;
    searchPaths.bin = [
      inputs.nixpkgs.mprocs
      makes
    ];
  }
