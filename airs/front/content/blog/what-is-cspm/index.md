---
slug: what-is-cspm/
title: What Is CSPM?
date: 2023-04-14
subtitle: The basics of cloud security posture management
category: philosophy
tags: cybersecurity, security-testing, cloud, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1681501483/blog/what-is-cspm/cover_cspm.webp
alt: Photo by James Beheshti on Unsplash
description: Cloud security posture management involves vulnerability assessment, prioritization and remediation to secure cloud-based systems and infrastructures.
keywords: What Is Cloud Security Posture Management, Cloud Security Posture Management, Cspm, Cloud Security, Security Testing, Remediation, Prioritization, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/CNU5avzgzKg
---

## Definition of CSPM

[Cloud security posture management](../../product/cspm/) (CSPM)
is the process of assessing cloud-based systems and infrastructures
for noncompliance with security requirements,
as well as prioritizing
and [remediating](../vulnerability-remediation-process/) such issues.
Thus,
CSPM goes beyond [vulnerability assessment](../vulnerability-assessment/),
as it involves not only identifying,
classifying and reporting security issues,
but also addressing them strategically
to reduce risks to information security.
Taken together,
these activities comprise a [vulnerability management](../what-is-vulnerability-management/)
process.

## How does CSPM work?

At Fluid Attacks,
we offer CSPM to secure your cloud-based assets continuously.
It is available in both of our [Continuous Hacking](../../services/continuous-hacking/)
[plans](../../plans/) (Machine Plan and Squad Plan)
and is included in our [21-day free trial](https://app.fluidattacks.com/SignUp)
of automated security testing (which is [CASA-approved](../casa-approved-static-scanning/)).
The CSPM process starts with [vulnerability scanning](../vulnerability-scan/)
in systems that are undergoing continuous changes.
The targets of evaluation (ToE) of such scans are infrastructure as code (IaC)
scripts (e.g., those written Terraform, AWS CloudFormation),
container images (e.g., Docker files, Docker Compose files)
and runtime environments.

The purpose of the **cyclical assessment** is
to find out about the security status of the targeted systems.
Assessments imply the identification,
classification
and report of security weaknesses or vulnerabilities.
And since organizations' software and threat landscapes are evolving nonstop,
these assessments are something to be done repeatedly
and starting as early as possible in the software development lifecycle (SDLC).
Some issues that can be detected performing CSPM are unrestricted ports,
unencrypted data, excessive privileges, exposed credentials,
among many others.

As a basis for assessment,
CSPM tools may use requirements taken from international security standards
and guidelines
(e.g., PCI DSS, HIPAA, GDPR, NIST, NYDFS, CIS, SOC 2).
For example,
we check for compliance with our curated,
ever-evolving [set of security requirements](https://docs.fluidattacks.com/criteria/requirements/).
Further,
tools in the market may allow the systems' owners
to set their organizations' internal policies.
In our case,
we let our clients configure which vulnerabilities to accept
(for a while or permanently),
and offer a DevSecOps agent that clients can run in their CI/CD pipelines
to automatically enforce acceptance policies.
Specifically,
this agent can be set to break the build if it identifies risky deployments
(i.e., those containing vulnerabilities
that the systems' owners have decided not to tolerate).

The step following assessment is **prioritization**
of the detected security issues for remediation.
A proficient CSPM solution should offer a method
(e.g., [risk-based scoring](https://try.fluidattacks.tech/report/cvssf/))
to identify which security posture weaknesses to solve first.
For instance,
we inform the assessed systems' owners of the risk exposure
that each security issue represents
with our [CVSSF metric](../cvssf-risk-exposure-metric/),
which introduces adjustments to the CVSS score.
This information is delivered through our [platform](../../platform/).
Among the platform's many features,
there are analytics that help decision-making to prioritize remediation.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/vulnerability-management/"
title="Get started with Fluid Attacks' Vulnerability Management solution
right now"
/>
</div>

**Remediation** is effectively correcting cybersecurity issues.
We talked about it in a [previous blog post](../vulnerability-remediation-process/),
where we also explained that,
when it is not possible to remediate a vulnerability,
then the options of mitigating or accepting it should be looked into.
Ideally,
though,
remediation should always be preferred.
Cloud security posture management solutions are expected
to offer remediation recommendations.
We make those available on the platform,
as part of the details of every security issue we report.
Additionally,
we provide the corresponding links to our [Documentation](https://docs.fluidattacks.com/),
where we show examples of compliant and noncompliant code.
After remediating,
our clients can just run the scan again to verify if their efforts were effective.

## Why is CSPM important?

Moving to the cloud is a very promising decision for organizations,
especially when benefiting from the offerings of cloud service providers,
as their solutions include tools, infrastructure, storage and processing power.
Thanks to these features,
development companies can create scalable software and save on costs.
However,
our experience in security assessment has taught us
that cloud service misconfigurations are a very common issue.
In the framework of the cloud security [shared responsibility model](../shared-responsibility-model/)
(SRM),
organizations need to make sure
that they use secure configurations.
Cloud security posture management is a valuable tool
to learn whether this is the case
and understand what needs to be done in case of noncompliance.

Another trend that justifies the implementation of CSPM
is the increasing use of IaC and containers.
The former refers to files containing editable scripts to provision
and manage infrastructure resources (e.g., those in public clouds),
and can therefore work as an application.
Containers,
on the other hand,
are functional and portable computing environments
with application source code,
software dependencies,
binaries
and configuration files
that allow users to run the application reliably
in a virtualized operating system.
Several vulnerabilities may appear in IaC and container images
(i.e., the static files with sets of instructions to create containers).
It could happen that malicious code is inserted into files
in supply chain attacks
or proprietary source code itself is insecure.

Implementing CSPM,
ultimately,
helps organizations manage risks such as unauthorized access,
account hijacking,
improper use of identities and cloud entitlements,
and external data sharing.

At Fluid Attacks,
we advise organizations to conduct [CSPM](../../product/cspm/) continuously
throughout their SDLC.
Moreover,
following the [DevSecOps](../devsecops-concept/) methodology,
we recommend
they start testing and remediating as early into development as possible.
Our [Continuous Hacking](../../services/continuous-hacking/)
Machine Plan is a service
that organizations can implement to follow these best practices
and start securing their cloud-based systems and infrastructures.
Besides,
we offer a more comprehensive plan ([Squad Plan](../../plans/)),
which,
in addition to Machine Plan's features,
includes manual source code review
and attack simulations by our ethical hackers.
We recommend this plan
to organizations who want to find complex vulnerabilities
that automated tools cannot detect.

Got any questions?
[Contact us](../../contact-us/).
