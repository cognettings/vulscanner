---
slug: advisories/indio/
title: Plane 0.7.1 - Insecure file upload
authors: Lautaro Casanova
writer: lcasanova 
codename: indio
product: Plane 0.7.1
date: 2023-07-14 12:00 COT
cveid: CVE-2023-30791
severity: 7.1
description: Plane v0.7.1 - Insecure file upload allows XSS exploitation
keywords: Fluid Attacks, Security, Vulnerabilities, Plane, File Upload
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                |
| --------------------- | -------------------------------------------------------------------------------|
| **Name**              | Plane v0.7.1 - Insecure file upload                                            |
| **Code name**         | [Indio](https://es.wikipedia.org/wiki/Patricio_Rey_y_sus_Redonditos_de_Ricota) |
| **Product**           | Plane                                                                          |
| **Affected versions** | 0.7.1                                                                          |
| **State**             | Public                                                                         |
| **Release Date**      | 2023-07-14                                                                     |

## Vulnerability

|                       |                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------|
| **Kind**              | Insecure file upload                                                                   |
| **Rule**              | [027. Insecure file upload](https://docs.fluidattacks.com/criteria/vulnerabilities/027)|
| **Remote**            | Yes                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.0/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H                                           |
| **CVSSv3 Base Score** | 7.1                                                                                    |
| **Exploit available** | Yes                                                                                    |
| **CVE ID(s)**         | [CVE-2023-30791](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-30791)        |

## Description

Plane version 0.7.1-dev allows an attacker to change the avatar of his
profile, which allows uploading files with HTML extension that interprets
both HTML and JavaScript.

## Vulnerability

The vulnerability arises when uploading files other than JPG and PNG which
it says is allowed, since files of all file extensions and sizes can be
uploaded and stored without validation. Then an attacker can upload an HTML
file as a profile avatar, and it may contain malicious JavaScript code stored
with which they can steal session cookies from users and the administrator.

## Exploit

![vulnerability-code-Plane](https://raw.githubusercontent.com/BetaH4k/Plane---CVE-0.7.1/main/exploit%20-%20file.png)

## Evidence of exploitation

Log in with any user and go to the menu and go to
"Settings -> General -> Logo (Upload)" we create a
file with HTML extension which inside sends in a
request to an attacker's server the user's cookies.

Once the attacker obtains the cookies he can use them to
log into the user's account and as seen in this example
gain full control of the account to delete, create, view.

![vulnerability-code-Plane](https://raw.githubusercontent.com/BetaH4k/Plane---CVE-0.7.1/main/CVE-Plane%20-%20file%20upload.gif)

## Our security policy

We have reserved the CVE-2023-30791 to refer to this issue from now on.

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
  discovered="2023-06-16"
  contacted="2023-06-16"
  confirmed="2023-06-23"
  patched=""
  disclosure="2023-07-14">
</time-lapse>
