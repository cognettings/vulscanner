---
id: cloudflare
title: Cloudflare
sidebar_label: Cloudflare
slug: /development/stack/cloudflare
---

## Rationale

[Cloudflare][CLOUDFLARE]
is our [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
provider for some infrastructure solutions like
[DNSSEC][DNSSEC],
[DDoS Protection](https://www.cloudflare.com/ddos/),
[Rate limiting](https://www.cloudflare.com/rate-limiting/),
[Auto-Renewable SSL certificates](https://www.cloudflare.com/ssl/),
[Content delivery network](https://www.cloudflare.com/cdn/),
[Web Application Firewall][WAF],
[Anti-bot capabilities](https://blog.cloudflare.com/super-bot-fight-mode/),
among others.

The main reasons why we chose it
over other alternatives are:

1. Creating network and security solutions is very easy,
  as all its components are seamlessly connected.
1. It can be
  [fully managed](https://registry.terraform.io/providers/cloudflare/cloudflare/latest/docs)
  using [Terraform](/development/stack/terraform).
1. It provides highly detailed analytics regarding site traffic
  in terms of both performance and security.
1. It has the
  [Fastest privacy-focused DNS service](https://blog.cloudflare.com/announcing-1111/)
  on the market.
1. It supports [DNSSEC][DNSSEC].
1. It has easy-to-implement, auto-renewable, auto-validated
  [SSL certificates](https://www.cloudflare.com/ssl/).
1. It provides a
  [Web Application Firewall][WAF]
  with
  [Preconfigured rules](https://www.cloudflare.com/learning/security/threats/owasp-top-10/),
  [DDoS mitigation](https://www.cloudflare.com/learning/ddos/ddos-mitigation/),
  [Rate limiting](https://www.cloudflare.com/en-au/rate-limiting/),
  [Anti-bot capabilities](https://blog.cloudflare.com/super-bot-fight-mode/),
  among others.
1. It has a
  [CDN](https://www.cloudflare.com/cdn/)
  with special
  [routing protocols](https://www.cloudflare.com/products/argo-smart-routing/),
  [HTTP/3 support](https://blog.cloudflare.com/http3-the-past-present-and-future/),
  [Customizable cache TTL](https://support.cloudflare.com/hc/en-us/articles/218411427-What-does-edge-cache-expire-TTL-mean-#summary-of-page-rules-settings),
  and [datacenters all over the world](https://www.cloudflare.com/network/).
  Cache comes automatically configured
  and is customizable by just changing
  its default settings.
1. It provides
  [Workers](https://workers.cloudflare.com/),
  a serverless approach for developing applications.
  We use it for the specific purpose of configuring
  security headers for all our sites.
1. It has
  [Page rules](https://support.cloudflare.com/hc/en-us/articles/218411427-Understanding-and-Configuring-Cloudflare-Page-Rules-Page-Rules-Tutorial-)
  that allow to easily implement
  [HTTP redirections](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections),
  [Cache Rules, encryption rules](https://support.cloudflare.com/hc/en-us/articles/202775670-Customizing-Cloudflare-s-cache),
  among others.

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [Akamai](https://www.akamai.com/):
    It is not as widely used,
    resulting in less
    community support.
    It is much more expensive and setting up
    its services seems more complicated when
    comparing it to
    [Cloudflare][CLOUDFLARE].
1. [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/):
    Creating digital certificates required to also manage
    [DNS](https://www.cloudflare.com/dns/)
    validation records.
1. [AWS CloudFront](https://aws.amazon.com/cloudfront/):
    Creating distributions was very slow.
    Connecting them to a s3 bucket and maintaining such
    connection was necessary.
    A [Lambda](/development/stack/aws/lambda/)
    was required in order to support accessing URL's
    without having to specify `index.html` at the end.
    Overall speaking, too much overhead was required
    to make things work.
1. [AWS Route53](https://aws.amazon.com/route53/):
    This service does not support
    [DNSSEC][DNSSEC],
    It is not as fast or as flexible as
    [Cloudflare's DNS](https://www.cloudflare.com/dns/).
1. [AWS Web Application Firewall](https://aws.amazon.com/waf/):
    It needs to be connected to a load balancer serving
    an application, it does not work for
    [static sites](https://en.wikipedia.org/wiki/Static_web_page).
    It is not as flexible as
    [Cloudflare's Web Application Firewall][WAF].

## Usage

We use [Cloudflare][CLOUDFLARE] for:

1. [Overall network configurations](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L1).
1. [DNS Records](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L79).
1. [HTTP Redirections](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L436).
1. [Managing security headers](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L481).
1. [Managing digital certificates](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/certificates.tf).
1. [Managing rate limiting](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/rate_limit.tf).
1. [Managing CDN Cache](https://gitlab.com/fluidattacks/universe/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/airs/deploy/production/terraform/cache.tf).
1. Hosting `.com` and `.io` supported
    [TLDs](https://www.cloudflare.com/tld-policies/)
    using
    [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/)

We do not use the following
[Cloudflare][CLOUDFLARE] services:

1. [Argo Tunnel](https://www.cloudflare.com/products/argo-tunnel/):
    Pending to review.
1. [Railgun](https://www.cloudflare.com/website-optimization/railgun/):
    Only
    [supported](https://www.cloudflare.com/docs/railgun/installation.html#installation-overview)
    on apt and yum.
1. Hosting domains with `.co` and `.la` not supported
    [TLDs](https://www.cloudflare.com/tld-policies/).
    For these domains we use
    [GoDaddy](https://www.godaddy.com).

## Guidelines

1. Any changes to
    [Cloudflare's][CLOUDFLARE]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    modifying its
    [Terraform module](https://gitlab.com/fluidattacks/universe/-/tree/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[CLOUDFLARE]: https://www.cloudflare.com/
[DNSSEC]: https://www.cloudflare.com/dns/dnssec/
[WAF]: https://www.cloudflare.com/lp/ppc/waf-x/
