# pylint: skip-file
import requests  # type: ignore
import ssl

# Non compliant: Certificate validation is disabled
requests.request("GET", "https://example.domain", verify=False)
requests.get("https://example.domain", verify=False)

# Compliant: Certificate validation is enabled (Either by default or explicit)
requests.request("GET", "https://example.domain")
requests.get("https://example.domain", verify=True)

# Noncompliant: by default certificate validation is not done
unsafe_ctx = ssl._create_unverified_context()
unsafe_ctx.verify_mode = ssl.CERT_NONE

unsafe_ctx1 = ssl.create_default_context()
unsafe_ctx1.verify_mode = ssl.CERT_NONE  # Noncompliant


safe_ctx = ssl.create_default_context()
safe_ctx.verify_mode = ssl.CERT_REQUIRED
