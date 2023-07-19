locals {
  machine_sizes = {
    small = {
      max_vcpus = 10000
      instances = ["m6gd.medium"]
    }
    medium = {
      max_vcpus = 10000
      instances = ["m6gd.large"]
    }
    large = {
      max_vcpus = 10000
      instances = ["m6gd.xlarge"]
    }
  }
  config = {
    common = {
      product = "common"
      subnets = [for subnet in data.aws_subnet.main : subnet.id]
      type    = "SPOT"
    }
    integrates = {
      product = "integrates"
      subnets = [for subnet in data.aws_subnet.main : subnet.id]
      type    = "SPOT"
    }
    skims = {
      product = "skims"
      subnets = [for subnet in data.aws_subnet.main : subnet.id]
      type    = "SPOT"
    }
    sorts = {
      product = "sorts"
      subnets = [for subnet in data.aws_subnet.main : subnet.id]
      type    = "SPOT"
    }
    observes = {
      product = "observes"
      subnets = [for subnet in data.aws_subnet.main : subnet.id]
      type    = "SPOT"
    }

  }
  environments = {
    clone = merge(
      local.machine_sizes.small,
      local.config.common,
      { subnets = [data.aws_subnet.clone.id] }
    )
    common_small = merge(
      local.machine_sizes.small,
      local.config.common
    )
    integrates_small = merge(
      local.machine_sizes.small,
      local.config.integrates
    )
    integrates_medium = merge(
      local.machine_sizes.medium,
      local.config.integrates
    )
    integrates_large = merge(
      local.machine_sizes.large,
      local.config.integrates,
    )
    observes_small = merge(
      local.machine_sizes.small,
      local.config.observes
    )
    observes_medium = merge(
      local.machine_sizes.medium,
      local.config.observes
    )
    observes_large = merge(
      local.machine_sizes.large,
      local.config.observes,
    )
    skims_small = merge(
      local.machine_sizes.small,
      local.config.skims
    )
    skims_medium = merge(
      local.machine_sizes.medium,
      local.config.skims
    )
    skims_large = merge(
      local.machine_sizes.large,
      local.config.skims
    )
    sorts_small = merge(
      local.machine_sizes.small,
      local.config.sorts
    )
    sorts_large = merge(
      local.machine_sizes.large,
      local.config.sorts,
    )
  }
}

resource "aws_security_group" "main" {
  name   = "compute"
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = []
  }
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"               = "compute"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_instance_profile" "main" {
  name = "ecsAndSsmInstanceProfileForBatch"
  role = aws_iam_role.main.name
}

resource "aws_iam_role" "main" {
  name = "ecsAndSsmRoleForBatch"
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM",
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
  ]
}

resource "aws_launch_template" "main" {
  name                                 = "compute"
  key_name                             = "gitlab"
  instance_initiated_shutdown_behavior = "terminate"

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      encrypted             = true
      delete_on_termination = true
      volume_size           = 30
      volume_type           = "gp3"
    }
  }

  block_device_mappings {
    device_name  = "/dev/xvdcz"
    virtual_name = "ephemeral0"
  }

  tag_specifications {
    resource_type = "volume"

    tags = {
      "Name"               = "compute"
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tags = {
    "Name"               = "compute"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  user_data               = filebase64("${path.module}/aws_batch_user_data")
  disable_api_termination = true
  vpc_security_group_ids  = [aws_security_group.main.id]
}

resource "aws_batch_compute_environment" "main" {
  for_each = local.environments

  compute_environment_name_prefix = "${each.key}_"

  service_role = data.aws_iam_role.main["prod_common"].arn
  state        = "ENABLED"
  type         = "MANAGED"

  compute_resources {
    bid_percentage = 100
    image_id       = "ami-0f09ed56128e994fe"
    type           = each.value.type

    max_vcpus = each.value.max_vcpus
    min_vcpus = 0

    instance_role       = aws_iam_instance_profile.main.arn
    spot_iam_fleet_role = data.aws_iam_role.main["prod_common"].arn

    instance_type      = each.value.instances
    security_group_ids = [aws_security_group.main.id]
    subnets            = each.value.subnets

    tags = {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = each.value.product
      "management:type"    = "product"
    }

    launch_template {
      launch_template_id = aws_launch_template.main.id
      version            = aws_launch_template.main.latest_version
    }
  }

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = each.value.product
    "management:type"    = "product"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_batch_job_queue" "main" {
  for_each = local.environments

  name                 = each.key
  state                = "ENABLED"
  priority             = 1
  compute_environments = [aws_batch_compute_environment.main[each.key].arn]

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = each.value.product
    "management:type"    = "product"
  }
}
