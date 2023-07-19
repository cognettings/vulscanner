{gitlabCi, ...}: let
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingSorts = gitlabCi.rules.titleMatching "^(all|sorts)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];

  gitlabDeployInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["sorts-small"];
  };
  gitlabLint = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["sorts-small"];
  };
  gitlabTest = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["sorts-small"];
  };
  gitlabTestInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["sorts-small"];
  };
in {
  pipelines = {
    sorts = {
      gitlabPath = "/sorts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/sorts";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintPython/dirOfModules/sorts";
          gitlabExtra =
            gitlabLint
            // {
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
        }
        {
          output = "/lintPython/imports/sorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/sortsTests";
          gitlabExtra =
            gitlabLint
            // {
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
        }
        {
          output = "/lintPython/module/sortsTraining";
          gitlabExtra =
            gitlabLint
            // {
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
        }
        {
          output = "/lintTerraform/sorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/sorts/association-rules/check/types";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/sorts/extract-features";
          gitlabExtra = {
            image = "ghcr.io/fluidattacks/makes/arm64:latest";
            interruptible = false;
            parallel = 20;
            rules = [
              gitlabCi.rules.schedules
              (gitlabCi.rules.varIsDefined "sorts_extract_features")
              gitlabCi.rules.always
            ];
            stage = "pre-build";
            tags = ["sorts-large"];
          };
        }
        {
          output = "/sorts/merge-features";
          gitlabExtra = {
            image = "ghcr.io/fluidattacks/makes/arm64:latest";
            interruptible = false;
            needs = ["/sorts/extract-features"];
            rules = [
              gitlabCi.rules.schedules
              (gitlabCi.rules.varIsDefined "sorts_extract_features")
              gitlabCi.rules.always
            ];
            stage = "build";
            tags = ["sorts-large"];
          };
        }
        {
          output = "/testPython/sorts";
          gitlabExtra =
            gitlabTest
            // {
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
        }
        {
          output = "/testTerraform/sorts";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
