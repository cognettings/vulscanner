from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingSorts,
)
from db_model.findings.types import (
    CVSS31Severity,
)
from db_model.types import (
    SeverityScore,
)
from typing import (
    NamedTuple,
)


class FindingDescriptionToUpdate(NamedTuple):
    attack_vector_description: str | None = None
    description: str | None = None
    recommendation: str | None = None
    sorts: FindingSorts | None = None
    threat: str | None = None
    title: str | None = None
    unfulfilled_requirements: list[str] | None = None


class FindingDraftToAdd(NamedTuple):
    attack_vector_description: str
    description: str
    hacker_email: str
    min_time_to_remediate: int | None
    recommendation: str
    requirements: str
    severity: CVSS31Severity
    threat: str
    title: str


class FindingAttributesToAdd(NamedTuple):
    attack_vector_description: str
    description: str
    min_time_to_remediate: int | None
    recommendation: str
    severity: CVSS31Severity
    severity_score: SeverityScore
    source: Source
    threat: str
    title: str
    unfulfilled_requirements: list[str]


class SeverityLevelSummary(NamedTuple):
    accepted: int
    closed: int
    total: int


class SeverityLevelsInfo(NamedTuple):
    critical: SeverityLevelSummary
    high: SeverityLevelSummary
    medium: SeverityLevelSummary
    low: SeverityLevelSummary


class Tracking(NamedTuple):
    cycle: int
    open: int
    closed: int
    date: str
    accepted: int
    accepted_undefined: int
    assigned: str
    justification: str
    safe: int
    vulnerable: int
