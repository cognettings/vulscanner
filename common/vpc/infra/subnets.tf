locals {
  subnets = [
    {
      name                    = "free2"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = false
      new_bits                = 6
      tags                    = {}
    },
    {
      name                    = "observes_1"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = false
      new_bits                = 9
      tags                    = {}
    },
    {
      name                    = "observes_2"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = false
      new_bits                = 9
      tags                    = {}
    },
    {
      name                    = "observes_3"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = false
      new_bits                = 9
      tags                    = {}
    },
    {
      name                    = "observes_4"
      availability_zone       = "us-east-1e"
      map_public_ip_on_launch = false
      new_bits                = 9
      tags                    = {}
    },
    {
      name                    = "free1"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = false
      new_bits                = 7
      tags                    = {}
    },
    {
      name                    = "batch_clone"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "free3"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "common"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = false
      new_bits                = 7
      tags                    = {}
    },
    {
      name                    = "k8s_1"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_2"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_3"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_4"
      availability_zone       = "us-east-1f"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_5"
      availability_zone       = "us-east-1e"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_6"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_7"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_8"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_9"
      availability_zone       = "us-east-1f"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "k8s_10"
      availability_zone       = "us-east-1e"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/common-k8s" = "shared"
        "kubernetes.io/role/elb"           = "1"
      }
    },
    {
      name                    = "ci_1"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = false
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "ci_2"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = false
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "ci_3"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = false
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "ci_4"
      availability_zone       = "us-east-1e"
      map_public_ip_on_launch = false
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "ci_5"
      availability_zone       = "us-east-1f"
      map_public_ip_on_launch = false
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "batch_main_1"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "batch_main_2"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "batch_main_3"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "batch_main_4"
      availability_zone       = "us-east-1e"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
    {
      name                    = "batch_main_5"
      availability_zone       = "us-east-1f"
      map_public_ip_on_launch = true
      new_bits                = 8
      tags                    = {}
    },
  ]
}

module "subnet_addrs" {
  source  = "hashicorp/subnets/cidr"
  version = "1.0.0"

  base_cidr_block = aws_vpc.fluid-vpc.cidr_block
  networks        = local.subnets
}

resource "aws_subnet" "main" {
  for_each = {
    for subnet in local.subnets : subnet.name => subnet
  }

  vpc_id                  = aws_vpc.fluid-vpc.id
  cidr_block              = module.subnet_addrs.network_cidr_blocks[each.key]
  availability_zone       = each.value.availability_zone
  map_public_ip_on_launch = each.value.map_public_ip_on_launch

  tags = merge(
    {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    },
    each.value.tags,
  )
}
