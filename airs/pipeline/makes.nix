{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingAirs = gitlabCi.rules.titleMatching "^(all|airs)";

  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabLintJob = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["airs-small"];
  };
in {
  pipelines = {
    airs = {
      gitlabPath = "/airs/gitlab-ci.yaml";
      jobs = [
        {
          image = "ghcr.io/fluidattacks/makes/amd64:latest";
          output = "/airs/eph";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "deploy-app";
            tags = ["airs-large-x86"];
          };
        }
        {
          image = "ghcr.io/fluidattacks/makes/amd64:latest";
          output = "/airs/prod";
          gitlabExtra = {
            rules = gitlabOnlyProd;
            stage = "deploy-app";
            tags = ["airs-large-x86"];
          };
        }
        {
          output = "/airs/lint/code";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/airs/lint/content";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/airs/lint/styles";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/lintMarkdown/airs";
          gitlabExtra = gitlabLintJob;
        }
        {
          image = "ghcr.io/fluidattacks/makes/arm64:latest";
          output = "/deployTerraform/airsInfra";
          gitlabExtra = {
            resource_group = "$CI_JOB_NAME";
            rules = gitlabOnlyProd;
            stage = "deploy-infra";
            tags = ["airs-small"];
          };
        }
        {
          output = "/lintTerraform/airsInfra";
          gitlabExtra = gitlabLintJob;
        }
        {
          image = "ghcr.io/fluidattacks/makes/arm64:latest";
          output = "/testTerraform/airsInfra";
          gitlabExtra = {
            resource_group = "$CI_JOB_NAME";
            rules = gitlabOnlyDev;
            stage = "test-infra";
            tags = ["airs-small"];
          };
        }
      ];
    };
  };
}
