variable "aspectoKey" {}
variable "telemetryhubKey" {}
variable "universeApiKey" {}

locals {
  kube_namespace = "kube-system"
}

# Auth

data "aws_iam_role" "monitoring" {
  name = local.monitoring_role
}

resource "kubernetes_service_account" "monitoring" {
  automount_service_account_token = true
  metadata {
    name      = local.monitoring_role
    namespace = local.kube_namespace

    annotations = {
      "eks.amazonaws.com/role-arn" = data.aws_iam_role.monitoring.arn
    }
  }
}

resource "kubernetes_cluster_role" "monitoring" {
  metadata {
    name = local.monitoring_role
  }

  rule {
    api_groups = [""]
    resources = [
      "endpoints",
      "nodes",
      "nodes/metrics",
      "nodes/proxy",
      "pods",
      "services"
    ]
    verbs = [
      "get",
      "list",
      "watch"
    ]
  }

  rule {
    non_resource_urls = ["/metrics"]
    verbs             = ["get"]
  }
}

resource "kubernetes_cluster_role_binding" "monitoring" {
  metadata {
    name = local.monitoring_role
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.monitoring.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.monitoring.metadata[0].name
    namespace = local.kube_namespace
  }
}


data "aws_iam_policy_document" "keda_service_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "${replace(module.cluster.cluster_oidc_issuer_url, "https://", "")}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(module.cluster.cluster_oidc_issuer_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:keda-operator"]
    }
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::205810638802:oidc-provider/${replace(module.cluster.cluster_oidc_issuer_url, "https://", "")}"]
    }

    effect = "Allow"
  }
}

resource "aws_iam_role" "keda-service-account" {
  name               = "keda_service_account"
  assume_role_policy = data.aws_iam_policy_document.keda_service_role_policy.json
}

resource "aws_iam_role_policy_attachment" "keda-attach-service-account" {
  role       = aws_iam_role.keda-service-account.name
  policy_arn = aws_iam_policy.autoscaler.arn
}


resource "kubernetes_service_account" "keda-operator" {
  metadata {
    name      = "keda-operator"
    namespace = local.kube_namespace

    labels = {
      "app.kubernetes.io/component"  = "operator"
      "app.kubernetes.io/instance"   = "keda-autoscaler"
      "app.kubernetes.io/managed-by" = "Helm"
      "app.kubernetes.io/name"       = "keda-operator"
      "app.kubernetes.io/part-of"    = "keda-operator"
      "app.kubernetes.io/version"    = "2.9.2"
      "helm.sh/chart"                = "keda-2.9.3"
    }
    annotations = {
      "eks.amazonaws.com/role-arn"     = aws_iam_role.keda-service-account.arn
      "meta.helm.sh/release-name"      = "keda-autoscaler"
      "meta.helm.sh/release-namespace" = "kube-system"
    }
  }

  automount_service_account_token = true
}

# For some reason, installing node-exporter from the Helm Chart
# https://artifacthub.io/packages/helm/prometheus-community/prometheus-node-exporter
# does not work, metrics are not sent to Prometheus and there is no error shown
resource "kubernetes_daemon_set_v1" "node_exporter" {
  metadata {
    name      = "node-exporter"
    namespace = local.kube_namespace
    labels = {
      app = "node-exporter"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "node-exporter"
      }
    }

    template {
      metadata {
        labels = {
          app = "node-exporter"
        }
      }

      spec {
        host_network = true

        affinity {
          node_affinity {
            required_during_scheduling_ignored_during_execution {
              node_selector_term {
                match_expressions {
                  key      = "worker_group"
                  operator = "In"
                  values = [
                    "dev",
                    "prod_integrates",
                    "prod_skims",
                  ]
                }
              }
            }
          }
        }

        container {
          args = [
            "--path.sysfs=/host/sys",
            "--path.rootfs=/host/root",
            "--no-collector.wifi",
            "--no-collector.hwmon",
            "--collector.filesystem.ignored-mount-points=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/pods/.+)($|/)",
            "--collector.netclass.ignored-devices=^(veth.*)$",
            "--collector.cpu"
          ]
          name  = "node-exporter"
          image = "prom/node-exporter:v1.6.0"

          port {
            container_port = 9100
            host_port      = 9100
            protocol       = "TCP"
          }

          resources {
            limits = {
              cpu    = "250m"
              memory = "180Mi"
            }
            requests = {
              cpu    = "102m"
              memory = "180Mi"
            }
          }

          volume_mount {
            mount_path        = "/host/sys"
            mount_propagation = "HostToContainer"
            name              = "sys"
            read_only         = true
          }
          volume_mount {
            mount_path        = "/host/root"
            mount_propagation = "HostToContainer"
            name              = "root"
            read_only         = true
          }
        }

        volume {
          name = "sys"
          host_path {
            path = "/sys"
          }
        }
        volume {
          name = "root"
          host_path {
            path = "/"
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "node_exporter_service" {
  metadata {
    name      = "node-exporter"
    namespace = local.kube_namespace
    annotations = {
      "prometheus.io/scrape" = "true"
      "prometheus.io/port"   = "9100"
    }
  }

  spec {
    selector = {
      app = "node-exporter"
    }

    port {
      port        = 9100
      target_port = 9100
      protocol    = "TCP"
    }
  }
}

resource "helm_release" "cert_manager" {
  name            = "cert-manager"
  description     = "Certificate manager, required to install OpenTelemtry Operator"
  repository      = "https://charts.jetstack.io"
  chart           = "cert-manager"
  version         = "1.11.0"
  namespace       = local.kube_namespace
  cleanup_on_fail = true
  atomic          = true

  values = [
    yamlencode(
      {
        installCRDs = true
        nodeSelector = {
          worker_group = "core"
        }
        cainjector = {
          nodeSelector = {
            worker_group = "core"
          }
        }
        webhook = {
          nodeSelector = {
            worker_group = "core"
          }
        }
        startupapicheck = {
          nodeSelector = {
            worker_group = "core"
          }
        }
      }
    )
  ]
}

resource "helm_release" "adot_operator" {
  name            = "adot-operator"
  description     = "OpenTelemetry Operator, scrapes metrics and sends them to AWS Managed Prometheus"
  repository      = "https://open-telemetry.github.io/opentelemetry-helm-charts"
  chart           = "opentelemetry-operator"
  version         = "0.21.2"
  namespace       = local.kube_namespace
  cleanup_on_fail = true
  atomic          = true

  values = [
    yamlencode(
      {
        nodeSelector = {
          worker_group = "core"
        }
      }
    )
  ]

  depends_on = [
    helm_release.cert_manager
  ]
}

resource "kubernetes_manifest" "adot_collector" {
  manifest = {
    apiVersion = "opentelemetry.io/v1alpha1"
    kind       = "OpenTelemetryCollector"
    metadata = {
      name      = "adot-collector"
      namespace = local.kube_namespace
    }
    spec = {
      image          = "public.ecr.aws/aws-observability/aws-otel-collector:v0.26.0"
      mode           = "deployment"
      serviceAccount = kubernetes_service_account.monitoring.metadata[0].name
      config         = <<EOT
        extensions:
          sigv4auth:
            service: "aps"
            region: "us-east-1"

        processors:
          batch:

        receivers:
          otlp:
            protocols:
              grpc:
          prometheus:
            config:
              scrape_configs:
                - job_name: 'kubernetes-nodes'
                  scheme: https

                  kubernetes_sd_configs:
                    - role: node

                  relabel_configs:
                    - action: labelmap
                      regex: __meta_kubernetes_node_label_(worker_group)
                      replacement: aws_$$${1}

                    - action: labelmap
                      regex: __meta_kubernetes_node_label_node_kubernetes_io_(instance_type)
                      replacement: aws_$$${1}

                  tls_config:
                    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                    insecure_skip_verify: true
                  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

                - job_name: 'kubernetes-cadvisor'
                  scheme: https
                  metrics_path: /metrics/cadvisor

                  kubernetes_sd_configs:
                    - role: node

                  relabel_configs:
                    - action: labelmap
                      regex: __meta_kubernetes_node_label_(worker_group)
                      replacement: aws_$$${1}

                    - action: labelmap
                      regex: __meta_kubernetes_node_label_node_kubernetes_io_(instance_type)
                      replacement: aws_$$${1}

                  tls_config:
                    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                    insecure_skip_verify: true
                  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

                - job_name: 'kubernetes-node-exporter'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_endpoints_name]
                      regex: 'node-exporter'
                      action: keep
                    - source_labels: [__meta_kubernetes_pod_node_name]
                      action: replace
                      target_label: instance

                - job_name: 'kubernetes-arm'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_service_name]
                      action: keep
                      regex: integrates-trunk
                    - source_labels: [__meta_kubernetes_service_name]
                      action: replace
                      target_label: service_name

                - job_name: 'kube-state-metrics'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_service_name]
                      action: keep
                      regex: kube-state-metrics

                - job_name: 'ci-metrics'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_service_name]
                      action: keep
                      regex: gitlab-ci-pipelines-exporter

          statsd:

        exporters:
          awsxray:
            indexed_attributes: ["graphql.operation.name", "otel.resource.deployment.environment"]
            region: "us-east-1"
          otlphttp/aspecto:
            endpoint: https://otelcol.aspecto.io
            headers:
              Authorization: ${var.aspectoKey}
          otlp/telemetryhub:
            endpoint: https://otlp.telemetryhub.com:4317
            headers:
              x-telemetryhub-key: ${var.telemetryhubKey}
          prometheusremotewrite:
            endpoint: https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-e60ff23e-bccf-4df2-bf46-745c50b45c70/api/v1/remote_write
            auth:
              authenticator: sigv4auth

        service:
          extensions: [sigv4auth]
          pipelines:
            metrics:
              receivers: [otlp, prometheus, statsd]
              processors: [batch]
              exporters: [prometheusremotewrite, otlphttp/aspecto, otlp/telemetryhub]
            traces:
              receivers: [otlp]
              processors: [batch]
              exporters: [awsxray, otlphttp/aspecto, otlp/telemetryhub]
      EOT
    }
  }

  depends_on = [helm_release.adot_operator]
}

resource "kubernetes_service_v1" "adot_collector_service" {
  metadata {
    name      = "adot-collector"
    namespace = local.kube_namespace
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = "adot-collector-collector"
    }

    port {
      name        = "grpc-port"
      port        = 4317
      target_port = 4317
      protocol    = "TCP"
    }

    port {
      name        = "statsd-port"
      port        = 8125
      target_port = 8125
      protocol    = "UDP"
    }
  }

  depends_on = [
    kubernetes_manifest.adot_collector
  ]
}

resource "helm_release" "kube_state_metrics" {
  chart      = "kube-state-metrics"
  name       = "kube-state-metrics"
  namespace  = "kube-system"
  repository = "https://prometheus-community.github.io/helm-charts"
  version    = "5.8.0"

  values = [
    yamlencode(
      {
        nodeSelector = {
          worker_group = "core"
        },
        metricAllowlist : [
          "kube_configmap_info",
          "kube_daemonset_labels",
          "kube_deployment_labels",
          "kube_deployment_status_replicas_available",
          "kube_deployment_status_replicas_unavailable",
          "kube_endpoint_info",
          "kube_horizontalpodautoscaler_labels",
          "kube_horizontalpodautoscaler_metadata_generation",
          "kube_horizontalpodautoscaler_spec_min_replicas",
          "kube_horizontalpodautoscaler_spec_max_replicas",
          "kube_horizontalpodautoscaler_status_current_replicas",
          "kube_horizontalpodautoscaler_status_desired_replicas",
          "kube_ingress_info",
          "kube_namespace_created",
          "kube_namespace_labels",
          "kube_networkpolicy_labels",
          "kube_persistentvolumeclaim_info",
          "kube_pod_container_info",
          "kube_pod_container_resource_requests",
          "kube_pod_container_resource_limits",
          "kube_pod_container_status_last_terminated_exitcode",
          "kube_pod_container_status_last_terminated_reason",
          "kube_pod_container_status_running",
          "kube_pod_info",
          "kube_pod_status_qos_class",
          "kube_pod_status_phase",
          "kube_pod_status_reason",
          "kube_secret_info",
          "kube_service_info",
          "kube_statefulset_labels",
        ]
      }
    )
  ]
}

resource "helm_release" "gitlab_ci_pipelines_exporter" {
  name       = "gitlab-ci-pipelines-exporter"
  repository = "https://charts.visonneau.fr"
  chart      = "gitlab-ci-pipelines-exporter"
  version    = "0.3.1"

  values = [
    yamlencode(
      {
        nodeSelector = {
          worker_group = "core"
        }
        config = {
          gitlab = {
            url   = "https://gitlab.com"
            token = var.universeApiKey
          }
          project_defaults = {
            output_sparse_status_metrics = false
          }
          projects = [
            {
              name = "fluidattacks/universe"
              pull = {
                environments = {
                  enabled = false
                }
                refs = {
                  branches = {
                    enabled         = true
                    regexp          = ".*atfluid$"
                    exclude_deleted = false
                  }
                  merge_requests = {
                    enabled = false
                  }
                }
                pipeline = {
                  jobs = {
                    enabled = true
                    runner_description = {
                      enabled = false
                    }
                  }
                }
              }
            }
          ]
        }
      }
    )
  ]
}
