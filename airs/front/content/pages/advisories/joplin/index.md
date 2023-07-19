---
slug: advisories/joplin/
title: PartKeepr v1.4.0 url attachment 'add parts' - SSRF
authors: Oscar Uribe
writer: ouribe
codename: joplin
product: PartKeepr v1.4.0
date: 2022-01-04 14:00 COT
cveid: CVE-2022-22702
severity: 4.3
description: PartKeepr v1.4.0 url attachment 'add parts' - SSRF
keywords: Fluid Attacks, Security, Vulnerabilities, PartKeepr
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                    |                                                     |
|--------------------|-----------------------------------------------------|
| **Name**           | PartKeepr v1.4.0 url attachment 'add parts' - SSRF  |
| **Code name**      | [Joplin](https://en.wikipedia.org/wiki/Janis_Joplin)|
| **Product**        | PartKeepr                                           |
| **Versions**       | v1.4.0                                              |
| **State**          | Public                                              |
| **Release date**   | 2022-01-09                                          |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Server Side Request Forgery                                      |
| **Rule**              | [100. Server-side request forgery (SSRF)](https://docs.fluidattacks.com/criteria/vulnerabilities/100)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N                                                                                        |
| **CVSSv3 Base Score** |   4.3                                                            |
| **Exploit available** |   No                                                             |
| **CVE ID(s)**         | [CVE-2022-22702](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22702)                   |

## Description

In PartKeepr versions up to and including 1.4.0, the functionality to
upload attachments using a URL when creating a part does not validate that
requests can be made to local ports, allowing an authenticated user
to carry out SSRF attacks and port enumeration.

## Proof of Concept

- Go to 'Add Part'.
- Click on 'Attachments'.
- Click on 'Add'.
- Fill the 'URL' field with an url using a local port "http://127.0.0.1:3306".
- Click on 'Upload'.
- Click on the uploaded file in order to download the file and see the content.

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-01-04 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of Fluid Attacks.

## References

**Vendor page** <https://partkeepr.org/>

**Issue** <https://github.com/partkeepr/PartKeepr/issues/1230/>

## Timeline

<time-lapse
  discovered="2022-01-03"
  contacted="2022-01-04"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-01-09">
</time-lapse>
