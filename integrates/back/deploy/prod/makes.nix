{outputs, ...}: {
  secretsForTerraformFromEnv = {
    integratesDeploy = {
      cluster_ca_certificate = "CLUSTER_CA_CERTIFICATE";
      cluster_endpoint = "CLUSTER_ENDPOINT";
      ci_commit_sha = "CI_COMMIT_SHA";
      ci_commit_ref_name = "CI_COMMIT_REF_NAME";
      cachix_auth_token = "CACHIX_AUTH_TOKEN";
      replicas = "REPLICAS";
      uuid = "UUID";
      universe_api_token = "UNIVERSE_API_TOKEN";
    };
  };
  envVarsForTerraform = {
    integratesDeploy = {
      endpoint = "app";
    };
  };
  deployTerraform = {
    modules = {
      integratesDeploy = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/integrates/back/deploy/prod/variables"
          outputs."/secretsForTerraformFromEnv/integratesDeploy"
          outputs."/envVarsForTerraform/integratesDeploy"
        ];
        src = "/integrates/back/deploy/prod";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesDeploy = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/integrates/back/deploy/prod/variables"
          outputs."/secretsForTerraformFromEnv/integratesDeploy"
          outputs."/envVarsForTerraform/integratesDeploy"
        ];
        src = "/integrates/back/deploy/prod";
        version = "1.0";
      };
    };
  };
}
