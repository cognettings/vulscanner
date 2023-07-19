module "inspector" {
  source = "./module/inspector"

  better_uptime_api_token = var.betterUptimeApiToken
  gitlab_api_token        = var.gitlabApiToken
  name                    = "common-ci-infra-module-inspector"
  region                  = var.region

  tags = {
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

output "inspector_endpoint" {
  value = module.inspector.endpoint
}
