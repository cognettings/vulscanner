{
  outputs,
  makeScript,
  ...
}: let
  migrate = outputs."/computeOnAwsBatch/observesCodeEtlMigration2";
in
  makeScript {
    searchPaths = {
      source = [
        outputs."/common/utils/git"
        outputs."/common/utils/sops"
        outputs."/observes/common/list-groups"
      ];
    };
    replace = {
      __argMigrate__ = "${migrate}/bin/${migrate.name}";
    };
    name = "observes-etl-code-upload-migration-fa-hash-range-on-aws";
    entrypoint = ./entrypoint.sh;
  }
