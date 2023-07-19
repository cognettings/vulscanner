{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingMelts = gitlabCi.rules.titleMatching "^(all|melts)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMelts
  ];

  gitlabLint = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["melts-small"];
  };
  gitlabTest = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["melts-small"];
  };
in {
  pipelines = {
    melts = {
      gitlabPath = "/melts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/module/melts";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
