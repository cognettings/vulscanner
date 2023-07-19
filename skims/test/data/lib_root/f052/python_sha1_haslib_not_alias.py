# pylint: skip-file
# type: ignore
import hashlib

# Safe
m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
m.digest()

# Unsafe line 12 must be marked
m = hashlib.sha1()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
m.digest()

# unsafe line 18 must be marked
hashlib.sha1("Sensitive DATA")
