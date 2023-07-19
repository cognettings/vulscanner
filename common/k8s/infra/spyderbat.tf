resource "helm_release" "nanoagent" {
  name             = "nanoagent"
  repository       = "https://spyderbat.github.io/nanoagent_helm/"
  chart            = "nanoagent"
  namespace        = "spyderbat"
  create_namespace = true
  version          = "1.0.20"
  cleanup_on_fail  = true
  atomic           = true

  set {
    name  = "nanoagent.agentRegistrationCode"
    value = "987wIxAw0C65FbAQXg0n"
  }
  set {
    name  = "nanoagent.orcurl"
    value = "https://orc.spyderbat.com/"
  }
  set {
    name  = "CLUSTER_NAME"
    value = "common-k8s"
  }
}
