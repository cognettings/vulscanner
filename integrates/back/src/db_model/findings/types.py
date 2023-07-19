from __future__ import (
    annotations,
)

from .enums import (
    DraftRejectionReason,
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
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
from typing import (
    NamedTuple,
)


class CVSS31Severity(NamedTuple):
    attack_complexity: Decimal = Decimal("0.0")
    attack_vector: Decimal = Decimal("0.0")
    availability_impact: Decimal = Decimal("0.0")
    availability_requirement: Decimal = Decimal("0.0")
    confidentiality_impact: Decimal = Decimal("0.0")
    confidentiality_requirement: Decimal = Decimal("0.0")
    exploitability: Decimal = Decimal("0.0")
    integrity_impact: Decimal = Decimal("0.0")
    integrity_requirement: Decimal = Decimal("0.0")
    modified_attack_complexity: Decimal = Decimal("0.0")
    modified_attack_vector: Decimal = Decimal("0.0")
    modified_availability_impact: Decimal = Decimal("0.0")
    modified_confidentiality_impact: Decimal = Decimal("0.0")
    modified_integrity_impact: Decimal = Decimal("0.0")
    modified_privileges_required: Decimal = Decimal("0.0")
    modified_user_interaction: Decimal = Decimal("0.0")
    modified_severity_scope: Decimal = Decimal("0.0")
    privileges_required: Decimal = Decimal("0.0")
    remediation_level: Decimal = Decimal("0.0")
    report_confidence: Decimal = Decimal("0.0")
    severity_scope: Decimal = Decimal("0.0")
    user_interaction: Decimal = Decimal("0.0")


class CVSS31SeverityParameters(NamedTuple):
    base_score_factor: Decimal
    exploitability_factor_1: Decimal
    impact_factor_1: Decimal
    impact_factor_2: Decimal
    impact_factor_3: Decimal
    impact_factor_4: Decimal
    impact_factor_5: Decimal
    impact_factor_6: Decimal
    mod_impact_factor_1: Decimal
    mod_impact_factor_2: Decimal
    mod_impact_factor_3: Decimal
    mod_impact_factor_4: Decimal
    mod_impact_factor_5: Decimal
    mod_impact_factor_6: Decimal
    mod_impact_factor_7: Decimal
    mod_impact_factor_8: Decimal


class DraftRejection(NamedTuple):
    other: str
    reasons: set[DraftRejectionReason]
    rejected_by: str
    rejection_date: datetime
    submitted_by: str


class FindingState(NamedTuple):
    modified_by: str
    modified_date: datetime
    source: Source
    status: FindingStateStatus
    rejection: DraftRejection | None = None
    justification: StateRemovalJustification = (
        StateRemovalJustification.NO_JUSTIFICATION
    )


class FindingVerification(NamedTuple):
    comment_id: str
    modified_by: str
    modified_date: datetime
    status: FindingVerificationStatus
    vulnerability_ids: set[str] | None = None


class FindingEvidence(NamedTuple):
    description: str
    modified_date: datetime
    url: str
    is_draft: bool = False


class FindingEvidences(NamedTuple):
    animation: FindingEvidence | None = None
    evidence1: FindingEvidence | None = None
    evidence2: FindingEvidence | None = None
    evidence3: FindingEvidence | None = None
    evidence4: FindingEvidence | None = None
    evidence5: FindingEvidence | None = None
    exploitation: FindingEvidence | None = None
    records: FindingEvidence | None = None


class FindingTreatmentSummary(NamedTuple):
    accepted: int = 0
    accepted_undefined: int = 0
    in_progress: int = 0
    untreated: int = 0


class FindingVerificationSummary(NamedTuple):
    requested: int = 0
    on_hold: int = 0
    verified: int = 0


class FindingUnreliableIndicators(NamedTuple):
    unreliable_closed_vulnerabilities: int = 0
    unreliable_max_open_severity_score: Decimal = Decimal("0.0")
    unreliable_newest_vulnerability_report_date: datetime | None = None
    unreliable_oldest_open_vulnerability_report_date: datetime | None = None
    unreliable_oldest_vulnerability_report_date: datetime | None = None
    unreliable_open_vulnerabilities: int = 0
    unreliable_rejected_vulnerabilities: int = 0
    unreliable_status: FindingStatus = FindingStatus.DRAFT
    unreliable_submitted_vulnerabilities: int = 0
    unreliable_total_open_cvssf: Decimal = Decimal("0.0")
    unreliable_treatment_summary: FindingTreatmentSummary = (
        FindingTreatmentSummary()
    )
    unreliable_verification_summary: FindingVerificationSummary = (
        FindingVerificationSummary()
    )
    unreliable_where: str = ""
    open_vulnerabilities: int = 0
    closed_vulnerabilities: int = 0
    submitted_vulnerabilities: int = 0
    rejected_vulnerabilities: int = 0
    max_open_severity_score: Decimal = Decimal("0.0")
    newest_vulnerability_report_date: datetime | None = None
    oldest_vulnerability_report_date: datetime | None = None
    treatment_summary: FindingTreatmentSummary = FindingTreatmentSummary()


class Finding(NamedTuple):
    hacker_email: str
    group_name: str
    id: str
    severity_score: SeverityScore
    state: FindingState
    title: str
    attack_vector_description: str = ""
    creation: FindingState | None = None
    rejected_vulnerabilities: int | None = None
    submitted_vulnerabilities: int | None = None
    description: str = ""
    evidences: FindingEvidences = FindingEvidences()
    min_time_to_remediate: int | None = None
    recommendation: str = ""
    requirements: str = ""
    severity: CVSS31Severity = CVSS31Severity()
    sorts: FindingSorts = FindingSorts.NO
    threat: str = ""
    unfulfilled_requirements: list[str] = []
    unreliable_indicators: FindingUnreliableIndicators = (
        FindingUnreliableIndicators()
    )
    verification: FindingVerification | None = None


class FindingEdge(NamedTuple):
    node: Finding
    cursor: str


class FindingsConnection(NamedTuple):
    edges: tuple[FindingEdge, ...]
    page_info: PageInfo
    total: int | None = None


class FindingEvidenceToUpdate(NamedTuple):
    description: str | None = None
    is_draft: bool | None = None
    modified_date: datetime | None = None
    url: str | None = None


class FindingMetadataToUpdate(NamedTuple):
    attack_vector_description: str | None = None
    description: str | None = None
    evidences: FindingEvidences | None = None
    hacker_email: str | None = None
    min_time_to_remediate: int | None = None
    recommendation: str | None = None
    requirements: str | None = None
    severity: CVSS31Severity | None = None
    severity_score: SeverityScore | None = None
    sorts: FindingSorts | None = None
    threat: str | None = None
    title: str | None = None
    unfulfilled_requirements: list[str] | None = None


class FindingUnreliableIndicatorsToUpdate(NamedTuple):
    unreliable_closed_vulnerabilities: int | None = None
    unreliable_max_open_severity_score: Decimal | None = None
    unreliable_newest_vulnerability_report_date: datetime | None = None
    unreliable_oldest_open_vulnerability_report_date: datetime | None = None
    unreliable_oldest_vulnerability_report_date: datetime | None = None
    unreliable_open_vulnerabilities: int | None = None
    unreliable_rejected_vulnerabilities: int | None = None
    unreliable_status: FindingStatus | None = None
    unreliable_submitted_vulnerabilities: int | None = None
    unreliable_total_open_cvssf: Decimal | None = None
    unreliable_treatment_summary: FindingTreatmentSummary | None = None
    unreliable_verification_summary: FindingVerificationSummary | None = None
    unreliable_where: str | None = None
    clean_unreliable_newest_vulnerability_report_date: bool = False
    clean_unreliable_oldest_open_vulnerability_report_date: bool = False
    clean_unreliable_oldest_vulnerability_report_date: bool = False
    open_vulnerabilities: int | None = None
    closed_vulnerabilities: int | None = None
    submitted_vulnerabilities: int | None = None
    rejected_vulnerabilities: int | None = None
    max_open_severity_score: Decimal | None = None
    newest_vulnerability_report_date: datetime | None = None
    oldest_vulnerability_report_date: datetime | None = None
    treatment_summary: FindingTreatmentSummary | None = None
