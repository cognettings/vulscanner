from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class MetadataTableRow:
    # pylint: disable=invalid-name
    id: str
    finding_id: str
    type: str
    custom_severity: int | None
    skims_method: str | None


@dataclass(frozen=True)
class StateTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_by: str
    modified_date: datetime
    source: str
    status: str


@dataclass(frozen=True)
class TreatmentTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str
    accepted_until: datetime | None
    acceptance_status: str | None


@dataclass(frozen=True)
class VerificationTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str


@dataclass(frozen=True)
class ZeroRiskTableRow:
    # pylint: disable=invalid-name
    id: str
    modified_date: datetime
    status: str
