from decimal import (
    Decimal,
)
from enum import (
    StrEnum,
)
from forces.model.vulnerability import (
    Vulnerability,
)
from typing import (
    NamedTuple,
)


class FindingStatus(StrEnum):
    VULNERABLE: str = "vulnerable"
    SAFE: str = "safe"


class Finding(NamedTuple):
    identifier: str
    title: str
    status: FindingStatus
    exploitability: float
    severity: Decimal
    url: str
    vulnerabilities: list[Vulnerability]
