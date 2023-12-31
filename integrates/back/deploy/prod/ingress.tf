resource "kubernetes_ingress_v1" "integrates_ingress" {
  metadata {
    name      = "integrates-${var.deployment_name}"
    namespace = "prod-integrates"
    annotations = {
      "kubernetes.io/ingress.class"                         = "alb"
      "alb.ingress.kubernetes.io/scheme"                    = "internet-facing"
      "alb.ingress.kubernetes.io/tags"                      = "management:area=cost,management:product=integrates,management:type=product"
      "alb.ingress.kubernetes.io/load-balancer-attributes"  = "idle_timeout.timeout_seconds=60"
      "alb.ingress.kubernetes.io/security-groups"           = "CloudFlare"
      "alb.ingress.kubernetes.io/healthcheck-path"          = "/"
      "alb.ingress.kubernetes.io/success-codes"             = "200,302"
      "alb.ingress.kubernetes.io/unhealthy-threshold-count" = "6"
      "alb.ingress.kubernetes.io/listen-ports"              = "[{\"HTTP\": 80}]"
      "alb.ingress.kubernetes.io/target-node-labels"        = "worker_group=prod_integrates"
      "external-dns.alpha.kubernetes.io/cloudflare-proxied" = "true"
    }
  }
  spec {
    rule {
      host = "${var.endpoint}.fluidattacks.com"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "integrates-${var.deployment_name}"
              port {
                number = 81
              }
            }
          }
        }
      }
    }
  }
}
