---
slug: advisories/giardino/
title: Plane v0.7.1 - Unauthorized access to files
authors: Lautaro Casanova
writer: lcasanova 
codename: giardino
product: Plane 0.7.1
date: 2023-07-14 12:00 COT
cveid: CVE-2023-2268
severity: 7.5
description: Plane v0.7.1     -    Unauthorized access to files
keywords: Fluid Attacks, Security, Vulnerabilities, Plane, Unauthorized
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                |
| --------------------- | -------------------------------------------------------------------------------|
| **Name**              | Plane v0.7.1 - Insecure file upload                                            |
| **Code name**         | [Giardino](https://es.wikipedia.org/wiki/Walter_Giardino)                      |
| **Product**           | Plane                                                                          |
| **Affected versions** | 0.7.1                                                                          |
| **State**             | Public                                                                         |
| **Release Date**      | 2023-07-14                                                                     |

## Vulnerability

|                       |                                                                                                |
| --------------------- | -----------------------------------------------------------------------------------------------|
| **Kind**              | Insecure file upload                                                                           |
| **Rule**              | [027. Unauthorized access to files](https://docs.fluidattacks.com/criteria/vulnerabilities/027)|
| **Remote**            | Yes                                                                                            |
| **CVSSv3 Vector**     | CVSS:3.0/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H                                                   |
| **CVSSv3 Base Score** | 7.5                                                                                            |
| **Exploit available** | Yes                                                                                            |
| **CVE ID(s)**         | [CVE-2023-2268](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2268)                  |

## Description

Plane version 0.7.1 allows an unauthenticated attacker to view all stored
server files of all users.

## Vulnerability

In the application users can change the photo of their avatar and upload
different types of files of different extensions which are all stored in
the same folder and there is no restriction. Any unauthenticated person
can access and download the resources. Knowing that Plane is created to
create issues on projects and manage them, this is critical, because if
bugs are reported on an application, an attacker can obtain the evidence
and files of the same issue.

## Exploit

![vulnerability-code-Plane](https://raw.githubusercontent.com/BetaH4k/Plane---CVE-0.7.1/main/Plane%20-%20information.png)

## Evidence of exploitation

By accessing the /uploads/ directory you can see all the files stored on
the server.

![vulnerability-code-Plane](https://raw.githubusercontent.com/BetaH4k/Plane---CVE-0.7.1/main/CVE-Plane-0.7.1-Information.gif)

## Our security policy

We have reserved the CVE-2023-2268 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Plane 0.7.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by
[Lautaro Casanova](https://www.linkedin.com/in/beta-casanova/)
from Fluid Attacks' Offensive Team.

## References

**Vendor page** <https://github.com/makeplane/plane>

## Timeline

<time-lapse
  discovered="2023-06-19"
  contacted="2023-06-20"
  confirmed="2023-06-23"
  patched=""
  disclosure="2023-07-14">
</time-lapse>
