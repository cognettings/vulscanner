data "http" "alb-policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/45f9e9d89e359bf0988d74b6240ca821823110bb/docs/install/iam_policy.json"
}

resource "aws_iam_policy" "alb" {
  name_prefix = "${local.cluster_name}-alb-"
  policy      = data.http.alb-policy.response_body
}

module "alb_oidc_role" {
  source           = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version          = "5.11.1"
  create_role      = true
  role_name_prefix = "${local.cluster_name}-alb-"
  provider_url     = replace(module.cluster.cluster_oidc_issuer_url, "https://", "")

  role_policy_arns = [
    aws_iam_policy.alb.arn,
  ]

  oidc_fully_qualified_subjects = [
    "system:serviceaccount:kube-system:alb",
  ]
}

resource "kubernetes_service_account" "alb" {
  automount_service_account_token = true

  metadata {
    name      = "alb"
    namespace = "kube-system"

    annotations = {
      "eks.amazonaws.com/role-arn" = module.alb_oidc_role.iam_role_arn
    }
  }
}

resource "helm_release" "alb" {
  name       = "alb"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.4.7"
  namespace  = "kube-system"

  values = [
    yamlencode(
      {
        clusterName = local.cluster_name
        serviceAccount = {
          create = false
          name   = kubernetes_service_account.alb.metadata[0].name
          annotations = {
            "eks.amazonaws.com/role-arn" = module.alb_oidc_role.iam_role_arn
          }
        }
        nodeSelector = {
          worker_group = "core"
        }
      }
    )
  ]
}
