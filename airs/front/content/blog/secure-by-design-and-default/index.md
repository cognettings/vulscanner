---
slug: secure-by-design-and-default/
title: Secure-by-Design and -Default
date: 2023-04-19
subtitle: A roadmap for developing and releasing secure software
category: politics
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1681918218/blog/secure-by-design-and-default/cover_secure_by_design_and_default.webp
alt: Photo by Ludovic Toinel on Unsplash
description: CISA and other agencies published a guide encouraging organizations to offer their customers secure-by-design and secure-by-default products.
keywords: Secure By Design, Secure By Default, Cisa, Fbi, Nsa, Secure Software Development, Secure Code Review, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/nGwyaWKFRVI
---

The Cybersecurity and Infrastructure Security Agency
(CISA) made an [important publication on April 13](https://www.cisa.gov/resources-tools/resources/secure-by-design-and-default).
Together with the National Security Agency (NSA),
Federal Bureau of Investigation (FBI)
and the cybersecurity authorities of New Zealand,
Netherlands, Germany, United Kingdom, Canada and Australia,
it created and released the guide
"[Shifting the Balance of Cybersecurity Risk](https://www.cisa.gov/sites/default/files/2023-04/principles_approaches_for_security-by-design-default_508_0.pdf):
Principles and Approaches for Security-by-Design and -Default,"
aimed especially at IT manufacturers.
This guide includes technical recommendations and core principles
to orient organizations toward incorporating security
from the early stages of the software development lifecycle (SDLC)
in order to build and deliver more secure products to customers.

If the governments of developed countries submit proposals such as this one,
encouraging or urging manufacturers to secure their products,
it's because they see their intervention as necessary.
What is happening is that
a good many technology providers are still lagging behind
in securing the products they develop and market.
They deliver their products to their customers,
who are usually in charge of monitoring their security
and reducing and responding to cyber risks.
As time goes by,
more and more vulnerabilities appear in the technology provided to customers,
who must keep an eye on patch updates and their installation.
Unfortunately,
multiple vendors still have security below functionality and time-to-market
in priority levels.
This is what government agencies and companies like ours
intend to help transform.

In short,
within the proposal referenced here,
"the authoring agencies urge manufacturers
to revamp their design and development programs
to permit only Secure-by-Design and -Default products
to be shipped to customers."
These products would have the security of customers as a fundamental objective
and, at the time of use, would not require configuration changes
or additional payments for features in favor of security.
More of the burden or commitment to security
in preventing misconfigurations and weaknesses
should fall on the manufacturers than on the customers.
Today,
[security should be seen by everyone as a quality requirement](../code-quality-and-security/).
A company will not stand out just by how appealing its products are
in terms of functionality
but also of security.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/secure-code-review/"
title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>
</div>

## Secure-by-Design

The authoring agencies encourage manufacturers
to recognize the cyber threats facing their products
and implement good development practices and defenses against them.
This requires making security a business priority
and investing resources in core features and mechanisms
that put customer protection first.
While this certainly increases costs
in the initial phases of the SDLC for manufacturers,
long-term maintenance costs are reduced.
Although vulnerabilities may inevitably continue to emerge in their products,
ideally,
lots of security issues,
many of which are "due to a relatively small subset of root causes,"
could be prevented.

For the Secure-by-Design objective,
the authoring agencies promote using NIST Special Publication 800-218,
"[Secure Software Development Framework](https://docs.fluidattacks.com/criteria/compliance/nistssdf)"
(SSDF).
Applying this set of best practices for secure software development
enables companies to identify,
remove and prevent security vulnerabilities
and mitigate the risks they pose.
Based primarily on the SSDF,
the agencies suggest,
for example:

- Employ [memory-safe programming languages](https://media.defense.gov/2022/Nov/10/2003112742/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF)
  (e.g., C#, Java, Ruby),
  which automatically manage memory
  and don't require the developer
  to add code for memory protection.

- Use new architectural features,
  such as those of the [CHERI research project](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/),
  which allow "fine-grained memory protection
  and highly scalable software compartmentalization"
  to limit the impact of vulnerability exploitation.

- Design infrastructure that allows the whole system to be unaffected
  when a security control is compromised.

- Acquire and maintain secure third-party software components
  (commercial or open-source).

- Generate a Software Bill of Materials ([SBOM](../sca-scans/))
  or detailed inventory of components or resources used in the software
  and their dependencies.

- Require peer review of the code by other developers.

- Apply static and dynamic application security testing
  ([SAST and DAST](../differences-between-sast-sca-dast/))
  to assess source code and software behavior, respectively,
  and detect misconfigurations and vulnerabilities to be remediated.

- Establish vulnerability disclosure programs
  oriented to researchers that can identify security issues
  and ensure that published [CVEs](../../compliance/cve/)
  contain the root cause
  or common weakness enumeration ([CWE](../../compliance/cwe/)).

- Comply with basic cybersecurity practices
  such as those outlined in [CISA's Cybersecurity Performance Goals](https://www.cisa.gov/cross-sector-cybersecurity-performance-goals).

Practices such as these,
especially for companies just getting started with cybersecurity,
can be implemented gradually,
first addressing,
for instance,
critical infrastructure and products and new software.

## Secure-by-Default

The authoring agencies urge manufacturers
to deliver products that the end users do not have to struggle
to protect against known and prevalent risks.
These products,
by default,
should come with sufficiently secure configurations.
Responsibility for security should fall first and foremost
on the product deliverer's shoulders,
and security controls should not represent an additional cost to customers.
As the agencies say,
manufacturers should incorporate such controls "in the base product
like seatbelts are included in all new cars.
Security is not a luxury option
but is closer to the standard every customer should expect
without negotiating or paying more."

In addition to Secure-by-Design practices,
the authoring agencies suggest manufacturers
prioritize Secure-by-Default configurations for their software
and provide them recommendations such as the following:

- Offer products that require establishing solid passwords
  during installation and configuration,
  as well as multi-factor authentication (MFA) for privileged users.

- Implement single sign-on (SSO) technology
  so that users can enter their login credentials only once
  to gain access to all the services they are allowed to use.

- Provide high-quality audit logging.
  (In this process,
  activities or incidents within the software are documented
  with details such as time of occurrence,
  responsible parties and impacts).

- Deliver recommendations on role-based access controls or authorizations,
  as well as warnings in cases of non-compliance.

- Do not include backward-compatible legacy features in the products.

- Significantly reduce the size of the "hardening guides"
  (expectations of secure configuration and handling of the product
  to be achieved by customers)
  by integrating many of their components
  into the product's default configuration.

Some of these latter practices require customers' input,
so it is also suggested to manage with them significant incentives
(e.g., listing potential risks)
in favor of adopting improved security standards.

## Final recommendations

The document referenced here concludes with recommendations
for software manufacturers' customers.
Perhaps the most relevant advice is encapsulated
in the following sentence:
"\[The\] authoring agencies recommend that
organizational executives prioritize the importance
of purchasing Secure-by-Design and Secure-by-Default products."

A growing number of organizations will tie up their success
with the security of their products and systems.
If your company,
whether a software developer and/or supplier,
is considering committing to Secure-by-Design and -Default practices,
Fluid Attacks offers you a comprehensive security testing service:
[Continuous Hacking](../../plans/).
Using manual and automated techniques such as SAST,
DAST, SCA and CSPM,
we contribute to making your products free of vulnerabilities
from the earliest stages of the SDLC.

If you want more details on the proposal from CISA and the other agencies,
check out their [full PDF here](https://www.cisa.gov/sites/default/files/2023-04/principles_approaches_for_security-by-design-default_508_0.pdf).
To read about issues related to the security of your code,
visit our series of posts on [secure code review](../../secure-code-review/).
