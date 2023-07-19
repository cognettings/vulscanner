variable "cluster_name" {
  default = "common-k8s"
}

variable "cluster_ca_certificate" {}

variable "cluster_endpoint" {}

variable "endpoint" {}

variable "ci_commit_sha" {}

variable "ci_commit_ref_name" {}

variable "cachix_auth_token" {}

variable "uuid" {}

variable "universe_api_token" {}

variable "replicas" {
  type = number
}

variable "deployment_name" {
  default = "trunk"
}
