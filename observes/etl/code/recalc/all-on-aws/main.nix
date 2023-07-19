{
  outputs,
  makeScript,
  ...
}: let
  recalcGroup = outputs."/computeOnAwsBatch/observesRecalcHash";
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
      __argCodeEtlRecalc__ = "${recalcGroup}/bin/${recalcGroup.name}";
    };
    name = "observes-etl-code-recalc-all-on-aws";
    entrypoint = ./entrypoint.sh;
  }
