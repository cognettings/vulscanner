---
slug: advisories/towers/
title: Faveo Helpdesk Enterprise 6.0.1 - Account Takeover via XSS
authors: Carlos Bello
writer: cbello
codename: towers
product: Faveo Helpdesk Enterprise 6.0.1 - Account Takeover via Stored XSS
date: 2023-06-23 12:00 COT
cveid: CVE-2023-1724
severity: 7.3
description: Faveo Helpdesk Enterprise 6.0.1 - Account Takeover via Stored XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Faveo Helpdesk, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------|
| **Name**              | Faveo Helpdesk Enterprise 6.0.1 - Privilege Escalation via Stored XSS                                               |
| **Code name**         | [Towers](https://en.wikipedia.org/wiki/Myke_Towers)                                                                 |
| **Product**           | Faveo Helpdesk Enterprise                                                                                           |
| **Affected versions** | Version 6.0.1                                                                                                       |
| **State**             | Public                                                                                                              |
| **Release date**      | 2023-06-23                                                                                                          |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                                                                           |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)                        |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1724](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1724)                                               |

## Description

Faveo Helpdesk Enterprise version 6.0.1 allows an attacker with agent
permissions to perform privilege escalation on the application. This occurs
because the application is vulnerable to stored XSS.

## Vulnerability

The application allows an agent to upload HTML code when attempting to upload
an image in the agent signature.

<iframe src="https://streamable.com/e/yayt90"
frameborder="0" width="835px" height="505px"
allowfullscreen></iframe>

The bad thing here is that we cannot access the session cookie from JS.
This is because the cookie has the `HttpOnly` flag. However, thanks to
XSS we can perform actions on behalf of an administrator, we can create
users with administrative permissions.

## Exploitation

Thanks to XSS and the possibility of creating users with administrative permissions.
A malicious agent can send a malicious link to the instance administrator to create
an account with administrative permissions, thus managing to elevate privileges in
the application.

<iframe src="https://streamable.com/e/951bm2"
frameborder="0" width="835px" height="505px"
allowfullscreen></iframe>

## Our security policy

We have reserved the CVE-2023-1724 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Faveo Helpdesk Enterprise 6.0.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/ladybirdweb/faveo-helpdesk/>

## Timeline

<time-lapse
  discovered="2023-03-30"
  contacted="2023-03-30"
  replied="2023-03-30"
  confirmed=""
  patched=""
  disclosure="2023-06-23">
</time-lapse>
