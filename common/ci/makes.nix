# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  projectPath,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.bash
      inputs.nixpkgs.git
      inputs.nixpkgs.jq
    ];
  };
in {
  deployTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCi"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCi"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonCi = {
      vars = [
        "BETTER_UPTIME_API_TOKEN"
        "GITLAB_RUNNER_TOKEN"
        "UNIVERSE_API_TOKEN"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonCi = {
      betterUptimeApiToken = "BETTER_UPTIME_API_TOKEN";
      gitlabApiToken = "UNIVERSE_API_TOKEN";
      gitlabRunnerToken = "GITLAB_RUNNER_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCi"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  lintPython = {
    modules = {
      commonCiInfraModuleInspector = {
        searchPaths.source = [
          outputs."/common/ci/infra/module/inspector/env"
        ];
        python = "3.10";
        src = "/common/ci/infra/module/inspector/src";
      };
    };
  };
}
