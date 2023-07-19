variable "cloudflareEmail" {}
variable "cloudflareApiKey" {}

resource "helm_release" "dns" {
  name       = "dns"
  repository = "https://kubernetes-sigs.github.io/external-dns/"
  chart      = "external-dns"
  version    = "1.12.2"
  namespace  = "kube-system"

  values = [
    yamlencode(
      {
        provider   = "cloudflare"
        policy     = "sync"
        registry   = "txt"
        txtOwnerId = local.cluster_name
        txtPrefix  = "${local.cluster_name}-"
        extraArgs  = ["--cloudflare-proxied"]
        env = [
          {
            name  = "CF_API_EMAIL"
            value = var.cloudflareEmail
          },
          {
            name  = "CF_API_KEY"
            value = var.cloudflareApiKey
          },
        ]
        nodeSelector = {
          worker_group = "core"
        }
      }
    )
  ]
}
