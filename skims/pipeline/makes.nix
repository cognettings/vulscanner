{
  gitlabCi,
  inputs,
  lib,
  projectPath,
  ...
}: let
  listDirectories = path: let
    content = builtins.readDir (projectPath path);
    directories =
      lib.filterAttrs
      (key: value: value == "directory" && !lib.hasPrefix "__" key)
      content;
  in
    builtins.attrNames directories;
  skimsSrcModules = listDirectories "/skims/skims";
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabJobDependencies = 40;
  gitlabTitleMatchingSkims = gitlabCi.rules.titleMatching "^(all|skims)";
  skimsTests =
    builtins.map (test: [test])
    inputs.skimsTestPythonCategoriesCI;
  functionalCoverageCombine =
    builtins.genList
    (x: [(builtins.toString (x + 1))])
    (
      builtins.ceil
      ((builtins.length skimsTests) / (gitlabJobDependencies * 1.0))
    );

  gitlabOnlyTrunk = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDevAndTrunk = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];

  gitlabDeployInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyTrunk;
    stage = "deploy-infra";
    tags = ["skims-small"];
  };
  gitlabLint = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["skims-small"];
  };
  gitlabTest = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDevAndTrunk;
    stage = "test-code";
    tags = ["skims-small"];
  };
  gitlabTestInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["skims-small"];
  };
in {
  pipelines = {
    skims = {
      gitlabPath = "/skims/gitlab-ci.yaml";
      jobs =
        [
          {
            output = "/deployTerraform/skims";
            gitlabExtra = gitlabDeployInfra;
          }
          {
            output = "/lintPython/imports/skims";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/skimsTest";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintTerraform/skims";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/pipelineOnGitlab/skims";
            gitlabExtra = gitlabLint;
          }
        ]
        ++ (
          builtins.map
          (module: {
            output = "/lintPython/dirOfModules/skims/${module}";
            gitlabExtra = gitlabLint;
          })
          skimsSrcModules
        )
        ++ (builtins.map
          (category: {
            output = "/testPython/skims@${category}";
            gitDepth =
              if category == "unittesting"
              then 0
              else 1;
            gitlabExtra =
              gitlabTest
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "skims/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
              };
          })
          inputs.skimsTestPythonCategoriesCI)
        ++ (builtins.map
          (args: {
            inherit args;
            output = "/skims/coverage/combine";
            gitlabExtra =
              gitlabTest
              // {
                after_script = ["cp ~/.cache/makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "skims/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                };
                needs =
                  builtins.map
                  (test: "/testPython/skims@${test}")
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
                    inputs.skimsTestPythonCategoriesCI
                  );
                stage = "post-deploy";
              };
          })
          functionalCoverageCombine)
        ++ [
          {
            output = "/skims/coverage";
            gitlabExtra =
              gitlabTest
              // {
                needs =
                  builtins.map
                  (test: "/skims/coverage/combine__${
                    builtins.elemAt
                    test
                    0
                  }")
                  functionalCoverageCombine;
                stage = "post-deploy";
              };
          }
          {
            output = "/testTerraform/skims";
            gitlabExtra = gitlabTestInfra;
          }
          {
            output = "/securePythonWithBandit/skims";
            gitlabExtra = gitlabLint;
          }
        ];
    };
  };
}
