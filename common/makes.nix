# https://github.com/fluidattacks/makes
{
  imports = [
    ./ci/makes.nix
    ./compute/makes.nix
    ./criteria/makes.nix
    ./dev/makes.nix
    ./dns/makes.nix
    ./foss/makes.nix
    ./k8s/makes.nix
    ./monitoring/makes.nix
    ./okta/makes.nix
    ./pipeline/makes.nix
    ./status/makes.nix
    ./test/mr/makes.nix
    ./users/makes.nix
    ./utils/git_self/makes.nix
    ./utils/async_sqs_consummer/makes.nix
    ./vpc/makes.nix
    ./vpn/makes.nix
  ];
  secretsForAwsFromGitlab = {
    dev = {
      roleArn = "arn:aws:iam::205810638802:role/dev";
      duration = 3600;
    };
    prodCommon = {
      roleArn = "arn:aws:iam::205810638802:role/prod_common";
      duration = 3600;
    };
  };
  secretsForEnvFromSops = {
    commonCloudflareDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
    commonCloudflareProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
  };
}
