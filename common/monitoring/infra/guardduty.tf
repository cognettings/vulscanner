provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

resource "aws_guardduty_detector" "us_east_1" {
  enable   = true
  provider = aws.us-east-1

  tags = {
    "Name"               = "guarduty"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }
}

provider "aws" {
  alias  = "us-east-2"
  region = "us-east-2"
}

resource "aws_guardduty_detector" "us_east_2" {
  enable   = true
  provider = aws.us-east-2

  tags = {
    "Name"               = "guarduty"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
  }
}

provider "aws" {
  alias  = "us-west-1"
  region = "us-west-1"
}

resource "aws_guardduty_detector" "us_west_1" {
  enable   = true
  provider = aws.us-west-1

  tags = {
    "Name"               = "guarduty"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
  }
}

provider "aws" {
  alias  = "us-west-2"
  region = "us-west-2"
}

resource "aws_guardduty_detector" "us_west_2" {
  enable   = true
  provider = aws.us-west-2

  tags = {
    "Name"               = "guarduty"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
  }
}
