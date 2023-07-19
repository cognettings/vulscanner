---
id: terraform
title: Terraform
sidebar_label: Terraform
slug: /development/stack/terraform
---

## Rationale

[Terraform][terraform]
is used for writing our entire
[infrastructure stack as code](https://en.wikipedia.org/wiki/Infrastructure_as_code).

The main reasons why we chose it
over other alternatives are:

1. It is [Open source](https://opensource.com/resources/what-open-source).
1. It is Widely used by the community.
1. It Uses [HCL](https://github.com/hashicorp/hcl),
   a very easy to learn structured configuration language.
1. It is not platform-bounded.
1. It has a stateless approach to infrastructure.
   There are no master machines, agents,
   or incremental infrastructure. Instead, infrastructure
   is regenerated from scratch every time it is required.
1. Due to its stateless approach,
   parity between development and production environments
   is assured.
1. It has hundreds of open source
   [providers](https://registry.terraform.io/browse/providers)
   that give it full flexibility across many platforms.
1. It has thousands of open source
   [modules](https://registry.terraform.io/browse/modules)
   that simplify writing infrastructure and avoiding repetition.
1. Deploying infrastructure
   usually takes no longer than a few minutes.

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [Ansible](https://www.ansible.com/):
   Deployments were too slow.
1. [AWS CDK](https://aws.amazon.com/cdk/):
   It is platform-bounded.
1. [AWS Cloudformation](https://aws.amazon.com/cloudformation/):
   It is platform-bounded.
1. [Chef](https://www.chef.io/):
   It has a stateful approach to infrastructure, including
   a master machine, agents and mutable infrastructure.
1. [Pulumi](https://www.pulumi.com/):
   It is not as widely used,
   resulting in less
   [providers](https://www.pulumi.com/docs/intro/cloud-providers/),
   [modules](https://www.npmjs.com/search?q=pulumi&page=0&perPage=20)
   and overall community support.
1. [Puppet](https://puppet.com/):
   It has a stateful approach to infastructure, including
   a master machine, agents and mutable infrastructure.
1. [SaltStack](https://saltproject.io/):
   It has a stateful approach to infastructure, including
   a master machine, agents and mutable infrastructure.

## Usage

Used for every infrastructure piece
like databases, DNS records, firewall rules,
computing clusters, among others.
Some examples are:

1. [Gitlab Runners](https://gitlab.com/fluidattacks/universe/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/ci/src/terraform).
1. [DNS](https://gitlab.com/fluidattacks/universe/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/dns/src/terraform).
1. [Kubernetes](https://gitlab.com/fluidattacks/universe/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/k8s/src/terraform).
1. [Okta](https://gitlab.com/fluidattacks/universe/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/okta/src/terraform).
1. [Website](https://gitlab.com/fluidattacks/universe/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/airs/deploy/production/terraform).

We do not use [Terraform][terraform] in:

1. [AWS Redshift](/development/stack/aws/redshift/):
   Pending to implement.
1. [Gitlab](/development/stack/gitlab):
   Pending to implement.
1. [Gitlab Runner Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html):
   Pending to implement.
1. [Google Workspace](https://workspace.google.com/):
   Pending to implement.

## Guidelines

1. Test an infrastructure module with `./m <product>.<module>.test`
1. Deploy an infrastructure module with `./m <product>.<module>.apply`

[terraform]: https://www.terraform.io/

## Terraform state lock

The `Terraform state file` stores local information
regarding our infrastructure configuration,
which is used to determine
the necessary changes required to be made in the real world (terraform apply).
This state file is shared amongst team members to ensure consistency;
however, if it is not properly locked,
it can lead to data loss, conflicts, and state file corruption.

In case of conflicts with the state file, please follow the steps below:

1. Obtain the state lock id from the failed job
1. Access the `terraform_state_lock` table in DynamoDB
   by going to AWS - production in Okta
   (requires prod_integrates role)
1. Search for the ID in the Info attribute and delete the `.tfstate` item
1. Attempt to rerun the job that failed.
