from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from custom_exceptions import (
    InvalidParameter,
    VulnerabilityEntryNotFound,
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
from db_model.utils import (
    get_as_utc_iso_format,
)
from db_model.vulnerabilities.constants import (
    ACCEPTED_TREATMENT_STATUSES,
    GROUP_INDEX_METADATA,
    NEW_ZR_INDEX_METADATA,
    RELEASED_FILTER_STATUSES,
    ZR_FILTER_STATUSES,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityAdvisory,
    VulnerabilityEdge,
    VulnerabilityHistoricEntry,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityUnreliableIndicatorsToUpdate,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
)
from dynamodb.types import (
    Index,
    Item,
    PrimaryKey,
    Table,
)
from dynamodb.utils import (
    get_cursor,
)
from serializers import (
    Snippet,
)


def get_current_treatment_converted(treatment: str) -> str:
    if treatment == "UNTREATED":
        return "NEW"

    return treatment


def get_inverted_treatment_converted(treatment: str) -> str:
    if treatment == "NEW":
        return "UNTREATED"

    return treatment


def get_current_state_converted(state: str) -> str:
    if state in {"SAFE", "VULNERABLE"}:
        translation: dict[str, str] = {
            "SAFE": "CLOSED",
            "VULNERABLE": "OPEN",
        }

        return translation[state]

    return state


def get_inverted_state_converted(state: str) -> str:
    if state in {"CLOSED", "OPEN"}:
        translation: dict[str, str] = {
            "CLOSED": "SAFE",
            "OPEN": "VULNERABLE",
        }

        return translation[state]

    return state


def filter_non_deleted(
    vulnerabilities: list[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status
        not in {
            VulnerabilityStateStatus.DELETED,
            VulnerabilityStateStatus.MASKED,
        }
    ]


def filter_released_and_non_zero_risk(
    vulnerabilities: list[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status in RELEASED_FILTER_STATUSES
        and (
            not vuln.zero_risk
            or vuln.zero_risk.status not in ZR_FILTER_STATUSES
        )
    ]


def filter_released_and_zero_risk(
    vulnerabilities: list[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status in RELEASED_FILTER_STATUSES
        and (vuln.zero_risk and vuln.zero_risk.status in ZR_FILTER_STATUSES)
    ]


def format_vulnerability(item: Item) -> Vulnerability:
    state = format_state(item["state"])
    treatment = (
        format_treatment(item["treatment"]) if "treatment" in item else None
    )
    verification = (
        format_verification(item["verification"])
        if "verification" in item
        else None
    )
    zero_risk = (
        format_zero_risk(item["zero_risk"]) if "zero_risk" in item else None
    )
    unreliable_indicators = (
        format_unreliable_indicators(item["unreliable_indicators"])
        if "unreliable_indicators" in item
        else VulnerabilityUnreliableIndicators()
    )
    cwe_ids: list[str] | None = (
        sorted(item["cwe_ids"]) if item.get("cwe_ids") else None
    )
    severity_score = (
        SeverityScore(
            base_score=Decimal(item["severity_score"]["base_score"]),
            temporal_score=Decimal(item["severity_score"]["temporal_score"]),
            cvss_v3=item["severity_score"]["cvss_v3"],
            cvssf=Decimal(item["severity_score"]["cvssf"]),
        )
        if item.get("severity_score") is not None
        else None
    )

    return Vulnerability(
        bug_tracking_system_url=item.get("bug_tracking_system_url"),
        created_by=item["created_by"],
        created_date=datetime.fromisoformat(item["created_date"]),
        custom_severity=(
            int(item["custom_severity"])
            if "custom_severity" in item
            and item["custom_severity"] is not None
            and item["custom_severity"]
            else None
        ),
        cwe_ids=cwe_ids,
        developer=item.get("developer"),
        event_id=item.get("pk_4"),
        finding_id=item["sk"].split("#")[1],
        group_name=item["group_name"],
        hacker_email=item["hacker_email"],
        hash=item.get("hash"),
        id=item["pk"].split("#")[1],
        organization_name=item["organization_name"],
        root_id=item.get("root_id"),
        severity_score=severity_score,
        skims_method=item.get("skims_method"),
        skims_technique=item.get("skims_technique"),
        state=state,
        stream=item.get("stream"),
        tags=item.get("tags"),
        technique=item.get("technique"),
        treatment=treatment,
        type=VulnerabilityType[item["type"]],
        unreliable_indicators=unreliable_indicators,
        verification=verification,
        zero_risk=zero_risk,
    )


def format_vulnerability_edge(
    index: Index | None,
    item: Item,
    table: Table,
) -> VulnerabilityEdge:
    return VulnerabilityEdge(
        node=format_vulnerability(item), cursor=get_cursor(index, item, table)
    )


def _format_snippet(snippet: Item | None = None) -> Snippet | None:
    if not snippet or isinstance(snippet, str):
        return None
    return Snippet(
        content=snippet["content"],
        offset=snippet["offset"],
        line=snippet["line"],
        column=snippet.get("column"),
        columns_per_line=snippet["columns_per_line"],
        line_context=snippet["line_context"],
        highlight_line_number=snippet["highlight_line_number"],
        show_line_numbers=snippet["show_line_numbers"],
        wrap=snippet["wrap"],
    )


def _format_advisory(
    advisory: Item | None = None,
) -> VulnerabilityAdvisory | None:
    if not advisory:
        return None
    return VulnerabilityAdvisory(
        cve=advisory.get("cve"),
        package=advisory.get("package"),
        vulnerable_version=advisory.get("vulnerable_version"),
    )


def format_state(item: Item) -> VulnerabilityState:
    tool = format_tool(item["tool"]) if "tool" in item else None
    return VulnerabilityState(
        advisories=_format_advisory(item.get("advisories")),
        commit=item.get("commit"),
        modified_by=item["modified_by"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        other_reason=item.get("other_reason"),
        reasons=[
            VulnerabilityStateReason[reason] for reason in item["reasons"]
        ]
        if "reasons" in item
        else None,
        source=Source[item["source"]],
        specific=item["specific"],
        status=VulnerabilityStateStatus[item["status"]],
        tool=tool,
        where=item["where"],
        snippet=_format_snippet(item.get("snippet")),
    )


def format_tool(item: Item) -> VulnerabilityTool:
    return VulnerabilityTool(
        name=item["name"], impact=VulnerabilityToolImpact[item["impact"]]
    )


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=datetime.fromisoformat(item["accepted_until"])
        if item.get("accepted_until")
        else None,
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if item.get("acceptance_status")
        else None,
        justification=item.get("justification"),
        assigned=item.get("assigned"),
        modified_by=item.get("modified_by"),
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityTreatmentStatus[item["status"]],
    )


def format_unreliable_indicators(
    item: Item,
) -> VulnerabilityUnreliableIndicators:
    return VulnerabilityUnreliableIndicators(
        unreliable_closing_date=datetime.fromisoformat(
            item["unreliable_closing_date"]
        )
        if item.get("unreliable_closing_date")
        else None,
        unreliable_efficacy=item.get("unreliable_efficacy"),
        unreliable_last_reattack_date=datetime.fromisoformat(
            item["unreliable_last_reattack_date"]
        )
        if item.get("unreliable_last_reattack_date")
        else None,
        unreliable_last_reattack_requester=item.get(
            "unreliable_last_reattack_requester"
        ),
        unreliable_last_requested_reattack_date=datetime.fromisoformat(
            item["unreliable_last_requested_reattack_date"]
        )
        if item.get("unreliable_last_requested_reattack_date")
        else None,
        unreliable_reattack_cycles=None
        if item.get("unreliable_reattack_cycles") is None
        else int(item["unreliable_reattack_cycles"]),
        unreliable_report_date=datetime.fromisoformat(
            item["unreliable_report_date"]
        )
        if item.get("unreliable_report_date")
        else None,
        unreliable_source=Source[item["unreliable_source"]]
        if item.get("unreliable_source")
        else Source.ASM,
        unreliable_treatment_changes=None
        if item.get("unreliable_treatment_changes") is None
        else int(item["unreliable_treatment_changes"]),
    )


def format_unreliable_indicators_item(
    indicators: VulnerabilityUnreliableIndicators,
) -> Item:
    item = {
        "unreliable_closing_date": (
            get_as_utc_iso_format(indicators.unreliable_closing_date)
            if indicators.unreliable_closing_date
            else None
        ),
        "unreliable_efficacy": indicators.unreliable_efficacy,
        "unreliable_last_reattack_date": (
            get_as_utc_iso_format(indicators.unreliable_last_reattack_date)
            if indicators.unreliable_last_reattack_date
            else None
        ),
        "unreliable_last_reattack_requester": (
            indicators.unreliable_last_reattack_requester
        ),
        "unreliable_last_requested_reattack_date": (
            get_as_utc_iso_format(
                indicators.unreliable_last_requested_reattack_date
            )
            if indicators.unreliable_last_requested_reattack_date
            else None
        ),
        "unreliable_reattack_cycles": indicators.unreliable_reattack_cycles,
        "unreliable_report_date": (
            get_as_utc_iso_format(indicators.unreliable_report_date)
            if indicators.unreliable_report_date
            else None
        ),
        "unreliable_source": indicators.unreliable_source,
        "unreliable_treatment_changes": (
            indicators.unreliable_treatment_changes
        ),
    }

    return {key: value for key, value in item.items() if value is not None}


def format_unreliable_indicators_to_update_item(
    indicators: VulnerabilityUnreliableIndicatorsToUpdate,
) -> Item:
    item = {
        "unreliable_closing_date": (
            get_as_utc_iso_format(indicators.unreliable_closing_date)
            if indicators.unreliable_closing_date
            else None
        ),
        "unreliable_efficacy": indicators.unreliable_efficacy,
        "unreliable_last_reattack_date": (
            get_as_utc_iso_format(indicators.unreliable_last_reattack_date)
            if indicators.unreliable_last_reattack_date
            else None
        ),
        "unreliable_last_reattack_requester": (
            indicators.unreliable_last_reattack_requester
        ),
        "unreliable_last_requested_reattack_date": (
            get_as_utc_iso_format(
                indicators.unreliable_last_requested_reattack_date
            )
            if indicators.unreliable_last_requested_reattack_date
            else None
        ),
        "unreliable_reattack_cycles": indicators.unreliable_reattack_cycles,
        "unreliable_report_date": (
            get_as_utc_iso_format(indicators.unreliable_report_date)
            if indicators.unreliable_report_date
            else None
        ),
        "unreliable_source": indicators.unreliable_source,
        "unreliable_treatment_changes": (
            indicators.unreliable_treatment_changes
        ),
    }
    item = {key: value for key, value in item.items() if value is not None}

    if indicators.clean_unreliable_closing_date:
        item["unreliable_closing_date"] = None
    if indicators.clean_unreliable_last_reattack_date:
        item["unreliable_last_reattack_date"] = None
    if indicators.clean_unreliable_last_requested_reattack_date:
        item["unreliable_last_requested_reattack_date"] = None
    if indicators.clean_unreliable_report_date:
        item["unreliable_report_date"] = None
    return item


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        event_id=item.get("event_id"),
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_zero_risk(item: Item) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=item["comment_id"],
        modified_by=item["modified_by"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityZeroRiskStatus[item["status"]],
    )


def historic_entry_type_to_str(item: VulnerabilityHistoricEntry) -> str:
    if isinstance(item, VulnerabilityState):
        return "state"
    if isinstance(item, VulnerabilityTreatment):
        return "treatment"
    if isinstance(item, VulnerabilityVerification):
        return "verification"
    if isinstance(item, VulnerabilityZeroRisk):
        return "zero_risk"

    raise InvalidParameter(type(item))


def get_current_entry(
    entry: VulnerabilityHistoricEntry, current_value: Vulnerability
) -> VulnerabilityHistoricEntry | None:
    if isinstance(entry, VulnerabilityState):
        return current_value.state
    if isinstance(entry, VulnerabilityTreatment):
        return current_value.treatment
    if isinstance(entry, VulnerabilityVerification):
        return current_value.verification
    if isinstance(entry, VulnerabilityZeroRisk):
        return current_value.zero_risk

    raise VulnerabilityEntryNotFound()


def get_assigned(*, treatment: VulnerabilityTreatment | None) -> str:
    if treatment is None or treatment.assigned is None:
        return ""

    return treatment.assigned


def get_group_index_key(vulnerability: Vulnerability) -> PrimaryKey:
    return keys.build_key(
        facet=GROUP_INDEX_METADATA,
        values={
            "group_name": vulnerability.group_name,
            "is_zero_risk": str(
                bool(
                    vulnerability.zero_risk
                    and vulnerability.zero_risk.status in ZR_FILTER_STATUSES
                )
            ).lower(),
            "state_status": vulnerability.state.status.lower(),
            "is_accepted": str(
                bool(
                    vulnerability.treatment
                    and vulnerability.treatment.status
                    in ACCEPTED_TREATMENT_STATUSES
                )
            ).lower(),
        },
    )


def get_new_group_index_key(
    current_value: Vulnerability, entry: VulnerabilityHistoricEntry
) -> PrimaryKey | None:
    new_group_index_key: PrimaryKey | None = None
    if isinstance(entry, VulnerabilityState):
        new_group_index_key = keys.build_key(
            facet=GROUP_INDEX_METADATA,
            values={
                "group_name": current_value.group_name,
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": entry.status.lower(),
                "is_accepted": str(
                    bool(
                        current_value.treatment
                        and current_value.treatment.status
                        in ACCEPTED_TREATMENT_STATUSES
                    )
                ).lower(),
            },
        )
    elif isinstance(entry, VulnerabilityTreatment):
        new_group_index_key = keys.build_key(
            facet=GROUP_INDEX_METADATA,
            values={
                "group_name": current_value.group_name,
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": current_value.state.status.lower(),
                "is_accepted": str(
                    bool(entry.status in ACCEPTED_TREATMENT_STATUSES)
                ).lower(),
            },
        )
    elif isinstance(entry, VulnerabilityZeroRisk):
        new_group_index_key = keys.build_key(
            facet=GROUP_INDEX_METADATA,
            values={
                "group_name": current_value.group_name,
                "is_zero_risk": str(
                    bool(entry.status in ZR_FILTER_STATUSES)
                ).lower(),
                "state_status": current_value.state.status.lower(),
                "is_accepted": str(
                    bool(
                        current_value.treatment
                        and current_value.treatment.status
                        in ACCEPTED_TREATMENT_STATUSES
                    )
                ).lower(),
            },
        )

    return new_group_index_key


def get_zr_index_key_gsi_6(current_value: Vulnerability) -> PrimaryKey:
    return keys.build_key(
        facet=NEW_ZR_INDEX_METADATA,
        values={
            "finding_id": current_value.finding_id,
            "vuln_id": current_value.id,
            "is_deleted": str(
                current_value.state.status is VulnerabilityStateStatus.DELETED
            ).lower(),
            "is_released": str(
                current_value.state.status in RELEASED_FILTER_STATUSES
            ).lower(),
            "is_zero_risk": str(
                bool(
                    current_value.zero_risk
                    and current_value.zero_risk.status in ZR_FILTER_STATUSES
                )
            ).lower(),
            "state_status": str(current_value.state.status.value).lower(),
            "verification_status": str(
                current_value.verification
                and current_value.verification.status.value
            ).lower(),
        },
    )


def get_new_zr_index_key_gsi_6(
    current_value: Vulnerability, entry: VulnerabilityHistoricEntry
) -> PrimaryKey | None:
    new_zr_index_key = None
    if isinstance(entry, VulnerabilityState):
        new_zr_index_key = keys.build_key(
            facet=NEW_ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    entry.status is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_released": str(
                    entry.status in RELEASED_FILTER_STATUSES
                ).lower(),
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": str(entry.status.value).lower(),
                "verification_status": str(
                    current_value.verification
                    and current_value.verification.status.value
                ).lower(),
            },
        )
    if isinstance(entry, VulnerabilityZeroRisk):
        new_zr_index_key = keys.build_key(
            facet=NEW_ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    current_value.state.status
                    is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_released": str(
                    current_value.state.status in RELEASED_FILTER_STATUSES
                ).lower(),
                "is_zero_risk": str(
                    entry.status in ZR_FILTER_STATUSES
                ).lower(),
                "state_status": str(current_value.state.status.value).lower(),
                "verification_status": str(
                    current_value.verification
                    and current_value.verification.status.value
                ).lower(),
            },
        )
    if isinstance(entry, VulnerabilityVerification):
        new_zr_index_key = keys.build_key(
            facet=NEW_ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    current_value.state.status
                    is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_released": str(
                    current_value.state.status in RELEASED_FILTER_STATUSES
                ).lower(),
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": str(current_value.state.status.value).lower(),
                "verification_status": str(entry.status.value).lower(),
            },
        )

    return new_zr_index_key
