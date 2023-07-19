resource "kubernetes_horizontal_pod_autoscaler_v2" "name" {
  metadata {
    name      = "integrates-${var.deployment_name}"
    namespace = "prod-integrates"
  }
  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment_v1.integrates_prod.metadata[0].name
    }
    min_replicas = 5
    max_replicas = 75
    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 60
        }
      }
    }
  }
}
