{
  makeSearchPaths,
  outputs,
  ...
}: {
  dev = {
    sorts = {
      source = [
        (makeSearchPaths {
          pythonPackage = [
            "$PWD/sorts/sorts"
          ];
        })
        outputs."/sorts/config/runtime"
      ];
    };
    sortsAssociationRules = {
      source = [
        outputs."/sorts/association-rules/env/dev"
      ];
    };
  };
}
