resource "kubernetes_service_v1" "integrates" {
  metadata {
    name      = "integrates-${var.deployment_name}"
    namespace = "prod-integrates"
  }
  spec {
    type = "NodePort"
    port {
      name        = "integrates"
      port        = 81
      target_port = 8001
      protocol    = "TCP"
    }
    selector = {
      "app" : "integrates-${var.deployment_name}"
    }
  }
}
