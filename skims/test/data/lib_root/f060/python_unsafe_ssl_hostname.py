# pylint: skip-file
import ssl

# Noncompliant: Host name verification is disabled
unsafe_ctx = ssl._create_unverified_context()
unsafe_ctx.check_hostname = False

unsafe_ctx1 = ssl.create_default_context()
unsafe_ctx1.check_hostname = False

safe_ctx = ssl._create_unverified_context()
safe_ctx.check_hostname = True  # Compliant

safe_ctx1 = ssl.create_default_context()
