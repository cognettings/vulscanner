{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  ...
}: let
  name = "integrates-back-test-functional";
in
  makeScript {
    inherit name;
    replace = {
      __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    };
    searchPaths = {
      bin = [
        inputs.nixpkgs.tokei
        outputs."/integrates/batch"
        outputs."/integrates/db"
      ];
      source = [
        outputs."/integrates/back/env/pypi/functional-tests"
        outputs."/common/utils/sops"
        outputs."/integrates/storage/dev/lib/populate"
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
