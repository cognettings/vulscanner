# pylint: disable-all
# type: ignore

import http
import http.client
import httplib
import httplib2
import urllib3

dang_headers = {"Accept": "*/*"}
safe_headers = {"Accept": "text/html", "Accept-Language": "*/*"}

# Unsafe cases

unsafe_1 = http.client.HTTPSConnection("www.example.com")
unsafe_1.request("GET", "/", headers=dang_headers)

unsafe_2 = http.client.HTTPConnection("www.example.com")
unsafe_2.request("GET", "/", headers=dang_headers)

unsafe_3 = urllib3.PoolManager()
unsafe_3.request("POST", "example.com", headers={"Accept": "*/*"})

unsafe_4 = httplib2.Http()
unsafe_4.request("example.com", method="POST", headers=dang_headers)

unsafe_5 = httplib.HTTPSConnection("example.com")
unsafe_5.request("POST", "/oauth2/v4/token", "whatever", headers=dang_headers)

# Safe cases

safe_con = http.client.HTTPSConnection("www.example.com")
safe_con.request("GET", "/", headers=safe_headers)

http.request("POST", "example.com", body="whatever", headers=safe_headers)
