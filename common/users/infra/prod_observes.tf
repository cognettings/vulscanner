locals {
  observes_redshift_cluster = {
    policies = {
      aws = {
        EtlDataAccess = [
          {
            Sid    = "MigrationBucketManagement"
            Effect = "Allow"
            Action = [
              "s3:GetObject",
              "s3:GetBucketAcl",
              "s3:GetBucketCors",
              "s3:GetEncryptionConfiguration",
              "s3:GetBucketLocation",
              "s3:ListBucket",
              "s3:ListAllMyBuckets",
              "s3:ListMultipartUploadParts",
              "s3:ListBucketMultipartUploads",
              "s3:PutObject",
              "s3:PutBucketAcl",
              "s3:PutBucketCors",
              "s3:DeleteObject",
              "s3:AbortMultipartUpload",
              "s3:CreateBucket",
            ]
            Resource = [
              "arn:aws:s3:::observes.etl-data",
              "arn:aws:s3:::observes.etl-data/*",
            ]
          },
        ]
      }
    }
  }
  observes_redshift_scheduler = {
    policies = {
      aws = {
        RedshiftAccess = [
          {
            Sid    = "redshiftResize"
            Effect = "Allow"
            Action = [
              "redshift:ResizeCluster",
            ]
            Resource = [
              "*",
            ]
          }
        ]
      }
    }
  }
  prod_observes = {
    policies = {
      aws = {
        ObservesGeneralAccess = [
          {
            Sid    = "terraformStateWrite"
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
          {
            Sid    = "generalRead"
            Effect = "Allow"
            Action = [
              "account:Get",
              "batch:Describe*",
              "batch:List*",
              "billing:Get*",
              "billing:List*",
              "ce:Describe*",
              "ce:Get*",
              "ce:List*",
              "consolidatedbilling:Get*",
              "consolidatedbilling:List*",
              "cur:DescribeReportDefinitions",
              "cloudwatch:Describe*",
              "cloudwatch:Get*",
              "cloudwatch:List*",
              "dynamodb:BatchGet*",
              "dynamodb:Describe*",
              "dynamodb:Get*",
              "dynamodb:List*",
              "dynamodb:Query*",
              "dynamodb:Scan*",
              "ec2:Describe*",
              "ec2:Get*",
              "freetier:Get*",
              "iam:Get*",
              "iam:List*",
              "invoicing:List*",
              "kms:CreateAlias",
              "kms:CreateKey",
              "kms:Describe*",
              "kms:Get*",
              "kms:List*",
              "kms:TagResource",
              "kms:UntagResource",
              "kms:UpdateAlias",
              "logs:Describe*",
              "logs:Filter*",
              "logs:Get*",
              "logs:List*",
              "payments:Get*",
              "payments:List*",
              "s3:Get*",
              "s3:List*",
              "tag:GetResources",
              "tax:Get*",
              "tax:List*",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "legacyPolicy"
            Effect = "Allow"
            Action = [
              "aws-portal:ViewBilling",
              "aws-portal:ViewUsage",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "generalWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:s3:::integrates/continuous-repositories",
              "arn:aws:s3:::integrates/continuous-repositories/*",
              "arn:aws:s3:::integrates/continuous-data",
              "arn:aws:s3:::integrates/continuous-data/*",
              "arn:aws:s3:::fluidanalytics",
              "arn:aws:s3:::fluidanalytics/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/observes-*",
              "arn:aws:s3:::observes*",
            ]
          },
          {
            Sid    = "manageObservesReports"
            Effect = "Allow"
            Action = [
              "ce:CreateReport",
              "ce:DeleteReport",
              "ce:DescribeReport",
              "ce:UpdateReport",
            ]
            Resource = [
              "arn:aws:cur:::definition/observes*",
            ]
          },
          {
            Sid    = "putAlarm"
            Effect = "Allow"
            Action = ["cloudwatch:PutMetricAlarm"]
            Resource = [
              "*",
            ]
          },
        ]
        ObservesBatch = [
          {
            Sid    = "batchTags"
            Effect = "Allow"
            Action = [
              "batch:TagResource",
              "batch:UntagResource",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job/*",
            ]
            "Condition" : { "StringEquals" : { "aws:RequestTag/management:product" : "observes" } }
          },
          {
            Sid    = "batchCancel"
            Effect = "Allow"
            Action = [
              "batch:CancelJob",
              "batch:TerminateJob",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job/*",
            ]
            "Condition" : { "StringEquals" : { "aws:ResourceTag/management:product" : "observes" } }
          },
          {
            Sid    = "batchSubmit"
            Effect = "Allow"
            Action = [
              "batch:SubmitJob",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
            ]
            "Condition" : { "StringEquals" : { "aws:RequestTag/management:product" : "observes" } }
          },
        ]
        ObservesRedshift = [
          {
            Sid    = "PassClusterRole"
            Effect = "Allow"
            Action = ["iam:PassRole"]
            Resource = [
              module.observes_redshift_aws.role.arn,
              module.observes_redshift_scheduler.role.arn
            ]
          },
          {
            Sid    = "redshiftManager"
            Effect = "Allow"
            Action = [
              "redshift:*",
              "redshift-data:*",
              "redshift-serverless:*",
              "sqlworkbench:*",
              "secretsmanager:*",
            ]
            Resource = [
              "*",
            ]
          },
        ]
        ObservesKinesis = [
          {
            Sid    = "KinesisGeneralRead"
            Effect = "Allow"
            Action = [
              "kinesis:ListStreams",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "KinesisStreamManagement"
            Effect = "Allow"
            Action = [
              "kinesis:AddTagsToStream",
              "kinesis:CreateStream",
              "kinesis:DeleteStream",
              "kinesis:DecreaseStreamRetentionPeriod",
              "kinesis:DisableEnhancedMonitoring",
              "kinesis:EnableEnhancedMonitoring",
              "kinesis:GetRecords",
              "kinesis:GetShardIterator",
              "kinesis:IncreaseStreamRetentionPeriod",
              "kinesis:MergeShards",
              "kinesis:RegisterStreamConsumer",
              "kinesis:RemoveTagsFromStream",
              "kinesis:SplitShard",
              "kinesis:StartStreamEncryption",
              "kinesis:StopStreamEncryption",
              "kinesis:UpdateShardCount",
              "kinesis:UpdateStreamMode",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
            ]
          },
          {
            Sid    = "KinesisConsumerManagement"
            Effect = "Allow"
            Action = [
              "kinesis:DeregisterStreamConsumer",
              "kinesis:SubscribeToShard",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror/consumer/*"
            ]
          },
          {
            Sid    = "KinesisReadStream"
            Effect = "Allow"
            Action = [
              "kinesis:DescribeLimits",
              "kinesis:DescribeStream",
              "kinesis:DescribeStreamSummary",
              "kinesis:ListShards",
              "kinesis:ListStreamConsumers",
              "kinesis:ListTagsForStream",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
            ]
          },
          {
            Sid    = "KinesisReadConsumers"
            Effect = "Allow"
            Action = [
              "kinesis:DescribeStreamConsumer",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror/consumer/*"
            ]
          },
        ]
        ObservesSecGroups = [
          {
            Sid    = "manageObservesSecGroups"
            Effect = "Allow"
            Action = [
              "ec2:CreateSecurityGroup",
              "ec2:DeleteSecurityGroup",
              "ec2:AuthorizeSecurityGroupEgress",
              "ec2:AuthorizeSecurityGroupIngress",
              "ec2:RevokeSecurityGroupEgress",
              "ec2:RevokeSecurityGroupIngress",
              "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
              "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
              "ec2:CreateTags",
              "ec2:DeleteTags",
              "ec2:DescribeTags",
            ]
            Resource = ["*"]
          },
        ]
      }
    }

    keys = {
      prod_observes = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_observes",
        ]
        tags = {
          "Name"               = "prod_observes"
          "management:area"    = "cost"
          "management:product" = "observes"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_observes" {
  source = "./modules/aws"

  name     = "prod_observes"
  policies = local.prod_observes.policies.aws
  tags = {
    "Name"               = "prod_observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

module "observes_redshift_aws" {
  # role for the redshift cluster
  # - only has access to the ETL data bucket
  source = "./modules/aws"

  name     = "observes_redshift_cluster"
  policies = local.observes_redshift_cluster.policies.aws
  assume_role_policy = [
    {
      Sid    = "RedshiftAccess",
      Effect = "Allow",
      Principal = {
        Service = "redshift.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }
  ]
  tags = {
    "Name"               = "observes_redshift_cluster"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
module "observes_redshift_scheduler" {
  # role for the redshift scheduler service
  # - only has permissions to resize the clusters
  source = "./modules/aws"

  name     = "observes_redshift_scheduler"
  policies = local.observes_redshift_scheduler.policies.aws
  assume_role_policy = [
    {
      Sid    = "RedshiftAccess",
      Effect = "Allow",
      Principal = {
        Service = "scheduler.redshift.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }
  ]
  tags = {
    "Name"               = "observes_redshift_scheduler"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

module "prod_observes_keys" {
  source   = "./modules/key"
  for_each = local.prod_observes.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}
