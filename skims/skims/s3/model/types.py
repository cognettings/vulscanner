from typing import (
    NamedTuple,
)


class Advisory(NamedTuple):
    id: str
    package_name: str
    package_manager: str
    vulnerable_version: str
    source: str
    cwe_ids: list[str] | None = None
    created_at: str | None = None
    modified_at: str | None = None
    severity: str | None = None
