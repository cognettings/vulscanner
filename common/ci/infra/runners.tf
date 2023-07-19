locals {
  runners = {
    airs-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["airs-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "airs" },
      )
    }
    airs-large-x86 = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["airs-large-x86"] },
      )
      workers = merge(
        local.config.large.workers,
        {
          ami       = "ami-07dc2dd8e0efbc46a"
          instances = ["m5d.large"]
        }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "airs" },
      )
    }
    common-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["common-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "common" },
      )
    }
    common-small-x86 = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["common-small-x86"] },
      )
      workers = merge(
        local.config.small.workers,
        {
          ami       = "ami-07dc2dd8e0efbc46a"
          instances = ["c5d.large"]
        }
      )
      tags = merge(
        local.config.small.tags,
        { "management:product" = "common" },
      )
    }
    common-large-x86 = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["common-large-x86"] },
      )
      workers = merge(
        local.config.large.workers,
        {
          ami       = "ami-07dc2dd8e0efbc46a"
          instances = ["m5d.large"]
        }
      )
      tags = merge(
        local.config.large.tags,
        { "management:product" = "common" },
      )
    }
    common-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["common-large"] },
      )
      workers = local.config.large.workers
      tags = merge(
        local.config.large.tags,
        { "management:product" = "common" },
      )
    }
    docs-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["docs-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "docs" },
      )
    }
    integrates-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        {
          instance = "m7g.xlarge"
          tags     = ["integrates-small"]
        },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "integrates" },
      )
    }
    melts-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["melts-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "melts" },
      )
    }
    observes-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["observes-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "observes" },
      )
    }
    skims-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        {
          instance = "m7g.xlarge"
          tags     = ["skims-small"]
        },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "skims" },
      )
    }
    sorts-small = {
      replicas = 1
      runner = merge(
        local.config.small.runner,
        { tags = ["sorts-small"] },
      )
      workers = local.config.small.workers
      tags = merge(
        local.config.small.tags,
        { "management:product" = "sorts" },
      )
    }
    sorts-large = {
      replicas = 1
      runner = merge(
        local.config.large.runner,
        { tags = ["sorts-large"] },
      )
      workers = local.config.large.workers
      tags = merge(
        local.config.large.tags,
        { "management:product" = "sorts" },
      )
    }
  }
  config = {
    small = {
      replicas = 0
      runner = {
        instance       = "m7g.large"
        version        = "15.9.1"
        ami            = "ami-063dfa652e831d3d3"
        monitoring     = true
        check-interval = 3
        user-data      = ""

        disk-size      = 15
        disk-type      = "gp3"
        disk-optimized = true

        docker-machine-options = []

        tags = []
      }
      workers = {
        instances  = ["m6gd.medium"]
        ami        = "ami-004811053d831c2c2"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        limit      = 500

        idle-count = 0
        idle-time  = 900

        disk-size      = 10
        disk-type      = "gp3"
        disk-optimized = true
      }
      tags = {
        "management:area" = "innovation"
        "management:type" = "product"
      }
    }
    large = {
      replicas = 0
      runner = {
        instance       = "m7g.large"
        version        = "15.9.1"
        ami            = "ami-063dfa652e831d3d3"
        monitoring     = true
        check-interval = 3
        user-data      = ""

        disk-size      = 15
        disk-type      = "gp3"
        disk-optimized = true

        docker-machine-options = []

        tags = []
      }
      workers = {
        instances  = ["m6gd.large"]
        ami        = "ami-004811053d831c2c2"
        user-data  = local.user-data.ephemeral-disk
        monitoring = false
        limit      = 500

        idle-count = 0
        idle-time  = 900

        disk-size      = 10
        disk-type      = "gp3"
        disk-optimized = true
      }
      tags = {
        "management:area" = "innovation"
        "management:type" = "product"
      }
    }
  }
  user-data = {
    ephemeral-disk = <<-EOT
      Content-Type: multipart/mixed; boundary="==BOUNDARY=="
      MIME-Version: 1.0

      --==BOUNDARY==
      Content-Type: text/cloud-config; charset="us-ascii"
      MIME-Version: 1.0
      Content-Transfer-Encoding: 7bit
      Content-Disposition: attachment; filename="cloud-config.txt"

      disk_setup:
        /dev/nvme1n1:
          table_type: mbr
          layout: true
          overwrite: true

      fs_setup:
        - label: nvme
          filesystem: ext4
          device: /dev/nvme1n1
          partition: auto
          overwrite: true

      mounts:
        - [/dev/nvme1n1, /var/lib/docker]

      --==BOUNDARY==--
    EOT
  }
}

module "runners" {
  source  = "npalm/gitlab-runner/aws"
  version = "6.3.1"
  for_each = merge([
    for name, values in local.runners : {
      for replica in range(values.replicas) : "${name}-${replica}" => values
    }
  ]...)

  # AWS
  aws_region                             = "us-east-1"
  vpc_id                                 = data.aws_vpc.main.id
  allow_iam_service_linked_role_creation = true
  enable_kms                             = true
  kms_deletion_window_in_days            = 30
  enable_cloudwatch_logging              = false

  # Runner
  enable_runner_ssm_access          = true
  subnet_id                         = data.aws_subnet.main["ci_1"].id
  instance_type                     = each.value.runner.instance
  gitlab_runner_version             = each.value.runner.version
  runner_instance_enable_monitoring = each.value.runner.monitoring
  runner_instance_ebs_optimized     = each.value.runner.disk-optimized
  runners_check_interval            = each.value.runner.check-interval
  userdata_pre_install              = each.value.runner.user-data
  docker_machine_options            = each.value.runner.docker-machine-options
  ami_filter = {
    image-id = [each.value.runner.ami]
  }
  runner_root_block_device = {
    delete_on_termination = true
    encrypted             = true
    volume_type           = each.value.runner.disk-type
    volume_size           = each.value.runner.disk-size
  }
  gitlab_runner_registration_config = {
    registration_token = var.gitlabRunnerToken
    tag_list           = join(",", each.value.runner.tags)
    description        = "ci-${each.key}"
    locked_to_project  = "true"
    run_untagged       = "false"
    maximum_timeout    = "86400"
    access_level       = "not_protected"
  }
  runner_instance_metadata_options = {
    http_endpoint = "enabled",
    http_tokens   = "required",

    http_put_response_hop_limit = 2,
    instance_metadata_tags      = "disabled",
  }

  # Workers
  use_fleet                           = true
  enable_docker_machine_ssm_access    = true
  docker_machine_spot_price_bid       = ""
  runners_gitlab_url                  = "https://gitlab.com"
  runners_executor                    = "docker+machine"
  runners_max_builds                  = 128
  runners_name                        = "ci-${each.key}"
  runners_output_limit                = 8192
  runners_privileged                  = false
  runners_pull_policy                 = "always"
  runners_request_spot_instance       = true
  runners_use_private_address         = false
  fleet_executor_subnet_ids           = [for subnet in data.aws_subnet.main : subnet.id]
  runners_idle_time                   = each.value.workers.idle-time
  runners_idle_count                  = each.value.workers.idle-count / each.value.replicas
  runners_limit                       = each.value.workers.limit / each.value.replicas
  runners_concurrent                  = each.value.workers.limit / each.value.replicas
  runners_request_concurrency         = each.value.workers.limit / each.value.replicas / 2
  runners_monitoring                  = each.value.workers.monitoring
  docker_machine_instance_types_fleet = each.value.workers.instances
  runners_root_size                   = each.value.workers.disk-size
  runners_volume_type                 = each.value.workers.disk-type
  runners_ebs_optimized               = each.value.workers.disk-optimized
  runners_userdata                    = each.value.workers.user-data
  runner_ami_filter = {
    image-id = [each.value.workers.ami]
  }
  docker_machine_instance_metadata_options = {
    http_tokens                 = "required",
    http_put_response_hop_limit = 3,
  }


  # Cache
  cache_shared = true
  cache_bucket = {
    create = false
    policy = module.cache.policy_arn
    bucket = module.cache.bucket
  }

  # Tags
  environment = "ci-${each.key}"
  overrides = {
    name_runner_agent_instance  = "ci-runner-${each.key}",
    name_docker_machine_runners = "ci-worker-${each.key}",
    name_sg                     = "",
    name_iam_objects            = "",
  }
  tags = each.value.tags
}
