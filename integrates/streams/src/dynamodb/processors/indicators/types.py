from dynamodb.types import (
    Record,
    StreamEvent,
)
from typing import (
    Any,
    NamedTuple,
)


class Indicators(NamedTuple):
    STATUS: str = "unreliable_status"
    SEVERITY: str = "max_open_severity_score"
    OPEN_VULNERABILITIES: str = "open_vulnerabilities"
    CLOSED_VULNERABILITIES: str = "closed_vulnerabilities"
    SUBMITTED_VULNERABILITIES: str = "submitted_vulnerabilities"
    REJECTED_VULNERABILITIES: str = "rejected_vulnerabilities"
    OLDEST_REPORT_DATE: str = "oldest_vulnerability_report_date"
    TREATMENT_SUMMARY: str = "treatment_summary"
    NEWEST_REPORT_DATE: str = "newest_vulnerability_report_date"


class IndicatorsChecker(NamedTuple):
    record: Record
    event: StreamEvent
    vuln: Any
    finding: Any | None
    vulnerabilities: list[Any]
    current_indicators: dict[str, Any]
    new_indicators: dict[str, Any]
