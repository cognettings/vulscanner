resource "aws_sns_topic" "guardduty_alert_us_east_2" {
  name     = "guardduty_alert"
  provider = aws.us-east-2

  policy = jsonencode(
    {
      Version = "2008-10-17"
      Statement = [
        {
          Sid    = "default"
          Effect = "Allow"
          Principal = {
            AWS = "*"
          }
          Action = [
            "sns:GetTopicAttributes",
            "sns:SetTopicAttributes",
            "sns:AddPermission",
            "sns:RemovePermission",
            "sns:DeleteTopic",
            "sns:Subscribe",
            "sns:ListSubscriptionsByTopic",
            "sns:Publish",
          ]
          Resource = ["*"]
          Condition = {
            StringEquals = {
              "AWS:SourceOwner" = "205810638802"
            }
          }
        },
        {
          Sid    = "AWSAnomalyDetectionSNSPublishingPermissions",
          Effect = "Allow",
          Principal = {
            Service = ["costalerts.amazonaws.com"]
          },
          Action   = ["sns:Publish"]
          Resource = ["*"]
        },
      ]
    }
  )

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_rule" "guardduty_alert_us_east_2" {
  name     = "guardduty_alert"
  provider = aws.us-east-2

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
    detail = {
      severity = range(1, 9, 0.1),
    }
  })

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "guardduty_alert_us_east_2" {
  rule      = aws_cloudwatch_event_rule.guardduty_alert_us_east_2.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.guardduty_alert_us_east_2.arn
  provider  = aws.us-east-2

  input_transformer {
    input_paths = {
      severity            = "$.detail.severity"
      Account_ID          = "$.detail.accountId"
      Finding_ID          = "$.detail.id"
      Finding_Type        = "$.detail.type"
      region              = "$.region"
      Finding_description = "$.detail.description"
    }
    input_template = <<EOF
{
  "region": <region>,
  "FindingUrl": "https://console.aws.amazon.com/guardduty/home?region=<region>#/findings?search=id%3D<Finding_ID>",
  "Account_ID": <Account_ID>,
  "severity": <severity>,
  "Finding_ID": <Finding_ID>,
  "Finding_Type": <Finding_Type>,
  "Finding_description": <Finding_description>
}
EOF
  }
}

resource "aws_sns_topic" "guardduty_alert_us_west_1" {
  name     = "guardduty_alert"
  provider = aws.us-west-1

  policy = jsonencode(
    {
      Version = "2008-10-17"
      Statement = [
        {
          Sid    = "default"
          Effect = "Allow"
          Principal = {
            AWS = "*"
          }
          Action = [
            "sns:GetTopicAttributes",
            "sns:SetTopicAttributes",
            "sns:AddPermission",
            "sns:RemovePermission",
            "sns:DeleteTopic",
            "sns:Subscribe",
            "sns:ListSubscriptionsByTopic",
            "sns:Publish",
          ]
          Resource = ["*"]
          Condition = {
            StringEquals = {
              "AWS:SourceOwner" = "205810638802"
            }
          }
        },
        {
          Sid    = "AWSAnomalyDetectionSNSPublishingPermissions",
          Effect = "Allow",
          Principal = {
            Service = ["costalerts.amazonaws.com"]
          },
          Action   = ["sns:Publish"]
          Resource = ["*"]
        },
      ]
    }
  )

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_rule" "guardduty_alert_us_west_1" {
  name     = "guardduty_alert"
  provider = aws.us-west-1

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
    detail = {
      severity = range(1, 9, 0.1),
    }
  })

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "guardduty_alert_us_west_1" {
  rule      = aws_cloudwatch_event_rule.guardduty_alert_us_west_1.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.guardduty_alert_us_west_1.arn
  provider  = aws.us-west-1

  input_transformer {
    input_paths = {
      severity            = "$.detail.severity"
      Account_ID          = "$.detail.accountId"
      Finding_ID          = "$.detail.id"
      Finding_Type        = "$.detail.type"
      region              = "$.region"
      Finding_description = "$.detail.description"
    }
    input_template = <<EOF
{
  "region": <region>,
  "FindingUrl": "https://console.aws.amazon.com/guardduty/home?region=<region>#/findings?search=id%3D<Finding_ID>",
  "Account_ID": <Account_ID>,
  "severity": <severity>,
  "Finding_ID": <Finding_ID>,
  "Finding_Type": <Finding_Type>,
  "Finding_description": <Finding_description>
}
EOF
  }
}

resource "aws_sns_topic" "guardduty_alert_us_west_2" {
  name     = "guardduty_alert"
  provider = aws.us-west-2

  policy = jsonencode(
    {
      Version = "2008-10-17"
      Statement = [
        {
          Sid    = "default"
          Effect = "Allow"
          Principal = {
            AWS = "*"
          }
          Action = [
            "sns:GetTopicAttributes",
            "sns:SetTopicAttributes",
            "sns:AddPermission",
            "sns:RemovePermission",
            "sns:DeleteTopic",
            "sns:Subscribe",
            "sns:ListSubscriptionsByTopic",
            "sns:Publish",
          ]
          Resource = ["*"]
          Condition = {
            StringEquals = {
              "AWS:SourceOwner" = "205810638802"
            }
          }
        },
        {
          Sid    = "AWSAnomalyDetectionSNSPublishingPermissions",
          Effect = "Allow",
          Principal = {
            Service = ["costalerts.amazonaws.com"]
          },
          Action   = ["sns:Publish"]
          Resource = ["*"]
        },
      ]
    }
  )

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}


resource "aws_cloudwatch_event_rule" "guardduty_alert_us_west_2" {
  name     = "guardduty_alert"
  provider = aws.us-west-2

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
    detail = {
      severity = range(1, 9, 0.1),
    }
  })

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "guardduty_alert_us_west_2" {
  rule      = aws_cloudwatch_event_rule.guardduty_alert_us_west_2.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.guardduty_alert_us_west_2.arn
  provider  = aws.us-west-2

  input_transformer {
    input_paths = {
      severity            = "$.detail.severity"
      Account_ID          = "$.detail.accountId"
      Finding_ID          = "$.detail.id"
      Finding_Type        = "$.detail.type"
      region              = "$.region"
      Finding_description = "$.detail.description"
    }
    input_template = <<EOF
{
  "region": <region>,
  "FindingUrl": "https://console.aws.amazon.com/guardduty/home?region=<region>#/findings?search=id%3D<Finding_ID>",
  "Account_ID": <Account_ID>,
  "severity": <severity>,
  "Finding_ID": <Finding_ID>,
  "Finding_Type": <Finding_Type>,
  "Finding_description": <Finding_description>
}
EOF
  }
}
