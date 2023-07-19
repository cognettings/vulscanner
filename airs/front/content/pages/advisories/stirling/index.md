---
slug: advisories/stirling/
title: OrangeScrum 2.0.11 - AWS Credentials Leak via PDF Rendering
authors: Carlos Bello
writer: cbello
codename: stirling
product: OrangeScrum 2.0.11 - AWS Credentials Leak via PDF Rendering
date: 2023-06-23 12:00 COT
cveid: CVE-2023-1783
severity: 6.5
description: OrangeScrum 2.0.11 - AWS Credentials Leak via PDF Rendering
keywords: Fluid Attacks, Security, Vulnerabilities, Orangescrum, AWS, PDF Rendering
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------|
| **Name**              | OrangeScrum 2.0.11 - AWS Credentials Leak via PDF Rendering                                                         |
| **Code name**         | [Stirling](https://en.wikipedia.org/wiki/Lindsey_Stirling)                                                          |
| **Product**           | OrangeScrum                                                                                                         |
| **Affected versions** | Version 2.0.11                                                                                                      |
| **State**             | Public                                                                                                              |
| **Release date**      | 2023-06-23                                                                                                          |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1783](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1783)                                               |

## Description

OrangeScrum version 2.0.11 allows an external attacker to remotely obtain
AWS instance credentials. This is possible because the application does
not properly validate the HTML content to be converted to PDF.

## Vulnerability

This vulnerability occurs because the application does not properly validate
the HTML content to be converted to PDF.

## Exploitation

![inject-payload-pdf.png](https://user-images.githubusercontent.com/51862990/229176351-76c91400-e865-4ab2-85e3-1f18c9850550.png)

<iframe src="https://streamable.com/e/vck5yr"
width="835" height="504" frameborder="0" title="POC-AWS-Credentials-Leak-OrangeScrum"
webkitallowfullscreen mozallowfullscreen allowfullscreen controls>
</iframe>

![aws-credentials.leak.png](https://user-images.githubusercontent.com/51862990/229174989-d7981ab9-5a71-44a6-acf3-cb3f53db8e18.png)

## Our security policy

We have reserved the CVE-2023-1783 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: OrangeScrum 2.0.11

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/Orangescrum/orangescrum/>

## Timeline

<time-lapse
  discovered="2023-03-31"
  contacted="2023-03-31"
  replied="2023-03-31"
  confirmed=""
  patched=""
  disclosure="2023-06-23">
</time-lapse>
