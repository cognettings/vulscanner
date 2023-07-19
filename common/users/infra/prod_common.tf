locals {
  prod_common = {
    policies = {
      aws = {
        AdminPolicy = [
          {
            Sid    = "allWrite"
            Effect = "Allow"
            Action = [
              "access-analyzer:*",
              "account:Get*",
              "acm:*",
              "aps:*",
              "apigateway:*",
              "athena:*",
              "autoscaling:*",
              "aws-marketplace:*",
              "backup:*",
              "batch:*",
              "billing:*",
              "budgets:*",
              "ce:*",
              "cloudformation:*",
              "cloudwatch:*",
              "cloudtrail:*",
              "consolidatedbilling:*",
              "cur:*",
              "dynamodb:*",
              "ec2:*",
              "ecs:*",
              "eks:*",
              "elasticache:*",
              "elasticloadbalancing:*",
              "es:*",
              "events:*",
              "firehose:*",
              "freetier:*",
              "glue:*",
              "grafana:*",
              "guardduty:*",
              "iam:*",
              "invoicing:*",
              "kinesis:*",
              "kinesisanalytics:*",
              "kms:*",
              "lambda:*",
              "logs:*",
              "organizations:*",
              "payments:*",
              "pricing:*",
              "ram:*",
              "rds:*",
              "redshift:*",
              "redshift-data:*",
              "redshift-serverless:*",
              "route53:*",
              "route53-recovery-control-config:*",
              "route53-recovery-readiness:*",
              "route53domains:*",
              "route53resolver:*",
              "s3:*",
              "sagemaker:*",
              "savingsplans:*",
              "schemas:*",
              "secretsmanager:*",
              "serverlessrepo:*",
              "servicequotas:*",
              "sns:*",
              "sso:*",
              "sqlworkbench:*",
              "sqs:*",
              "ssm:*",
              "sts:*",
              "support:*",
              "sustainability:*",
              "tag:*",
              "tax:*",
              "xray:*"
            ]
            Resource = ["*"]
          },
          {
            Sid    = "legacyPolicy"
            Effect = "Allow"
            Action = [
              "aws-portal:*",
            ]
            Resource = ["*"]
          },
        ]
      }
    }

    keys = {
      common_google = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_google"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_okta = {
        admins = [
          "prod_common",
        ]
        read_users = [
          "dev"
        ]
        users = []
        tags = {
          "Name"               = "common_okta"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_status = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_status"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_vpn = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_vpn"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      prod_common = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users      = []
        tags = {
          "Name"               = "prod_common"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_common_aws" {
  source = "./modules/aws"

  name     = "prod_common"
  policies = local.prod_common.policies.aws

  assume_role_policy = [
    {
      Sid    = "AssumeRolePolicy",
      Effect = "Allow",
      Principal = {
        Service = [
          "batch.amazonaws.com",
          "events.amazonaws.com",
          "spotfleet.amazonaws.com",
        ],
      },
      Action = "sts:AssumeRole",
    },
  ]

  tags = {
    "Name"               = "prod_common"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_common_keys" {
  source   = "./modules/key"
  for_each = local.prod_common.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}
