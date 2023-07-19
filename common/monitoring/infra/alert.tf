resource "aws_ce_anomaly_monitor" "cost_anomaly_alert" {
  name              = "cost_anomaly_alert"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_sns_topic" "cost_anomaly_alert" {
  name = "cost_anomaly_alert"

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
    "Name"               = "cost_anomaly_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_sns_topic_subscription" "cost_anomaly_alert" {
  protocol  = "email"
  endpoint  = "development@fluidattacks.com"
  topic_arn = aws_sns_topic.cost_anomaly_alert.arn
}

resource "aws_ce_anomaly_subscription" "cost_anomaly_alert" {
  name      = "cost_anomaly_alert"
  frequency = "IMMEDIATE"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.cost_anomaly_alert.arn,
  ]

  subscriber {
    type    = "SNS"
    address = aws_sns_topic.cost_anomaly_alert.arn
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_PERCENTAGE"
      values        = ["15"]
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
}

resource "aws_sns_topic" "guardduty_alert" {
  name         = "guardduty_alert"
  display_name = "Guardduty Notification"

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
          Sid    = "eventsSns",
          Effect = "Allow",
          Principal = {
            Service = ["events.amazonaws.com"]
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

resource "aws_sns_topic_subscription" "guardduty_alert" {
  protocol  = "email"
  endpoint  = "development@fluidattacks.com"
  topic_arn = aws_sns_topic.guardduty_alert.arn
}

resource "aws_cloudwatch_event_rule" "guardduty_alert" {
  name = "guardduty_alert"

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
    detail = {
      severity = range(4, 9, 0.1),
    }
  })

  tags = {
    "Name"               = "guardduty_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "guardduty_alert" {
  rule      = aws_cloudwatch_event_rule.guardduty_alert.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.guardduty_alert.arn

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

resource "aws_sns_topic" "grafana_alerts" {
  name       = "grafana_alerts"
  fifo_topic = false
}

resource "aws_sns_topic_subscription" "grafana_alerts" {
  protocol  = "email"
  endpoint  = "auribe@fluidattacks.com"
  topic_arn = aws_sns_topic.grafana_alerts.arn
}
