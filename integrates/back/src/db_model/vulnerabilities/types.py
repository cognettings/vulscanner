from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityTechnique,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    PageInfo,
)
from serializers import (
    Snippet,
)
from typing import (
    NamedTuple,
)


class VulnerabilityTool(NamedTuple):
    name: str
    impact: VulnerabilityToolImpact


class VulnerabilityAdvisory(NamedTuple):
    cve: list[str] | None
    package: str | None
    vulnerable_version: str | None


class VulnerabilityState(NamedTuple):
    modified_by: str
    modified_date: datetime
    source: Source
    specific: str
    status: VulnerabilityStateStatus
    where: str
    commit: str | None = None
    advisories: VulnerabilityAdvisory | None = None
    reasons: list[VulnerabilityStateReason] | None = None
    other_reason: str | None = None
    tool: VulnerabilityTool | None = None
    snippet: Snippet | None = None


class VulnerabilityTreatment(NamedTuple):
    modified_date: datetime
    status: VulnerabilityTreatmentStatus
    acceptance_status: VulnerabilityAcceptanceStatus | None = None
    accepted_until: datetime | None = None
    justification: str | None = None
    assigned: str | None = None
    modified_by: str | None = None


class VulnerabilityUnreliableIndicators(NamedTuple):
    unreliable_closing_date: datetime | None = None
    unreliable_source: Source = Source.ASM
    unreliable_efficacy: Decimal | None = None
    unreliable_last_reattack_date: datetime | None = None
    unreliable_last_reattack_requester: str | None = None
    unreliable_last_requested_reattack_date: datetime | None = None
    unreliable_reattack_cycles: int | None = None
    unreliable_report_date: datetime | None = None
    unreliable_treatment_changes: int | None = None


class VulnerabilityVerification(NamedTuple):
    modified_date: datetime
    status: VulnerabilityVerificationStatus
    event_id: str | None = None


class VulnerabilityZeroRisk(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: datetime
    status: VulnerabilityZeroRiskStatus


class Vulnerability(NamedTuple):
    created_by: str
    created_date: datetime
    finding_id: str
    group_name: str
    hacker_email: str
    id: str
    organization_name: str
    state: VulnerabilityState
    type: VulnerabilityType
    technique: VulnerabilityTechnique | None = None
    bug_tracking_system_url: str | None = None
    custom_severity: int | None = None
    cwe_ids: list[str] | None = None
    developer: str | None = None
    event_id: str | None = None
    hash: int | None = None
    root_id: str | None = None
    severity_score: SeverityScore | None = None
    skims_method: str | None = None
    skims_technique: str | None = None
    stream: list[str] | None = None
    tags: list[str] | None = None
    treatment: VulnerabilityTreatment | None = None
    unreliable_indicators: VulnerabilityUnreliableIndicators = (
        VulnerabilityUnreliableIndicators()
    )
    verification: VulnerabilityVerification | None = None
    zero_risk: VulnerabilityZeroRisk | None = None

    def get_path(self) -> str:
        if self.type.value == VulnerabilityType.INPUTS.value:
            if len(chunks := self.state.where.rsplit(" (", maxsplit=1)) == 2:
                where, _ = chunks
            else:
                where = chunks[0]
        else:
            where = self.state.where
        return where

    def __hash__(self) -> int:
        if self.root_id:
            return hash(
                (
                    self.state.specific,
                    self.type.value,
                    self.get_path(),
                    self.root_id,
                )
            )
        return hash((self.state.specific, self.type.value, self.get_path()))


class VulnerabilityEdge(NamedTuple):
    node: Vulnerability
    cursor: str


class VulnerabilitiesConnection(NamedTuple):
    edges: tuple[VulnerabilityEdge, ...]
    page_info: PageInfo
    total: int | None = None


class VulnerabilityMetadataToUpdate(NamedTuple):
    bug_tracking_system_url: str | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    custom_severity: str | None = None
    cwe_ids: list[str] | None = None
    hacker_email: str | None = None
    hash: int | None = None
    skims_method: str | None = None
    skims_technique: str | None = None
    developer: str | None = None
    root_id: str | None = None
    severity_score: SeverityScore | None = None
    stream: list[str] | None = None
    tags: list[str] | None = None
    type: VulnerabilityType | None = None
    technique: VulnerabilityTechnique | None = None


VulnerabilityHistoric = (
    tuple[VulnerabilityState, ...]
    | tuple[VulnerabilityTreatment, ...]
    | tuple[VulnerabilityVerification, ...]
    | tuple[VulnerabilityZeroRisk, ...]
)

VulnerabilityHistoricEntry = (
    VulnerabilityState
    | VulnerabilityTreatment
    | VulnerabilityVerification
    | VulnerabilityZeroRisk
)


class VulnerabilityUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_closing_date: datetime | None = None
    unreliable_efficacy: Decimal | None = None
    unreliable_last_reattack_date: datetime | None = None
    unreliable_last_reattack_requester: str | None = None
    unreliable_last_requested_reattack_date: datetime | None = None
    unreliable_reattack_cycles: int | None = None
    unreliable_report_date: datetime | None = None
    unreliable_source: Source | None = None
    unreliable_treatment_changes: int | None = None
    clean_unreliable_closing_date: bool = False
    clean_unreliable_last_reattack_date: bool = False
    clean_unreliable_last_requested_reattack_date: bool = False
    clean_unreliable_report_date: bool = False


class VulnerabilityFilters(NamedTuple):
    treatment_status: str | None = None
    verification_status: str | None = None
    where: str | None = None


class FindingVulnerabilitiesZrRequest(NamedTuple):
    finding_id: str
    after: str | None = None
    filters: VulnerabilityFilters = VulnerabilityFilters()
    first: int | None = None
    paginate: bool = False
    state_status: VulnerabilityStateStatus | None = None
    verification_status: VulnerabilityVerificationStatus | None = None


class GroupVulnerabilitiesRequest(NamedTuple):
    group_name: str
    state_status: VulnerabilityStateStatus | None = None
    after: str | None = None
    first: int | None = None
    is_accepted: bool | None = None
    paginate: bool = False


class FindingVulnerabilitiesRequest(NamedTuple):
    finding_id: str
    after: str | None = None
    first: int | None = None
    paginate: bool = False


class VulnerabilityHistoricTreatmentRequest(NamedTuple):
    id: str
    after: str | None = None
    first: int | None = None
    paginate: bool = False
