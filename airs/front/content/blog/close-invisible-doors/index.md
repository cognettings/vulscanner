---
slug: close-invisible-doors/
title: Alert! 'Invisible' Doors Opened
date: 2021-10-28
subtitle: Focus on what is being more exploited
category: attacks
tags: vulnerability, hacking, software, exploit, risk, cybersecurity
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1635442529/blog/close-invisible-doors/cover_doors.webp
alt: Photo by Nastya Dulhiier on Unsplash
description: It is just a matter of updating or changing software. However, unnoticed vulnerable software equals an open door for criminals.
keywords: Attack Surface, Vulnerabilities, Remediation, Software Update, Continuous Checks, Data Breaches, Intrusion, Ethical Hacking, Pentesting
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/OKOOGO578eo
---

You have one or several digital services that can be reached from
anywhere over the Internet. You might have as well one or more wireless
devices allowing employees to access corporate services and visitors to
access resources on the Internet. These are just two examples of how
information technology enables organizations to run their operations
broadly. In either case, there is something essential to do daily:
checking whether the software components allowing users to do their work
are updated and free of vulnerabilities.

Recently, [the alert
AA21-209A](https://us-cert.cisa.gov/ncas/alerts/aa21-209a) was published
on the Cybersecurity & Infrastructure Security Agency (CISA) website,
coauthored by this organization and other American, Australian, and
British agencies. The message is simple: **there are a bunch of known
vulnerabilities that are being routinely exploited**.

In that document, you can find the details of these vulnerabilities
affecting the software of many world-renowned vendors like Microsoft,
VMware, and Fortinet, to name a few. Want to prevent a hack or data
breach? Have a look at the list, and make sure you have addressed these
CVEs. But, don’t stop there: make sure your organization has a process
to continuously check whether your software, especially the components
that can be reached from the Internet or by visitors or intruders in
your corporate network, is free from known vulnerabilities.

## Types of these often-exploited vulnerabilities

In our work with many organizations, we routinely find software
components that are vulnerable to known exploits. We always provide our
customers with the information to address these weaknesses over the
systems they entrust us for hacking. This is the main reason we wrote
this piece: aligned with the alert, we have evidence that organizations
may be more exposed than they think with the outdated software they
might have, but this is something they fail to address quickly.

<div class="imgblock">

![Top Routinely Exploited CVEs in 2020 (Source: [Alert AA21-209A - Top
Routinely Exploited
Vulnerabilities](https://us-cert.cisa.gov/ncas/alerts/aa21-209a)).](https://res.cloudinary.com/fluid-attacks/image/upload/v1635443574/blog/close-invisible-doors/table_doors.webp)

<div class="title">

Figure 1. Top Routinely Exploited CVEs in 2020 (Source: [Alert AA21-209A - Top
Routinely Exploited
Vulnerabilities](https://us-cert.cisa.gov/ncas/alerts/aa21-209a)).

</div>

</div>

What are these exposures? Let’s make a summary of what is in the alert
document.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/vulnerability-management/"
title="Get started with Fluid Attacks' Vulnerability Management solution
right now"
/>
</div>

- **Path traversal** (see Fluid Attacks Documentation: [Path
  Traversal](https://docs.fluidattacks.com/criteria/vulnerabilities/063)).
  In short, a software component can be hacked if it allows accessing
  files that are not supposed to be accessed. By using strings like
  `../` (a string used as a command to navigate across folders in an
  operative system), attackers can bypass the boundaries of the
  software and gain access to sensitive information or
  functionalities.

- **Remote code execution** (see Fluid Attacks Documentation:
  [RCE](https://docs.fluidattacks.com/criteria/vulnerabilities/004/)).
  This weakness allows, literally, the execution of code remotely. If
  a software component is vulnerable to this sort of flaw, unexpected
  actions can be triggered by an internal or external attacker.

- **Elevation of privileges** (see Fluid Attacks Documentation:
  [privilege
  escalation](https://docs.fluidattacks.com/criteria/vulnerabilities/005)).
  Usually, a wrong configuration enables users to assign themselves
  somehow rights they shouldn’t have. For instance, a bank sales
  representative might leverage this flaw to give more resources or
  authorizations than they should in their role.

Think of any of these weaknesses; they could be present in your IT
assets at some point. It might take just one of these to gain access to
a corporate network and, for instance, silently leak confidential data.
Also, it is not very difficult to think about a ransomware attack.

Closing these "invisible" doors could make a significant contribution in
managing operational and organizational risk. The steps that can be
taken to prevent the abuse of IT assets from these vulnerabilities could
save a lot of effort and money for organizations. Furthermore, these
steps would preserve the goodwill of their brands.

## Cybersecurity is a process and should be layered

Why is it essential to have continuous checks? Because cybersecurity is
not an end, and threats are evolving so fast that everything is becoming
more digital and software-mediated. Have a look at the MIT Technology
Review article "[2021 has broken the record for zero-day hacking
attacks](https://www.technologyreview.com/2021/09/23/1036140/2021-record-zero-day-hacks-reasons/)."
These numbers are worrisome, and we should ask ourselves how many
vulnerabilities are out there silently harming. Organizations need to
focus on what they can have control of and do it quickly.

Also, organizations must bear in mind that cybersecurity is not
concentrated in one or two places. Quite the opposite: cybersecurity is
distributed or layered. Although we have emphasized outdated software
here, other IT and business environment components should also be
addressed as attack surfaces. For example, there are cases in which one
information resource is, by omission, published on the Internet, and
only that allows an attacker to gain access to a supposedly protected
network. Layered cybersecurity is critical to ensure availability is
preserved, as well as integrity and confidentiality. Companies must
check whether different layers of protection are fully working.

Companies can have comprehensive support in this endeavor from other
expert organizations across all of their IT assets or cover at least the
most critical ones. This is usually more efficient and desirable, as the
independence of the third party ensures the disclosure of all flaws for
the betterment of the organization.

## What can Fluid Attacks do for you?

Fluid Attacks focuses on attacking systems
[continuously](../../services/continuous-hacking/) for proactive
defense. Our tests are performed constantly, considering the changes
made in the source code, the deployed applications, and the
infrastructure.

We aim to find all vulnerabilities
that exist across the software development lifecycle.
Yes,
we can start checking for vulnerabilities right away
when you have just begun developing your software.
We employ several techniques like static [code review](../../solutions/secure-code-review/),
looking for coding practices that inject vulnerabilities,
and dynamic [penetration testing](../../solutions/penetration-testing/)
over deployed applications and infrastructure.
In this last scenario,
the interaction between infrastructure and application
might lead to other vulnerabilities not visible in the source code.
Thus,
it is a comprehensive approach.

Organizations of all sizes can benefit from our approach by precisely
doing what we suggest in this article: closing the "invisible doors."
Our mission is to point out to our customers where these doors are and
provide them with the information to close them effectively. We also run
tests to check whether fixes have been successful.

We hope you have enjoyed this post. Let us know what you think, and
[reach out to us](../../contact-us/) if you want to know more about our
solutions.
