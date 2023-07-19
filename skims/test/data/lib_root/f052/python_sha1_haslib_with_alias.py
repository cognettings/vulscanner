# pylint: skip-file
# type: ignore

from hashlib import (
    sha1 as danger,
)

# Unsafe line 9 must be marked
m = danger()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
m.digest()

# unsafe line 15 must be marked
danger("Sensitive DATA")
