resource "kubernetes_deployment_v1" "worker" {
  metadata {
    name      = "integrates-tasks-${var.deployment_name}"
    namespace = "prod-integrates"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "integrates-tasks-${var.deployment_name}"
      }
    }

    strategy {
      rolling_update {
        max_surge       = "10%"
        max_unavailable = "10%"
      }
    }

    template {
      metadata {
        labels = {
          app = "integrates-tasks-${var.deployment_name}"
        }
      }

      spec {
        service_account_name = "prod-integrates"
        node_selector = {
          "worker_group" = "prod_skims"
        }

        container {
          name              = "tasks-worker"
          image             = "ghcr.io/fluidattacks/makes/arm64:latest"
          image_pull_policy = "Always"

          command = ["sh"]
          args    = ["-c", "m gitlab:fluidattacks/universe@${var.ci_commit_sha} /integrates/jobs/server_async"]

          env {
            name  = "MAKES_K8S_COMPAT"
            value = "1"
          }
          resources {
            requests = {
              cpu    = "1000m"
              memory = "6000Mi"
            }
            limits = {
              cpu    = "2000m"
              memory = "6500Mi"
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

        }

        termination_grace_period_seconds = 120
      }
    }
  }
}
