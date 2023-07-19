locals {
  prod_docs = {
    policies = {
      aws = {
        DocsPolicy = [
          {
            Sid    = "s3Write"
            Effect = "Allow"
            Action = ["*"]
            // This buckets and resources list belog to docs, so the wildcard
            // above is not dangerous
            Resource = [
              "arn:aws:s3:::docs.fluidattacks.com",
              "arn:aws:s3:::docs.fluidattacks.com/*",
              "arn:aws:s3:::docs-dev.fluidattacks.com",
              "arn:aws:s3:::docs-dev.fluidattacks.com/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/docs*",
            ]
          },
          {
            Sid    = "dynamoWrite"
            Effect = "Allow"
            Action = [
              "dynamodb:DeleteItem",
              "dynamodb:GetItem",
              "dynamodb:PutItem",
            ]
            Resource = [
              var.terraform_state_lock_arn,
            ]
          },
        ]
      }

      cloudflare = {
        account = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Scripts Write"],
          ]
          resources = {
            "com.cloudflare.api.account.*" = "*"
          }
        }
        accountZone = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
          ]
          resources = {
            "com.cloudflare.api.account.zone.*" = "*"
          }
        }
      }
    }

    keys = {
      prod_docs = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_docs",
        ]
        tags = {
          "Name"               = "prod_docs"
          "management:area"    = "cost"
          "management:product" = "docs"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_docs_aws" {
  source = "./modules/aws"

  name     = "prod_docs"
  policies = local.prod_docs.policies.aws

  tags = {
    "Name"               = "prod_docs"
    "management:area"    = "cost"
    "management:product" = "docs"
    "management:type"    = "product"
  }
}

module "prod_docs_keys" {
  source   = "./modules/key"
  for_each = local.prod_docs.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}

module "prod_docs_cloudflare" {
  source = "./modules/cloudflare"

  name   = "prod_docs"
  policy = local.prod_docs.policies.cloudflare
}

output "prod_docs_cloudflare_api_token" {
  sensitive = true
  value     = module.prod_docs_cloudflare.cloudflare_api_token
}
