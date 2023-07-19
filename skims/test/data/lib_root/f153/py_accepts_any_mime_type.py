# pylint: disable-all
# type: ignore

import requests
import urllib2
import urllib as urllib_alias
from urllib import (
    request as request_alias,
)

dang_headers = {"Accept": "*/*"}
safe_headers = {"Accept": "text/html"}

# Unsafe Connections

unsafe_1 = requests.post("example.com", headers=dang_headers)

unsafe_2 = urllib_alias.request.Request("example.com", headers=dang_headers)

unsafe_3 = request_alias.urlopen("example.com", headers=dang_headers)

unsafe_4 = urllib2.Request("example.com", headers=dang_headers)

# Safe connections

safe_1 = requests.post("example.com", headers=safe_headers)

safe_2 = urllib_alias.request.Request("example.com", headers=safe_headers)

safe_3 = request_alias.urlopen("https://example.com", headers=safe_headers)

safe_4 = urllib2.Request("https://thewebsite.com", headers=safe_headers)
