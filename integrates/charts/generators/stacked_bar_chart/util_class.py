from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)

# Constants
DATE_FMT: str = "%Y - %m - %d"
DATE_SHORT_FMT: str = "%Y-%m"
DATE_WEEKLY_FMT: str = "%y-%m-%d"
MIN_PERCENTAGE: Decimal = Decimal("15.0")


class TimeRangeType(str, Enum):
    MONTHLY: str = "MONTHLY"
    QUARTERLY: str = "QUARTERLY"
    SEMESTERLY: str = "SEMESTERLY"
    WEEKLY: str = "WEEKLY"
    YEARLY: str = "YEARLY"


# Let's no over think it
MONTH_TO_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

DISTRIBUTION_OVER_TIME: list[str] = [
    "date",
    "Closed",
    "Accepted",
    "Open",
]

RISK_OVER_TIME: list[str] = [
    "date",
    "Closed",
    "Accepted",
    "Reported",
]

EXPOSED_OVER_TIME: list[str] = [
    "date",
    "Exposure",
]


class RiskOverTime(NamedTuple):
    monthly: dict[str, dict[datetime, Decimal]]
    quarterly: dict[str, dict[datetime, Decimal]]
    semesterly: dict[str, dict[datetime, Decimal]]
    time_range: TimeRangeType
    weekly: dict[str, dict[datetime, Decimal]]
    yearly: dict[str, dict[datetime, Decimal]]


class AssignedFormatted(NamedTuple):
    accepted: Decimal
    accepted_undefined: Decimal
    closed_vulnerabilities: Decimal
    open_vulnerabilities: Decimal
    remaining_open_vulnerabilities: Decimal
    name: str


# Typing
GroupDocumentData = NamedTuple(
    "GroupDocumentData",
    [
        ("accepted", Decimal),
        ("closed", Decimal),
        ("opened", Decimal),
        ("date", datetime),
        ("total", Decimal),
    ],
)
