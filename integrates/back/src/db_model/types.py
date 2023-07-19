from .constants import (
    CVSS_V3_DEFAULT,
    DEFAULT_INACTIVITY_PERIOD,
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    PageInfo,
)
from typing import (
    Generic,
    NamedTuple,
    TypeVar,
)

T = TypeVar("T")


class CodeLanguage(NamedTuple):
    language: str
    loc: int


class Policies(NamedTuple):
    modified_date: datetime
    modified_by: str
    inactivity_period: int | None = DEFAULT_INACTIVITY_PERIOD
    max_acceptance_days: int | None = None
    max_acceptance_severity: Decimal | None = DEFAULT_MAX_SEVERITY
    max_number_acceptances: int | None = None
    min_acceptance_severity: Decimal | None = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Decimal | None = None
    vulnerability_grace_period: int | None = None


class PoliciesToUpdate(NamedTuple):
    inactivity_period: int | None = None
    max_acceptance_days: int | None = None
    max_acceptance_severity: Decimal | None = None
    max_number_acceptances: int | None = None
    min_acceptance_severity: Decimal | None = None
    min_breaking_severity: Decimal | None = None
    vulnerability_grace_period: int | None = None


class SeverityScore(NamedTuple):
    base_score: Decimal = Decimal("0.0")
    temporal_score: Decimal = Decimal("0.0")
    cvss_v3: str = CVSS_V3_DEFAULT
    cvssf: Decimal = Decimal("0.0")


class Edge(NamedTuple, Generic[T]):
    node: T
    cursor: str


class Connection(NamedTuple, Generic[T]):
    edges: tuple[Edge[T], ...]
    page_info: PageInfo
    total: int | None = None
