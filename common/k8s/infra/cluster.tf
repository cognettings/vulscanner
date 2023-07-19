locals {
  worker_groups = {
    core = {
      instance_types = [
        "m6g.large",
        "m6gd.large",
        "m7g.large",
      ]
      tags = {
        "management:area"    = "cost"
        "management:product" = "common"
        "management:type"    = "product"
      }
    }
    dev = {
      max_size  = 100
      disk_size = 50
      instance_types = [
        "m6g.xlarge",
        "m6gd.xlarge",
        "m7g.xlarge",
      ]
      tags = {
        "management:area"    = "innovation"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    prod_integrates = {
      max_size = 120
      instance_types = [
        "m6g.large",
        "m6gd.large",
        "m7g.large",
      ]
      tags = {
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    prod_skims = {
      max_size       = 50
      user_data      = "${path.module}/init/prod_skims"
      subnets        = [data.aws_subnet.batch_clone.id]
      instance_types = ["m6gd.large"]
      tags = {
        "management:area"    = "cost"
        "management:product" = "skims"
        "management:type"    = "service"
      }
    }
  }
}

module "cluster" {
  source                                 = "terraform-aws-modules/eks/aws"
  version                                = "19.6.0"
  cluster_name                           = local.cluster_name
  cluster_version                        = "1.24"
  cluster_endpoint_public_access         = true
  cluster_endpoint_private_access        = false
  enable_irsa                            = true
  cloudwatch_log_group_retention_in_days = 0

  # Nodes
  eks_managed_node_group_defaults = {
    capacity_type          = "SPOT"
    force_update_version   = true
    ebs_optimized          = true
    enable_monitoring      = true
    vpc_security_group_ids = [data.aws_security_group.cloudflare.id]
  }

  eks_managed_node_groups = {
    for group, values in local.worker_groups : group => {
      max_size = lookup(values, "max_size", 10)

      ami_type       = lookup(values, "arch", "AL2_ARM_64")
      instance_types = values.instance_types

      iam_role_additional_policies = {
        ssm_core = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
        ssm_role = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
      }

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            volume_size           = lookup(values, "disk_size", 20)
            volume_type           = "gp3"
            encrypted             = true
            delete_on_termination = true
          }
        }
      }
      user_data_template_path = lookup(values, "user_data", null)

      subnet_ids = lookup(
        values,
        "subnets",
        [for subnet in data.aws_subnet.main : subnet.id]
      )

      labels = merge(
        { worker_group = group },
        lookup(values, "labels", {}),
      )

      tags = values.tags
    }
  }

  # Network
  vpc_id     = data.aws_vpc.main.id
  subnet_ids = [for subnet in data.aws_subnet.main : subnet.id]

  # Auth
  manage_aws_auth_configmap = true
  aws_auth_accounts         = [data.aws_caller_identity.main.account_id]
  aws_auth_roles = concat(
    [
      for admin in local.admins : {
        rolearn  = data.aws_iam_role.main[admin].arn
        username = admin
        groups   = ["system:masters"]
      }
    ],
    [
      for user in local.users : {
        rolearn  = data.aws_iam_role.main[user].arn
        username = user
        groups   = distinct(["dev", user])
      }
    ],
  )

  # Encryption
  create_kms_key          = true
  enable_kms_key_rotation = true
  kms_key_aliases         = [local.cluster_name]
  kms_key_owners = [
    for admin in local.admins : data.aws_iam_role.main[admin].arn
  ]
  kms_key_administrators = [
    for user in local.users : data.aws_iam_role.main[user].arn
  ]

  node_security_group_additional_rules = {
    keda_metrics_server_access = {
      description                   = "Cluster access to keda operator deployment"
      protocol                      = "tcp"
      from_port                     = 9666
      to_port                       = 9666
      type                          = "ingress"
      source_cluster_security_group = true
    }
  }

  tags = {
    "Name"               = local.cluster_name
    "Environment"        = "production"
    "GithubRepo"         = "terraform-aws-eks"
    "GithubOrg"          = "terraform-aws-modules"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
