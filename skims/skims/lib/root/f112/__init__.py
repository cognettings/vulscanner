from lib.root.f112.java import (
    java_sql_injection,
)
from lib.root.f112.javascript import (
    unsafe_sql_injection as js_sql_injection,
)
from lib.root.f112.typescript import (
    unsafe_sql_injection as ts_sql_injection,
)

__all__ = [
    "java_sql_injection",
    "js_sql_injection",
    "ts_sql_injection",
]
