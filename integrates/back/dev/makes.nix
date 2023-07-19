{
  makeSearchPaths,
  makeTemplate,
  outputs,
  ...
}: {
  dev = {
    integratesBack = {
      source = [
        (makeTemplate {
          name = "integrates-dev";
          replace = {
            __argIntegratesBackEnv__ = outputs."/integrates/back/env";
          };
          template = ''
            require_env_var AWS_ACCESS_KEY_ID
            require_env_var AWS_SECRET_ACCESS_KEY
            source __argIntegratesBackEnv__/template dev
          '';
        })
        (makeSearchPaths {
          pythonPackage = [
            "$PWD/integrates"
            "$PWD/integrates/back/src"
            "$PWD/common/utils/bugsnag/client"
            "$PWD/common/utils/git_self/src"
          ];
        })
        outputs."/integrates/back/charts/pypi"
        outputs."/integrates/back/env/pypi/unit-tests"
      ];
    };
  };
}
