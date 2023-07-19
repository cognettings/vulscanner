resource "kubernetes_secret_v1" "integrates" {
  metadata {
    name      = "integrates-${var.deployment_name}"
    namespace = "prod-integrates"
  }
  data = {
    "CACHIX_AUTH_TOKEN"  = "${var.cachix_auth_token}"
    "CI_COMMIT_REF_NAME" = "${var.ci_commit_ref_name}"
    "CI_COMMIT_SHA"      = "${var.ci_commit_sha}"
    "UNIVERSE_API_TOKEN" = "${var.universe_api_token}"
  }
}
