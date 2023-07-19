---
id: kubernetes
title: Kubernetes
sidebar_label: Kubernetes
slug: /development/stack/kubernetes
---

## Rationale

[Kubernetes][kubernetes]
is the system we use
for hosting, deploying and managing
our applications.
It comprises infrastructure solutions like
[RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/),
[distributed persistent storage](https://kubernetes.io/docs/concepts/storage/persistent-volumes/),
[managing resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/),
[managing DNS records](https://github.com/kubernetes-sigs/external-dns),
[managing load balancers](https://github.com/kubernetes-sigs/aws-load-balancer-controller),
[autoscaling](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler),
[blue-Green deployments](https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment),
[rollbacks][rollbacks]
among many others.
It allows us to serve and scale our applications
in an easy, secure and automated way.

The main reasons why we chose
it over other alternatives are:

1. It is capable of deploying complex applications,
   including related
   [Servers](<https://en.wikipedia.org/wiki/Server_(computing)>),
   [DNS records](https://en.wikipedia.org/wiki/Domain_Name_System),
   and [load balancers](<https://en.wikipedia.org/wiki/Load_balancing_(computing)>)
   in an automated way,
   allowing us to focus
   more on the application development
   and less on the infrastructure supporting it.
1. It can be
   [fully managed](https://gitlab.com/fluidattacks/universe/-/blob/ba230133febd3325d0f5c995f638a176b89d32a2/makes/applications/makes/k8s/src/terraform/cluster.tf)
   using [Terraform](/development/stack/terraform/).
1. It supports
   [Blue-Green deployments](https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment),
   allowing us to deploy applications
   many times a day
   without service interruptions.
1. It supports
   [Rollbacks][rollbacks],
   allowing us to revert applications
   to previous versions
   in case the need arise.
1. It supports
   [Horizontal autoscaling](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler),
   allowing us to easily adapt our applications
   to the loads they're getting.
1. It supports
   [Service accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/),
   [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/),
   and [IRSA](https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/),
   allowing to give applications
   permissions to external resources
   using a
   [least privilege](/criteria/requirements/186)
   approach.
1. It supports
   [resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/),
   allowing to easily distribute containers among physical machines using
   a granular `cpu/memory per container` approach.
1. It has its own [package manager](https://helm.sh/),
   which makes deploying services
   [very easy](https://gitlab.com/fluidattacks/universe/-/blob/ba230133febd3325d0f5c995f638a176b89d32a2/makes/applications/makes/k8s/src/terraform/new-relic.tf#L5).
1. It has its own
   [local reproducibility](https://minikube.sigs.k8s.io/docs/)
   tool for simulating clusters
   in local environments.
1. It is [Open source][oss].
1. It is not platform-bounded.
1. [Azure AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/),
   [AWS EKS](/development/stack/aws/eks/),
   [GCP GKE](https://cloud.google.com/kubernetes-engine),
   support it.
1. It can be [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
   when implemented under a
   [cloud provider][cloud].
1. Migrating it from one
   [cloud provider][cloud]
   to another is,
   although not a simple task, at least possible.
1. It is
   [widely used by the community](https://enterprisersproject.com/article/2020/6/kubernetes-statistics-2020).
1. It has many
   [open source extensions](https://github.com/kubernetes-sigs).

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [AWS ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html):
   It is a serverless service
   for running containers.
   It is expensive as only one container
   exists within an entire physical machine.
   It does not support extensions.
   It is platform-bounded.
   It is not [Open source][oss].
1. [AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html):
   It is a serverless service
   for running containers
   without administering the infrastructure
   they run upon.
   It is expensive as only one container
   exists within an entire physical machine.
   It does not support extensions.
   It is platform-bounded.
   It is not [Open source][oss].
1. [AWS EC2](/development/stack/aws/ec2):
   It is a service for cloud computing.
   [AWS EKS](/development/stack/aws/eks/)
   actually uses it for setting up cluster workers.
   It does not support extensions.
   It is platform-bounded.
   It is not [Open source][oss].
1. [HashiCorp Nomad](https://www.nomadproject.io/):
   Currently, no
   [cloud provider][cloud]
   supports it,
   which means that having to manage
   both managers and workers is required.
   It takes a simpler approach
   to orchestrating applications,
   with the downside of losing flexibility.
1. [Docker Swarm](https://www.sumologic.com/glossary/docker-swarm/):
   Currently, no
   [cloud provider][cloud]
   supports it,
   which means that having to manage
   both managers and workers is required.
   It takes a simpler approach
   to orchestrating applications,
   with the downside of losing flexibility.

## Usage

We use [Kubernetes][kubernetes] for:

1. [Hosting](https://gitlab.com/fluidattacks/universe/-/tree/4ad18b78c630878afdafbf192fcbf54c7bc7a006/makes/foss/units/integrates/back/deploy/prod/k8s)
   our
   [Platform][asm].
1. [Automatically](https://gitlab.com/fluidattacks/universe/-/blob/ba230133febd3325d0f5c995f638a176b89d32a2/makes/applications/integrates/back/deploy/dev/entrypoint.sh)
   deploying
   [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments)
   on
   [CI/CD](https://docs.gitlab.com/ee/ci/introduction/)
   workflows.
1. [Automatically deploying DNS records](https://gitlab.com/fluidattacks/universe/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/dns.tf)
   for applications.
1. [Automatically deploying load balancers](https://gitlab.com/fluidattacks/universe/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/alb.tf)
   for applications.
1. [Automatically scaling worker nodes](https://gitlab.com/fluidattacks/universe/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/autoscaler.tf)
   based on application load.
1. Running application performance monitoring using [New Relic](https://newrelic.com/).

We do not use [Kubernetes][kubernetes] for:

1. [Rollbacks][rollbacks]:
   We should version production artifacts
   in order to be able to automatically
   return to a previous working version
   of our applications.
1. [Gitlab Runner](https://docs.gitlab.com/runner/executors/kubernetes.html):
   It was slow,
   unreliable
   and added too much overhead to workers.
   We decided to go back to
   [Autoscaling Runner](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/).
1. [Chaos Engineering](https://github.com/chaos-mesh/chaos-mesh/):
   In order to harden ourselves against errors,
   we should create a little chaos in our infrastructure.

## Guidelines

### General

1. Any changes to the
   [cluster](https://gitlab.com/fluidattacks/universe/-/tree/4ad18b78c630878afdafbf192fcbf54c7bc7a006/makes/foss/modules/makes/kubernetes)
   infrastructure and configuration
   must be done via
   [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. Any changes related to the
   [Platform][asm]
   (deployments, autoscaling, ingress...)
   for both
   [development](https://gitlab.com/fluidattacks/universe/-/tree/4ad18b78c630878afdafbf192fcbf54c7bc7a006/makes/foss/units/integrates/back/deploy/dev/k8s)
   and
   [production](https://gitlab.com/fluidattacks/universe/-/tree/4ad18b78c630878afdafbf192fcbf54c7bc7a006/makes/foss/units/integrates/back/deploy/prod/k8s)
   must be done via
   [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure
   via [Terraform](/development/stack/terraform),
   visit the
   [Terraform Guidelines](/development/stack/terraform#guidelines).

### Components

Our cluster implements:

1. [AWS EKS Terraform module](https://github.com/terraform-aws-modules/terraform-aws-eks)
   for declaring the cluster as code
   using [Terraform](/development/stack/terraform/).
1. [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
   for automatically initializing
   [AWS load balancers](/development/stack/aws/elb/)
   when declaring
   [ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/).
1. [AWS Kubernetes Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
   for automatically scaling
   the cluster size based on
   [resource assignation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).
1. [ExternalDNS](https://github.com/kubernetes-sigs/external-dns)
   for automatically setting DNS records
   when declaring
   [ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/).
1. [Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
   for automatically scaling
   [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
   like production [Platform][asm]
   based on application load (CPU, Memory, custom metrics).
1. [New Relic](https://newrelic.com/)
   for monitoring both
   production [Platform][asm]
   and general infrastructure.

### Debugging

#### Connect to cluster

In order to connect
to the Kubernetes Cluster,
you must:

1. Login as an Integrates developer
   using [this guide](/development/stack/aws#get-development-keys).
1. Install kubectl and aws-cli with `nix-env -i awscli kubectl`.
1. Select cluster by running
   `aws eks update-kubeconfig --name common-k8s --region us-east-1`.
1. Run `kubectl get node`.

Your input should be similar to this:

```bash
$ kubectl get node
NAME                            STATUS   ROLES    AGE   VERSION
ip-192-168-5-112.ec2.internal   Ready    <none>   58d   v1.17.9-eks-4c6976
ip-192-168-5-144.ec2.internal   Ready    <none>   39d   v1.17.11-eks-cfdc40
ip-192-168-5-170.ec2.internal   Ready    <none>   20d   v1.17.11-eks-cfdc40
ip-192-168-5-35.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-5-51.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-109.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-127.ec2.internal   Ready    <none>   18d   v1.17.11-eks-cfdc40
ip-192-168-6-135.ec2.internal   Ready    <none>   31d   v1.17.11-eks-cfdc40
ip-192-168-6-151.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-221.ec2.internal   Ready    <none>   13d   v1.17.11-eks-cfdc40
ip-192-168-7-151.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-7-161.ec2.internal   Ready    <none>   33d   v1.17.11-eks-cfdc40
ip-192-168-7-214.ec2.internal   Ready    <none>   61d   v1.17.9-eks-4c6976
ip-192-168-7-48.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-7-54.ec2.internal    Ready    <none>   39d   v1.17.11-eks-cfdc40
```

#### Common commands

Most commands have the following syntax: `kubectl <action> <resource> -n <namespace>`

- Common actions are: `get`, `describe`, `logs`, `exec` and `edit`.
- Common resources are: `pod`, `node`, `deployment`, `ingress`, `hpa`.
- Common namespaces are: `development`, `production` and `kube-system`.
  Aditionally, the `-A` flag executes `<action>` for all namespaces.

Some basic examples are:

| Command                     | Example | Description                  |
| --------------------------- | ------- | ---------------------------- |
| `kubectl get pod -A`        | `N/A`   | Get all running pods         |
| `kubectl get node -A`       | `N/A`   | Get all cluster nodes        |
| `kubectl get deployment -A` | `N/A`   | Get all cluster deployments  |
| `kubectl get hpa -A`        | `N/A`   | Get all autoscaling policies |
| `kubectl get namespace`     | `N/A`   | Get all cluster namespaces   |

Some more complex examples are:

| Command                                                             | Example                                                                               | Description                   |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------- |
| `kubectl describe pod -n <namespace> <pod>`                         | `kubectl describe pod -n development app-dsalazaratfluid-7c485cf565-w9gwg`            | Describe pod configurations   |
| `kubectl logs -n <namespace> <pod> -c <container>`                  | `kubectl logs -n development app-dsalazaratfluid-7c485cf565-w9gwg -c app`             | Get container logs from a pod |
| `kubectl exec -it -n <namespace> <pod> -c <container> -- <command>` | `kubectl exec -it -n development app-dsalazaratfluid-7c485cf565-w9gwg -c app -- bash` | Access a container within pod |
| `kubectl edit deployment -n <namespace> <deployment>`               | `kubectl edit deployment -n development integrates-dsalazaratfluid`                   | Edit a specific deployment    |

[asm]: https://fluidattacks.com/categories/arm/
[kubernetes]: https://kubernetes.io/
[rollbacks]: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment
[oss]: https://opensource.com/resources/what-open-source
[cloud]: https://en.wikipedia.org/wiki/Cloud_computing
