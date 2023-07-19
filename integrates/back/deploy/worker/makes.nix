{outputs, ...}: {
  secretsForTerraformFromEnv = {
    workerInfra = {
      cluster_ca_certificate = "CLUSTER_CA_CERTIFICATE";
      cluster_endpoint = "CLUSTER_ENDPOINT";
      ci_commit_sha = "CI_COMMIT_SHA";
    };
  };
  deployTerraform = {
    modules = {
      workerInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/integrates/back/deploy/worker/variables"
          outputs."/secretsForTerraformFromEnv/workerInfra"
        ];
        src = "/integrates/back/deploy/worker";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      workerInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/integrates/back/deploy/worker/variables"
          outputs."/secretsForTerraformFromEnv/workerInfra"
        ];
        src = "/integrates/back/deploy/worker";
        version = "1.0";
      };
    };
  };
}
