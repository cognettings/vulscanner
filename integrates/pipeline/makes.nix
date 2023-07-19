{
  gitlabCi,
  inputs,
  lib,
  projectPath,
  ...
}: let
  chartsTemplate = {
    after_script = ["cp ~/.cache/makes/provenance-* ."];
    artifacts = {
      expire_in = "1 week";
      paths = [
        "integrates/charts"
        "provenance-*"
      ];
      when = "on_success";
    };
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    stage = "analytics";
  };
  listDirectories = path: let
    content = builtins.readDir (projectPath path);
    directories =
      lib.filterAttrs
      (key: value: value == "directory" && !lib.hasPrefix "__" key)
      content;
  in
    builtins.attrNames directories;
  backSrcModules = listDirectories "/integrates/back/src";
  chartsSrcModules = listDirectories "/integrates/charts/generators";
  functionalTests =
    builtins.map (test: [test])
    (listDirectories "/integrates/back/test/functional/src");
  gitlabJobDependencies = 40;
  functionalCoverageCombine =
    builtins.genList
    (x: [(builtins.toString (x + 1))])
    (
      builtins.ceil
      ((builtins.length functionalTests) / (gitlabJobDependencies * 1.0))
    );
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|integrates)";
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDevAndProd = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabDeployEphemeralRule = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    # Integrates and forces only need ephemeral in dev
    gitlabBranchNotTrunk
    (gitlabCi.rules.titleMatching "^(all|integrates)")
  ];
  gitlabDeployAppDev = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "deploy-app";
    tags = ["integrates-small"];
  };
  gitlabDeployAppDevInterested = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabDeployEphemeralRule;
    stage = "deploy-app";
    tags = ["integrates-small"];
  };
  gitlabDeployAppProdResourceGroup = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["integrates-small"];
  };
  gitlabDeployForcesProd = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["integrates-small"];
  };
  gitlabDeployInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["integrates-small"];
  };
  gitlabExternal = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDevAndProd;
    stage = "external";
    tags = ["integrates-small"];
  };
  gitlabLint = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["integrates-small"];
  };
  gitlabPostDeployDev = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = ["integrates-small"];
  };
  gitlabTestDevAndProd = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDevAndProd;
    stage = "test-code";
    tags = ["integrates-small"];
  };
  gitlabTestInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["integrates-small"];
  };
  inherit (inputs.nixpkgs) lib;
in {
  pipelines = {
    integratesDefault = {
      gitlabPath = "/integrates/pipeline/default.yaml";
      jobs =
        [
          {
            output = "/deployTerraform/integratesInfra";
            gitlabExtra = gitlabDeployInfra;
          }
          {
            output = "/integrates/back/authz-matrix";
            gitlabExtra =
              gitlabDeployAppDev
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/back/deploy/permissions_matrix"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                };
              };
          }
          {
            output = "/deployContainerImage/forcesDev";
            gitlabExtra =
              gitlabDeployAppDevInterested
              // {
                image = "ghcr.io/fluidattacks/makes/amd64:latest";
                tags = ["common-small-x86"];
              };
          }
          {
            output = "/deployContainerImage/forcesProd";
            gitlabExtra =
              gitlabDeployForcesProd
              // {
                image = "ghcr.io/fluidattacks/makes/amd64:latest";
                tags = ["common-small-x86"];
              };
          }
          {
            output = "/integrates/back/deploy/dev";
            gitlabExtra =
              gitlabDeployAppDevInterested
              // {
                environment = {
                  name = "development/$CI_COMMIT_REF_SLUG";
                  url = "https://$CI_COMMIT_REF_SLUG.app.fluidattacks.com";
                };
              };
          }
          {
            output = "/integrates/back/deploy/prod";
            gitlabExtra =
              gitlabDeployAppProdResourceGroup
              // {
                environment = {
                  name = "production";
                  url = "https://app.fluidattacks.com";
                };
              };
          }
          {
            output = "/integrates/forces/test";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          {
            args = ["changes_db"];
            output = "/integrates/back/test/unit";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          {
            args = ["not_changes_db"];
            output = "/integrates/back/test/unit";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          rec {
            args = ["dev" (toString gitlabExtra.parallel) "gitlab"];
            output = "/integrates/charts/documents";
            gitlabExtra =
              chartsTemplate
              // {
                parallel = 7;
                rules = gitlabOnlyDev;
                tags = ["integrates-small"];
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          {
            output = "/integrates/coverage";
            gitlabExtra =
              gitlabExternal
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/build"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                  reports = {
                    coverage_report = {
                      coverage_format = "cobertura";
                      path = "integrates/coverage.xml";
                    };
                  };
                };
                coverage = "/(?i)total.*? (100(?:\\.0+)?\\%|[1-9]?\\d(?:\\.\\d+)?\\%)$/";
                needs =
                  [
                    "/integrates/back/test/unit__changes_db"
                    "/integrates/back/test/unit__not_changes_db"
                  ]
                  ++ (
                    builtins.map
                    (test: "/integrates/coverage/combine__${
                      builtins.elemAt
                      test
                      0
                    }")
                    functionalCoverageCombine
                  );
              };
          }
          {
            output = "/integrates/front/deploy/dev";
            gitlabExtra = gitlabDeployAppDev;
          }
          {
            output = "/integrates/front/deploy/prod";
            gitlabExtra = gitlabDeployAppProdResourceGroup;
          }
          {
            output = "/integrates/front/lint";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/front/test";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                image = "ghcr.io/fluidattacks/makes/amd64:latest";
                parallel = 5;
                tags = ["common-small-x86"];
              };
          }
          {
            output = "/integrates/back/lint/asyncdef";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/back/lint/schema";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/back/lint/schema/deprecations";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/back/lint/charts";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/secrets/lint";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/back/test/load";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                ];
              };
          }
          {
            output = "/integrates/web/e2e";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                artifacts = {
                  paths = [
                    "integrates/back/test/e2e/src/screenshots"
                  ];
                  expire_in = "1 day";
                  when = "on_failure";
                };
                needs = [
                  "/integrates/back/deploy/dev"
                  "/integrates/front/deploy/dev"
                ];
                parallel = 5;
              };
          }
          {
            output = "/integrates/web/forces";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                ];
                retry = 2;
              };
          }
          {
            output = "/lintPython/module/integratesBackCharts";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackChartsCollector";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/dirOfModules/streams";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/integrates";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackDeployPermissionsMatrix";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesJobsCloneRoots";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesJobsExecuteMachine";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackMigrations";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackTestE2e";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackTestFunctional";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackTestUnit";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/forces";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/forcesTests";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintTerraform/integratesInfra";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/pipelineOnGitlab/integratesDefault";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/pipelineOnGitlab/integratesBackTestFunctional";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/securePythonWithBandit/integratesBack";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/testTerraform/integratesInfra";
            gitlabExtra = gitlabTestInfra;
          }
        ]
        ++ (
          builtins.map
          (args: {
            inherit args;
            output = "/integrates/coverage/combine";
            gitlabExtra =
              gitlabExternal
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                };
                needs =
                  builtins.map
                  (test: "/integrates/back/test/functional__${
                    builtins.elemAt
                    test
                    0
                  }")
                  (
                    lib.lists.sublist
                    (
                      (
                        (
                          lib.strings.toInt
                          (builtins.elemAt args 0)
                        )
                        - 1
                      )
                      * gitlabJobDependencies
                    )
                    gitlabJobDependencies
                    functionalTests
                  );
              };
          })
          functionalCoverageCombine
        )
        ++ (
          builtins.map
          (module: {
            output = "/lintPython/dirOfModules/integrates/${module}";
            gitlabExtra = gitlabLint;
          })
          backSrcModules
        )
        ++ (
          builtins.map
          (module: {
            output = "/lintPython/dirOfModules/integratesBackChartsGenerators/${module}";
            gitlabExtra = gitlabLint;
          })
          chartsSrcModules
        );
    };
    integratesBackTestFunctional = {
      gitlabPath = "/integrates/pipeline/back-test-functional.yaml";
      jobs =
        builtins.map
        (args: {
          inherit args;
          output = "/integrates/back/test/functional";
          gitlabExtra =
            gitlabTestDevAndProd
            // {
              after_script = ["cp ~/.cache/makes/provenance-* ."];
              artifacts = {
                paths = [
                  "integrates/.coverage*"
                  "provenance-*"
                ];
                expire_in = "1 day";
                when = "on_success";
              };
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
        })
        functionalTests;
    };
  };
}
