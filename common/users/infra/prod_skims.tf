locals {
  prod_skims = {
    policies = {
      aws = {
        SkimsPolicy = [
          {
            Sid    = "batchRead"
            Effect = "Allow"
            Action = [
              "batch:DescribeComputeEnvironments",
              "batch:DescribeJobDefinitions",
              "batch:DescribeJobQueues",
              "batch:DescribeJobs",
              "batch:ListJobs",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "batchWrite"
            Effect = "Allow"
            Action = [
              "batch:SubmitJob",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
            ]
          },
          {
            Sid    = "logsRead"
            Effect = "Allow"
            Action = [
              "logs:CreateLogGroup",
              "logs:Describe*",
              "logs:Filter*",
              "logs:Get*",
              "logs:List*",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "logsWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:log-group:skims",
              "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:log-group:skims:log-stream:*",
            ]
          },
          {
            Sid    = "ec2Read"
            Effect = "Allow"
            Action = [
              "ec2:Describe*",
              "ec2:Get*",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "ec2Write"
            Effect = "Allow"
            Action = [
              "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
              "ec2:AuthorizeSecurityGroupEgress",
              "ec2:AuthorizeSecurityGroupIngress",
              "ec2:Create*",
              "ec2:DeleteNetworkInterface",
              "ec2:DeleteSecurityGroup",
              "ec2:DeleteSubnet",
              "ec2:DeleteTags",
              "ec2:ModifySubnetAttribute",
              "ec2:RevokeSecurityGroupEgress",
              "ec2:RevokeSecurityGroupIngress",
              "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
              "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "s3Read"
            Effect = "Allow"
            Action = [
              "s3:ListBucket",
            ]
            Resource = [
              "arn:aws:s3:::fluidattacks.com",
            ]
          },
          {
            Sid    = "s3ReadRepos"
            Effect = "Allow"
            Action = [
              "s3:ListBucket",
              "s3:ListObjectsV2",
              "s3:GetObject",
            ]
            Resource = [
              "arn:aws:s3:::integrates/continuous-repositories",
              "arn:aws:s3:::integrates/continuous-repositories/*",
            ]
          },
          {
            Sid    = "write"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:s3:::fluidattacks.com/resources/doc/skims/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/skims*",
              "arn:aws:s3:::skims*",
              "arn:aws:s3:::skims.sca",
              "arn:aws:s3:::skims.sca/*",
              "arn:aws:dynamodb:us-east-1:205810638802:table/skims*",
              "arn:aws:dynamodb:us-east-1:205810638802:table/celery",
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
          {
            Sid    = "dynamoCreate"
            Effect = "Allow"
            Action = [
              "dynamodb:CreateTable"
            ]
            Resource = ["*"]
          },
          {
            Sid    = "dynamoReadJobs"
            Effect = "Allow"
            Action = [
              "dynamodb:GetItem",
              "dynamodb:Query",
              "dynamodb:DeleteItem",
              "dynamodb:UpdateItem",
            ]
            Resource = [
              "arn:aws:dynamodb:us-east-1:205810638802:table/fi_async_processing",
            ]
          },
          {
            Sid    = "sqsWrite"
            Effect = "Allow"
            Action = [
              "sqs:CreateQueue",
              "sqs:DeleteQueue",
              "sqs:GetQueueAttributes",
              "sqs:SetQueueAttributes",
              "sqs:TagQueue",
              "sqs:UntagQueue",
              "sqs:AddPermission",
              "sqs:RemovePermission",
              "sqs:ListQueues",
            ]
            Resource = [
              "*",
            ]
          },
          {
            Sid    = "sqsAll"
            Effect = "Allow"
            Action = [
              "sqs:*",
              "sqs:ChangeMessageVisibility",
              "sqs:DeleteMessage",
              "sqs:GetQueueUrl",
              "sqs:PurgeQueue",
              "sqs:ReceiveMessage",
              "sqs:SendMessage",
            ]
            Resource = [
              "arn:aws:sqs:us-east-1:205810638802:skims-*",
              "arn:aws:sqs:us-east-1:205810638802:celery",
            ]
          },
          {
            Sid    = "eksRead"
            Effect = "Allow"
            Action = [
              "eks:Describe*",
              "eks:Get*",
              "eks:ListQueues",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "eksWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:eks:${var.region}:${data.aws_caller_identity.main.account_id}:cluster/integrates-*"
            ]
          },
          {
            Sid    = "cloudWatchAll"
            Effect = "Allow"
            Action = [
              "cloudwatch:GetMetricData",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "sqsQueueMessages"
            Effect = "Allow"
            Action = [
              "sqs:ChangeMessageVisibility",
              "sqs:GetQueueAttributes",
              "sqs:GetQueueUrl",
              "sqs:SendMessage",
            ]
            Resource = [
              "arn:aws:sqs:us-east-1:205810638802:integrates_report_soon",
            ]
          }
        ]
      }
    }

    keys = {
      prod_skims = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_skims",
        ]
        tags = {
          "Name"               = "prod_skims"
          "management:area"    = "cost"
          "management:product" = "skims"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_skims_aws" {
  source = "./modules/aws"

  name     = "prod_skims"
  policies = local.prod_skims.policies.aws

  tags = {
    "Name"               = "prod_skims"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}

module "prod_skims_keys" {
  source   = "./modules/key"
  for_each = local.prod_skims.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}
