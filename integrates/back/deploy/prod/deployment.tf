resource "kubernetes_deployment_v1" "integrates_prod" {
  metadata {
    name      = "integrates-${var.deployment_name}"
    namespace = "prod-itegrates"
  }
  spec {
    replicas = var.replicas
    selector {
      match_labels = {
        "app" = "integrates-${var.deployment_name}"
      }
    }
    strategy {
      rolling_update {
        max_surge       = "25%"
        max_unavailable = "10%"
      }
    }
    template {
      metadata {
        labels = {
          "app" = "integrates-${var.deployment_name}"
          "uuid" : var.uuid
        }
      }
      spec {
        service_account_name = "prod-integrates"
        node_selector = {
          "worker_group" = "prod_integrates"
        }
        termination_grace_period_seconds = 60
        container {
          name              = "back"
          image             = "ghcr.io/fluidattacks/makes/arm64:latest"
          image_pull_policy = "Always"
          command           = ["sh"]
          args = [
            "-c",
            "m gitlab:fluidattacks/universe@${var.ci_commit_sha} /integrates/back/deploy/probes/liveness;",
            "m gitlab:fluidattacks/universe@${var.ci_commit_sha} /integrates/back/deploy/probes/readiness;",
            "m gitlab:fluidattacks/universe@${var.ci_commit_sha} /integrates/back prod"
          ]
          env {
            name  = "MAKES_K8S_COMPAT"
            value = "1"
          }
          env {
            name  = "OTEL_EXPORTER_OTLP_ENDPOINT"
            value = "http://adot-collector.kube-system:4317"
          }
          resources {
            requests = {
              "cpu"    = "1000m"
              "memory" = "600Mi"
            }
            limits = {
              "cpu"    = "2000m"
              "memory" = "6500Mi"
            }
          }
          env_from {
            secret_ref {
              name = "integrates-${var.deployment_name}"
            }
          }
          security_context {
            allow_privilege_escalation = false
            privileged                 = false
            read_only_root_filesystem  = false
          }
          port {
            container_port = 8001
          }
          readiness_probe {
            exec {
              command = [
                "sh",
                "-c",
                "~/.cache/makes/out-integrates-back-deploy-probes-readiness/bin/* prod_integrates FluidIntegrates http://localhost:8001"
              ]
            }
            initial_delay_seconds = 120
            period_seconds        = 60
            success_threshold     = 1
            failure_threshold     = 10
            timeout_seconds       = 60
          }
          liveness_probe {
            exec {
              command = [
                "sh",
                "-c",
                "~/.cache/makes/out-integrates-back-deploy-probes-liveness/bin/* prod_integrates FluidIntegrates http://localhost:8001 https://${var.endpoint}.fluidattacks.com"
              ]
            }
            initial_delay_seconds = 120
            period_seconds        = 60
            success_threshold     = 1
            failure_threshold     = 10
            timeout_seconds       = 60
          }
        }
      }
    }
  }
}
