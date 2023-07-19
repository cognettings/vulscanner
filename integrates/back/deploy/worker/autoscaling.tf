resource "kubernetes_manifest" "scaledobject_prod_integrates_integrates_tasks_autoscaler" {
  manifest = {
    "apiVersion" = "keda.sh/v1alpha1"
    "kind"       = "ScaledObject"
    "metadata" = {
      "name"      = "integrates-tasks-autoscaler-${var.deployment_name}"
      "namespace" = "prod-integrates"
    }
    "spec" = {
      "advanced" = {
        "horizontalPodAutoscalerConfig" = {
          "behavior" = {
            "scaleDown" = {
              "policies" = [
                {
                  "periodSeconds" = 60
                  "type"          = "Percent"
                  "value"         = 40
                },
              ]
              "stabilizationWindowSeconds" = 240
            }
            "scaleUp" = {
              "policies" = [
                {
                  "periodSeconds" = 60
                  "type"          = "Percent"
                  "value"         = 30
                },
              ]
              "stabilizationWindowSeconds" = 180
            }
          }
        }
      }
      "fallback" = {
        "failureThreshold" = 5
        "replicas"         = 3
      }
      "maxReplicaCount" = 45
      "minReplicaCount" = 1
      "pollingInterval" = 20
      "scaleTargetRef" = {
        "name" = "integrates-tasks-${var.deployment_name}"
      }
      "triggers" = [
        {
          "metadata" = {
            "awsRegion"     = "us-east-1"
            "identityOwner" = "operator"
            "queueLength"   = "20"
            "queueURL"      = "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_report"
          }
          "type" = "aws-sqs-queue"
        },
        {
          "metadata" = {
            "awsRegion"     = "us-east-1"
            "identityOwner" = "operator"
            "queueLength"   = "50"
            "queueURL"      = "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_report_soon"
          }
          "type" = "aws-sqs-queue"
        },
        {
          "metadata" = {
            "awsRegion"     = "us-east-1"
            "identityOwner" = "operator"
            "queueLength"   = "50"
            "queueURL"      = "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_clone"
          }
          "type" = "aws-sqs-queue"
        },
        {
          "metadata" = {
            "awsRegion"     = "us-east-1"
            "identityOwner" = "operator"
            "queueLength"   = "150"
            "queueURL"      = "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_refresh"
          }
          "type" = "aws-sqs-queue"
        },
        {
          "metadata" = {
            "awsRegion"     = "us-east-1"
            "identityOwner" = "operator"
            "queueLength"   = "200"
            "queueURL"      = "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_rebase"
          }
          "type" = "aws-sqs-queue"
        },
      ]
    }
  }
}
