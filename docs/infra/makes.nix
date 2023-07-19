{outputs, ...}: {
  deployTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodDocs"
          outputs."/secretsForEnvFromSops/docsInfraProd"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/docsInfraDev"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra/src";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    docsInfraDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN"];
      manifest = "/docs/secrets/dev.yaml";
    };
    docsInfraProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_TOKEN"];
      manifest = "/docs/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    docsInfra = {
      cloudflareAccountId = "CLOUDFLARE_ACCOUNT_ID";
      cloudflareApiToken = "CLOUDFLARE_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      docsInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/docsInfraDev"
          outputs."/secretsForTerraformFromEnv/docsInfra"
        ];
        src = "/docs/infra/src";
        version = "1.0";
      };
    };
  };
}
