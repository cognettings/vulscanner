{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      integrates = {
        searchPaths = {
          source = [
            outputs."/integrates/back/env/pypi/runtime"
            outputs."/integrates/back/env/pypi/unit-tests"
            outputs."/integrates/back/env/pypi/type-stubs"
          ];
        };
        python = "3.11";
        src = "/integrates/back/src";
      };
      integratesBackChartsGenerators = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/charts/generators";
      };
    };
    imports = {
      integrates = {
        config = "/integrates/back/setup.imports.cfg";
        src = "/integrates/back/src";
      };
    };
    modules = {
      integratesBackDeployPermissionsMatrix = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/back/deploy/permissions_matrix";
      };
      integratesBackMigrations = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/back/migrations";
      };
      integratesBackTestUnit = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/unit-tests"
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/back/test/unit/src";
      };
      integratesBackTestE2e = {
        searchPaths.source = [
          outputs."/integrates/web/e2e/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/back/test/e2e/src";
      };
      integratesBackTestFunctional = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/functional-tests"
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/back/test/functional/src";
      };
      integratesBackChartsCollector = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/charts/collector";
      };
      integratesBackCharts = {
        searchPaths.source = [
          outputs."/integrates/back/env/pypi/runtime"
          outputs."/integrates/back/charts/pypi"
          outputs."/integrates/back/env/pypi/type-stubs"
        ];
        python = "3.11";
        src = "/integrates/charts";
      };
    };
  };
}
