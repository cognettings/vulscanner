---
slug: healthcare-clouds/
title: Healthcare in the Clouds
date: 2017-04-27
category: opinions
subtitle: Cloud based systems in healthcare and their issues
tags: cloud, cybersecurity, compliance
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330889/blog/healthcare-clouds/cover_b77ciq.webp
alt: several balloons floating in the air
description: Cloud-based systems can be of great benefit to healthcare institutions, but they can also lead to security issues that must be handled and that we explain here.
keywords: Health Care, Cloud, Information, Risks, Security, Protect, Pentesting, Ethical Hacking
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
source: https://unsplash.com/photos/DuBNA1QMpPA
---

The healthcare nowadays is in the clouds, and not just the prices. With
the fast pace in which technology advances and the many different
solutions that are offered to all types of users, enterprises across all
sectors are either in the cloud, transitioning to the cloud, or thinking
about making the idea of cloud a reality. Hospitals and healthcare
providers are no exception. The cloud provides near real time, accurate
exchange of information to support a variety of health care
scenarios—which is the objective of the Health Information Technology
for Economic and Clinical Health Act (`HITECH` Act), (Filkins, 2011).

<div class="imgblock">

![healthcare](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330888/blog/healthcare-clouds/image1_enepic.webp)

<div class="title">

Figure 1. Healthcare in the cloud

</div>

</div>

The first steps hospitals took into migrating to the cloud was `SaaS`
(Software as a Service). "\`SaaS\` is a way of delivering applications
over the Internet as a service. Instead of installing and maintaining
software, you simply access it via the Internet, freeing yourself from
complex software and hardware management" (Salesforce, 2016). Now we are
one step further, the cloud.

Hospitals handle sensitive patient information and therefore have to
abide by a series of laws that were put in place in order to assure
privacy, secure access to that information and reduce fraud. Migrating
to the cloud raises some concerns regarding those exact issues. Since
all healthcare organizations are obligated to comply with these laws,
the compliance itself not only brings the biggest risks but also poses
the biggest challenge, whether it be in a server room down the hall or
in the cloud.

Different countries have different laws in place that all hope to
achieve the same objective but may differ in some aspects. In this
article we will be talking about the security risk implied in the
transition of hospitals and other healthcare organizations to the cloud
but focused only on the United States law and healthcare providers.

## Health Information Technology for Economic and Clinical Health Act (HITECH)

The `HITECH` act was created in 2009 to stimulate the adoption of
electronic health records (`EHR`) and supporting technology in the
United States. This act stipulates that beginning in 2011, healthcare
providers would be offered financial incentives for demonstrating
"meaningful use" of `EHRs` until 2015, after which time penalties may be
applied for failing to demonstrate such use (Rouse, 2015).

## The Health Insurance Portability and Accountability Act (HIPAA)

The `HIPAA` act provides data privacy and security provisions for
safeguarding medical information. This is intended to guarantee the
privacy of medical information. This act is not directly related to
`HITECH` but they both reinforce each other in some aspects (Rouse,
2015).

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/devsecops/"
title="Get started with Fluid Attacks' DevSecOps solution right now"
/>
</div>

## Compliance in the Cloud

Chris Bowen, founder of `ClearDATA`, says there are three main focus
areas for `HIPAA` and `HITECH` regulations related to technology: 1.
Administrative controls: Policies must be in place to determine who has
access to what data. 2. Technical controls: Rules must be in place to
secure data. 3. Physical controls: Standards for physical access to data
and infrastructure resources must be abided by (Butler, 2016).

With the right precautions all of these regulations can be met in a
cloud environment. The majority of public clouds now offer a monitoring
and log functionality. Within the functionality, depending on the cloud,
you can also set up alarms to flag and report any unusual activity. That
covers the administrative controls. If the cloud you choose doesn’t
offer encryption then you aren’t looking at the right options. Clouds
also offer the possibility to deploy virtual security controls such as
an `IDS`, a `WAF` or even a `DLP`. With all data encrypted in the cloud
and some security controls deployed, depending on your needs, you can
cover the technical controls. Finally, most cloud providers offer
assurances to customers regarding physical access to the data centers
hosting their clouds. In this case you are transferring the risk to a
third party but based on the `SLA` they are obligated to meet and
therefore satisfying the physical controls.

## Fraud and Cloud. Friends or foes?

Now that we can check off compliance we are left with fraud, the other
big risk. With the migration to the cloud, it is not only your
application but also your data that leaves your sight, which means it is
no longer protected by whatever perimeter protection you had previously
set up. This combined with the fact that cloud enables users to access
information from various devices and various locations makes identity
and access management more challenging and leaves room for fraud.

Medical identity fraud, which has affected an estimated `1.5` million
Americans, and Financial fraud, which is estimated at `$5` billion
annually only in New York, are amongst the most popular types of fraud
(Filkins, 2011).

In the cloud, identity becomes the key to maintaining security,
visibility and control (Filkins, 2011). To solve the identity and access
management problem we need to stop the proliferation of user
credentials. When a system uses multiple credentials for one user, the
user tends to forget and lose them. A Single Sign On (`SSO`) technology
gives us a solution. A SSO in an authentication service that allows a
user to use one set of credential to access multiple applications.

`SSO` on its own is not enough, audits are the Robin to our `SSO` Batman
and the periodic auditing of all accesses and critical transactions will
complete the battle against fraud. This by no means implies that a `SSO`
service and audits will guarantee that you are going to be fraud free,
it is just a strong strategy and a very good start.

"The allure of on-demand cloud services combined with advances in cloud
security have transformed the healthcare `IT` mindset from “Why move to
the public cloud?” to “What should we move, how do we do it?”"
(ClearDATA, 2016).

Technology advances everyday, your enterprise must keep up with it. Here
is a great article that gives you [9 Tips on securing your hospital’s
information on the
cloud](http://www.networkworld.com/article/3121967/cloud-computing/9-keys-to-having-a-hipaa-compliant-cloud.html)

## References

1. [Why this hospital is moving to Amazon’s
   cloud](http://www.networkworld.com/article/3121957/cloud-computing/why-this-hospital-is-moving-to-amazon-s-cloud.html).

2. [ClearDATA. 5 Risks Hospitals Face When Using The Public
   Cloud](https://assets.sourcemedia.com/2c/ec/ab05b5b44513a7fc8170f0f6f75e/5-risks-hospitals-face-when-using-the-public-cloud-hit.pdf).

3. [Filkins, B. Cloudy with a Chance of Better Health
   Care](https://www.sans.org/reading-room/whitepapers/analyst/cloudy-chance-health-care-security-compliance-fundamentals-protecting-e-h-35055).

4. [Rouse, M. HIPAA, Health Insurance Portability and Accountability
   Act](http://searchhealthit.techtarget.com/definition/HITECH-Act).

5. [Rouse, M. HITECH
   Act](http://searchhealthit.techtarget.com/definition/HITECH-Act).

6. [Salesforce. SaaS: Software as a
   Service](https://www.salesforce.com/saas/).
