---
slug: advisories/arcangel/
title: PaperCut MF/NG 22.0.10 (Build 65996 2023-03-27) - Remote code execution via CSRF
authors: Carlos Bello
writer: cbello
codename: arcangel
product: PaperCut MF/NG 22.0.10 (Build 65996 2023-03-27) - Remote code execution via CSRF
date: 2023-06-13 12:00 COT
cveid: CVE-2023-2533
severity: 8.4
description: PaperCut MF/NG 22.0.10 (Build 65996 2023-03-27) - Remote code execution via CSRF
keywords: Fluid Attacks, Security, Vulnerabilities, RCE, CSRF, Papercut Ng, Papercut Mf, CVE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                  |
| --------------------- | ---------------------------------------------------------------------------------|
| **Name**              | PaperCut MF/NG 22.0.10 (Build 65996 2023-03-27) - Remote code execution via CSRF |
| **Code name**         | [Arcangel](https://en.wikipedia.org/wiki/Arcángel)                               |
| **Product**           | PaperCut MF/NG                                                                   |
| **Affected versions** | Version 22.0.10 (Build 65996 2023-03-27)                                         |
| **State**             | Public                                                                           |
| **Release date**      | 2023-04-10                                                                       |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.4                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-2533](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2533)                                               |

## Description

PaperCut MF/NG version 22.0.10 allows to persuade an administrator to alter
server configurations. This is possible because the application is vulnerable
to CSRF.

## Vulnerability

A Cross-Site Request Forgery (CSRF) vulnerability has been identified in
PaperCut NG/MF, which, under specific conditions, could potentially enable
an attacker to alter security settings or execute arbitrary code. This could
be exploited if the target is an admin with a current login session. Exploiting
this would typically involve the possibility of deceiving an admin into clicking
a specially crafted malicious link, potentially leading to unauthorized changes.

## Exploitation

Will be available soon.

## Evidence of exploitation

It is important to clarify that we only need an administrator to perform the
necessary configurations with the CSRF that will later enable the RCE. This
RCE is triggered when anyone on the network sends a print job to an infected
printer.

Unlike administrators, a user without administrative privileges, within the
network where the printers are configured, will need the [Mobility Print](https://chrome.google.com/webstore/detail/mobility-print/alhngdkjgnedakdlnamimgfihgkmenbh)
extension to be able to see the printers configured by the administrator of
the PaperCut instance, and thus be able to send the print job to the infected
printer.

<iframe src="https://www.veed.io/embed/47a753c5-ab50-4310-b16a-0d5779f698ae"
width="835" height="504" frameborder="0" title="RCE-PaperCut-22.0.10"
webkitallowfullscreen mozallowfullscreen allowfullscreen controls>
</iframe>

## Our security policy

We have reserved the ID CVE-2023-2533 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: PaperCut MF/NG 22.0.10 (Build 65996 2023-03-27)

* Operating System: MacOS

## Mitigation

An updated version of PaperCut is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.papercut.com/>

**PaperCut NG/MF Security Bulletin (June 2023) | CVEs addressed** <https://www.papercut.com/kb/Main/SecurityBulletinJune2023#cves-addressed>

## Timeline

<time-lapse
  discovered="2023-05-04"
  contacted="2023-05-04"
  replied="2023-05-04"
  confirmed="2023-05-08"
  patched="2023-06-09"
  disclosure="2023-06-13">
</time-lapse>
