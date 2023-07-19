from ..types import (
    SeverityLevelsInfo,
    SeverityLevelSummary,
)
from .utils import (
    get_finding,
    get_open_vulnerabilities,
    get_open_vulnerabilities_len,
    get_vulnerabilities_to_reattack,
    remove_all_evidences,
    remove_vulnerabilities,
    validate_duplicated_finding,
    validate_finding_requirements,
)
from aioextensions import (
    collect,
)
import authz
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    FindingNotFound,
    InvalidCVSS3VectorString,
    InvalidSeverityScore,
    RootNotFound,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
    filter_vulnerabilities as filter_vulns_utils,
    findings as findings_utils,
    validations_deco,
    vulnerabilities as vulns_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timezone,
)
from db_model import (
    findings as findings_model,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingMetadataToUpdate,
    FindingState,
)
from db_model.roots.types import (
    GitRootState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from finding_comments import (
    domain as comments_domain,
)
from findings.types import (
    FindingAttributesToAdd,
    FindingDescriptionToUpdate,
)
import logging
import logging.config
import pytz
from roots import (
    utils as roots_utils,
)
from settings import (
    LOGGING,
)
from settings.various import (
    TIME_ZONE,
)
from time import (
    time,
)
from typing import (
    Any,
    TypedDict,
)
import uuid
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.types import (
    Treatments,
    Verifications,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


class VulnsProperties(TypedDict):
    remaining_exposure: int
    severity_level: str
    severity_score: Decimal
    vulns_props: dict[str, dict[str, dict[str, Any]]]


@validations_deco.validate_fields_deco(
    [
        "attributes.attack_vector_description",
        "attributes.description",
        "attributes.recommendation",
        "attributes.unfulfilled_requirements",
        "attributes.threat",
    ]
)
@validations_deco.validate_fields_length_deco(
    [
        "attributes.unfulfilled_requirements",
    ],
    min_length=1,
    max_length=300,
)
@validations_deco.validate_fields_length_deco(
    [
        "attributes.attack_vector_description",
        "attributes.threat",
    ],
    min_length=1,
    max_length=650,
)
@validations_deco.validate_fields_length_deco(
    [
        "attributes.description",
    ],
    min_length=1,
    max_length=1000,
)
@validations_deco.validate_fields_length_deco(
    [
        "attributes.recommendation",
    ],
    min_length=1,
    max_length=500,
)
@validations_deco.validate_update_severity_values_deco("attributes.severity")
async def add_finding(
    *,
    loaders: Dataloaders,
    group_name: str,
    stakeholder_email: str,
    attributes: FindingAttributesToAdd,
    is_from_machine: bool = False,
) -> Finding:
    await findings_utils.is_valid_finding_title(loaders, attributes.title)
    await validate_finding_requirements(
        loaders, attributes.title, attributes.unfulfilled_requirements
    )
    if not attributes.severity_score.cvss_v3:
        raise InvalidCVSS3VectorString()

    cvss_utils.validate_cvss_vector(attributes.severity_score.cvss_v3)
    updated_severity = cvss_utils.adjust_privileges_required(
        attributes.severity
    )
    if not is_from_machine:
        await validate_duplicated_finding(
            loaders,
            group_name,
            attributes.title,
            attributes.description,
            attributes.threat,
            updated_severity,
        )
        if cvss_utils.get_severity_score(updated_severity) <= Decimal(0):
            raise InvalidSeverityScore()

    finding = Finding(
        hacker_email=stakeholder_email,
        attack_vector_description=attributes.attack_vector_description,
        description=attributes.description,
        group_name=group_name,
        id=str(uuid.uuid4()),
        min_time_to_remediate=attributes.min_time_to_remediate,
        state=FindingState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            source=attributes.source,
            status=FindingStateStatus.CREATED,
        ),
        recommendation=attributes.recommendation,
        severity=updated_severity,
        severity_score=attributes.severity_score,
        title=attributes.title,
        threat=attributes.threat,
        unfulfilled_requirements=sorted(
            set(attributes.unfulfilled_requirements)
        ),
    )
    await findings_model.add(finding=finding)
    return finding


async def remove_finding(
    loaders: Dataloaders,
    email: str,
    finding_id: str,
    justification: StateRemovalJustification,
    source: Source,
) -> None:
    finding = await get_finding(loaders, finding_id)
    if finding.state.status == FindingStateStatus.DELETED:
        raise FindingNotFound()

    await remove_vulnerabilities(
        loaders,
        finding.id,
        VulnerabilityStateReason[justification.value],
        email,
    )
    await remove_all_evidences(finding.id, finding.group_name)
    await comments_domain.remove_comments(finding_id=finding_id)
    deletion_state = FindingState(
        justification=justification,
        modified_by=email,
        modified_date=datetime_utils.get_utc_now(),
        source=source,
        status=FindingStateStatus.DELETED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=deletion_state,
    )
    if not findings_utils.is_finding_released(finding):
        await findings_model.remove(
            group_name=finding.group_name, finding_id=finding.id
        )


async def get_last_closed_vulnerability_info(
    loaders: Dataloaders,
    findings: Iterable[Finding],
) -> tuple[int, Vulnerability | None]:
    """Get days since the last closed vulnerability and its metadata."""
    valid_findings_ids = [
        finding.id
        for finding in findings
        if not findings_utils.is_deleted(finding)
    ]
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            valid_findings_ids
        )
    )
    closed_vulns = filter_vulns_utils.filter_closed_vulns(vulns)
    closing_vuln_dates = [
        vulns_utils.get_closing_date(vuln) for vuln in closed_vulns
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates) if v is not None
        )
        last_closed_vuln: Vulnerability | None = closed_vulns[date_index]
        last_closed_days = (
            datetime_utils.get_now().date() - current_date
        ).days
    else:
        last_closed_days = 0
        last_closed_vuln = None
    return last_closed_days, last_closed_vuln


async def get_max_open_severity(
    loaders: Dataloaders, findings: Iterable[Finding]
) -> tuple[Decimal, Finding | None]:
    open_vulns = await collect(
        get_open_vulnerabilities_len(loaders, finding.id)
        for finding in findings
    )
    open_findings = [
        finding
        for finding, open_vulns_count in zip(findings, open_vulns)
        if open_vulns_count > 0
    ]
    total_severity: list[float] = [
        float(cvss_utils.get_severity_score(finding.severity))
        for finding in open_findings
    ]
    if total_severity:
        severity, severity_index = max(
            (v, i) for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal("0.1"))
        max_severity_finding: Finding | None = open_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = None
    return max_severity, max_severity_finding


async def get_newest_vulnerability_report_date(
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    report_dates = vulns_utils.get_report_dates(
        filter_vulns_utils.filter_released_vulns(vulns)
    )

    return max(report_dates) if report_dates else None


async def _is_pending_verification(
    loaders: Dataloaders, finding_id: str
) -> bool:
    return len(await get_vulnerabilities_to_reattack(loaders, finding_id)) > 0


async def get_pending_verification_findings(
    loaders: Dataloaders,
    group_name: str,
) -> list[Finding]:
    """Gets findings pending for verification."""
    findings = await findings_utils.get_group_findings(
        group_name=group_name, loaders=loaders
    )
    are_pending_verifications = await collect(
        _is_pending_verification(loaders, finding.id) for finding in findings
    )
    return [
        finding
        for finding, is_pending_verification in zip(
            findings, are_pending_verifications
        )
        if is_pending_verification
    ]


async def get_treatment_summary(
    loaders: Dataloaders,
    finding_id: str,
) -> Treatments:
    return vulns_domain.get_treatments_count(
        await get_open_vulnerabilities(loaders, finding_id)
    )


async def get_verification_summary(
    loaders: Dataloaders,
    finding_id: str,
) -> Verifications:
    return vulns_domain.get_verifications_count(
        await get_open_vulnerabilities(loaders, finding_id)
    )


async def _get_wheres(
    loaders: Dataloaders, finding_id: str, limit: int | None = None
) -> list[str]:
    finding_vulns = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    open_vulns = filter_vulns_utils.filter_open_vulns(finding_vulns)
    wheres: list[str] = list(set(vuln.state.where for vuln in open_vulns))
    if limit:
        wheres = wheres[:limit]
    return wheres


async def get_where(loaders: Dataloaders, finding_id: str) -> str:
    """
    General locations of the Vulnerabilities. It is limited to 20 locations.
    """
    return ", ".join(sorted(await _get_wheres(loaders, finding_id, limit=20)))


async def has_access_to_finding(
    loaders: Dataloaders, email: str, finding_id: str
) -> bool | None:
    """Verify if the user has access to a finding submission."""
    finding: Finding | None = await loaders.finding.load(finding_id)
    if finding:
        return await authz.has_access_to_group(
            loaders, email, finding.group_name
        )
    raise FindingNotFound()


async def mask_finding(
    loaders: Dataloaders, finding: Finding, email: str
) -> None:
    await comments_domain.remove_comments(finding_id=finding.id)
    await remove_all_evidences(finding.id, finding.group_name)

    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding.id
    )
    await collect(
        tuple(
            vulns_domain.mask_vulnerability(
                loaders=loaders,
                email=email,
                finding_id=finding.id,
                vulnerability=vulnerability,
            )
            for vulnerability in vulnerabilities
        ),
        workers=8,
    )

    if finding.state.status == FindingStateStatus.DELETED and bool(
        finding.unreliable_indicators.unreliable_open_vulnerabilities
        + finding.unreliable_indicators.unreliable_closed_vulnerabilities
    ):
        # Findings in the MASKED state will be archived by Streams
        # for analytics purposes
        await findings_model.update_state(
            current_value=finding.state,
            finding_id=finding.id,
            group_name=finding.group_name,
            state=finding.state._replace(
                modified_by=email,
                modified_date=datetime_utils.get_utc_now(),
                status=FindingStateStatus.MASKED,
            ),
        )

    await findings_model.remove(
        group_name=finding.group_name, finding_id=finding.id
    )
    LOGGER.info(
        "Finding masked",
        extra={
            "extra": {
                "finding_id": finding.id,
                "group_name": finding.group_name,
            }
        },
    )


async def repo_subtitle(
    loaders: Dataloaders, vuln: Vulnerability, group_name: str
) -> str:
    repo = "Vulnerabilities"
    if vuln.root_id is not None:
        try:
            root = await roots_utils.get_root(
                loaders, vuln.root_id, group_name
            )
            nickname = (
                root.state.nickname
                if isinstance(root.state.nickname, str)
                else repo
            )
            repo = (
                f"{nickname}/{root.state.branch}"
                if isinstance(root.state, (GitRootState, str))
                else nickname
            )
        except RootNotFound:
            repo = "Vulnerabilities"
    return repo


async def vulns_properties(
    loaders: Dataloaders,
    finding_id: str,
    vulnerabilities: list[Vulnerability],
    is_closed: bool = False,
) -> dict[str, Any]:
    finding = await get_finding(loaders, finding_id)
    vulns_props: dict[str, dict[str, dict[str, Any]]] = {}
    repos = await collect(
        [
            repo_subtitle(loaders, vuln, finding.group_name)
            for vuln in vulnerabilities
        ]
    )

    for vuln, repo in zip(vulnerabilities, repos):
        vuln_dict = vulns_props.get(repo, {})
        if is_closed:
            exposure = 4 ** (
                cvss_utils.get_vulnerabilities_score(finding, [vuln]) - 4
            )
            report_date = (
                vuln.unreliable_indicators.unreliable_report_date.date()
                if vuln.unreliable_indicators.unreliable_report_date
                else None
            )
            days_open = (
                (datetime_utils.get_utc_now().date() - report_date).days
                if report_date
                else 0
            )
            reattack_requester = (
                vuln.unreliable_indicators.unreliable_last_reattack_requester
            )
            vuln_dict.update(
                {
                    f"{vuln.state.where}{vuln.state.specific}": {
                        "location": vuln.state.where,
                        "specific": vuln.state.specific,
                        "source": vuln.state.source.value,
                        "assigned": vuln.treatment.assigned
                        if vuln.treatment
                        else None,
                        "report date": report_date,
                        "time to remediate": f"{days_open} calendar days",
                        "reattack requester": reattack_requester,
                        "reduction in exposure": round(exposure, 1),
                    },
                }
            )
        else:
            vuln_dict.update(
                {
                    f"{vuln.state.where}{vuln.state.specific}": {
                        "location": vuln.state.where,
                        "specific": vuln.state.specific,
                        "source": vuln.state.source.value,
                    },
                }
            )
        vulns_props[repo] = dict(sorted(vuln_dict.items()))

    return vulns_props


def get_remaining_exposure(
    finding: Finding, closed_vulnerabilities: int
) -> int:
    open_vulnerabilities = (
        finding.unreliable_indicators.unreliable_open_vulnerabilities
    )
    return int(
        (open_vulnerabilities - closed_vulnerabilities)
        * (4 ** (cvss_utils.get_severity_score(finding.severity) - 4))
    )


@validations_deco.validate_fields_deco(["description"])
@validations_deco.validate_fields_length_deco(
    [
        "description.description",
    ],
    min_length=1,
    max_length=1000,
)
@validations_deco.validate_fields_length_deco(
    [
        "description.attack_vector_description",
        "description.threat",
    ],
    min_length=1,
    max_length=650,
)
@validations_deco.validate_fields_length_deco(
    [
        "description.recommendation",
    ],
    min_length=1,
    max_length=500,
)
async def update_description(
    loaders: Dataloaders,
    finding_id: str,
    description: FindingDescriptionToUpdate,
) -> None:
    unfulfilled_requirements = (
        None
        if description.unfulfilled_requirements is None
        else sorted(set(description.unfulfilled_requirements))
    )
    if description.title:
        await findings_utils.is_valid_finding_title(loaders, description.title)

    finding = await get_finding(loaders, finding_id)
    if description.description is not None or description.threat is not None:
        await validate_duplicated_finding(
            loaders,
            finding.group_name,
            description.title or finding.title,
            description.description or finding.description,
            description.threat or finding.threat,
            finding.severity,
            finding,
        )

    if unfulfilled_requirements is not None:
        await validate_finding_requirements(
            loaders,
            description.title or finding.title,
            unfulfilled_requirements,
        )

    metadata = FindingMetadataToUpdate(
        attack_vector_description=description.attack_vector_description,
        description=description.description,
        recommendation=description.recommendation,
        sorts=description.sorts,
        threat=description.threat,
        title=description.title,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def update_severity(
    loaders: Dataloaders,
    finding_id: str,
    severity: CVSS31Severity,
) -> None:
    finding = await get_finding(loaders, finding_id)
    updated_severity = cvss_utils.adjust_privileges_required(severity)
    cvss3_vector = cvss_utils.parse_cvss31_severity_legacy(updated_severity)
    metadata = FindingMetadataToUpdate(
        severity=updated_severity,
        severity_score=cvss_utils.get_severity_score_from_cvss_vector(
            cvss3_vector
        ),
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def update_severity_from_cvss_vector(
    loaders: Dataloaders,
    finding_id: str,
    cvss_vector: str,
) -> None:
    finding = await get_finding(loaders, finding_id)
    severity_legacy = cvss_utils.parse_cvss_vector_string(cvss_vector)
    metadata = FindingMetadataToUpdate(
        severity=severity_legacy,
        severity_score=cvss_utils.get_severity_score_from_cvss_vector(
            cvss_vector
        ),
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def get_vuln_nickname(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> str:
    result: str = f"{vuln.state.where} ({vuln.state.specific})"
    if vuln.type == VulnerabilityType.LINES:
        try:
            if root := await roots_utils.get_root(
                loaders, vuln.root_id or "", vuln.group_name
            ):
                return f" {root.state.nickname}/{result}"
        except RootNotFound:
            pass
    return result


# pylint: disable=too-many-arguments,too-many-locals
async def add_reattack_justification(
    loaders: Dataloaders,
    finding_id: str,
    open_vulnerabilities: Iterable[Vulnerability],
    closed_vulnerabilities: Iterable[Vulnerability],
    commit_hash: str | None = None,
    comment_type: CommentType = CommentType.COMMENT,
    email: str = "machine@fluidttacks.com",
    full_name: str = "Machine Services",
    observations: str | None = None,
) -> None:
    justification = (
        datetime.now(tz=timezone.utc)
        .astimezone(tz=pytz.timezone(TIME_ZONE))
        .strftime("%Y/%m/%d %H:%M")
    )
    commit_msg = f" in commit {commit_hash}" if commit_hash else ""
    observations_msg = (
        f"\n\nObservations:\n  {observations}" if observations else ""
    )
    justification = (
        "A reattack request was executed on "
        f"{justification.replace(' ', ' at ')}{commit_msg}."
    )
    vulns_nicknames = await collect(
        [get_vuln_nickname(loaders, vuln) for vuln in open_vulnerabilities],
        workers=32,
    )
    vulns_strs = [f"  - {vuln_nickname}" for vuln_nickname in vulns_nicknames]
    if vulns_strs:
        justification += "\n\nOpen vulnerabilities:\n"
        justification += "\n".join(vulns_strs) if vulns_strs else ""

    vulns_nicknames = await collect(
        [get_vuln_nickname(loaders, vuln) for vuln in closed_vulnerabilities],
        workers=32,
    )

    vulns_strs = [f"  - {vuln_nickname}" for vuln_nickname in vulns_nicknames]
    if vulns_strs:
        justification += "\n\nClosed vulnerabilities:\n"
        justification += "\n".join(vulns_strs) if vulns_strs else ""
    justification += observations_msg
    LOGGER.info(
        "%s Vulnerabilities were verified and found open in finding %s",
        len(list(open_vulnerabilities)),
        finding_id,
    )
    LOGGER.info(
        "%s Vulnerabilities were verified and found closed in finding %s",
        len(list(closed_vulnerabilities)),
        finding_id,
    )
    if open_vulnerabilities or closed_vulnerabilities:
        closed_properties: VulnsProperties | None = None
        if closed_vulnerabilities:
            finding = await get_finding(loaders, finding_id)
            if (
                finding.unreliable_indicators.unreliable_status
                == FindingStatus.VULNERABLE
            ):
                severity_score = cvss_utils.get_vulnerabilities_score(
                    finding, closed_vulnerabilities
                )
                closed_properties = VulnsProperties(
                    remaining_exposure=get_remaining_exposure(
                        finding, len(list(closed_vulnerabilities))
                    ),
                    severity_level=cvss_utils.get_severity_level(
                        severity_score
                    ),
                    severity_score=severity_score,
                    vulns_props=await vulns_properties(
                        loaders,
                        finding_id,
                        [
                            vuln
                            for vuln in closed_vulnerabilities
                            if vuln is not None
                        ],
                        is_closed=True,
                    ),
                )
        await comments_domain.add(
            loaders,
            FindingComment(
                finding_id=finding_id,
                id=str(round(time() * 1000)),
                comment_type=comment_type,
                parent_id="0",
                creation_date=datetime_utils.get_utc_now(),
                full_name=full_name,
                content=justification,
                email=email,
            ),
            closed_properties=closed_properties,
        )


async def get_oldest_no_treatment(
    loaders: Dataloaders,
    findings: Iterable[Finding],
) -> dict[str, int | str] | None:
    """Get the finding with oldest "no treatment" vulnerability."""
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )
    open_vulns = filter_vulns_utils.filter_open_vulns(vulns)
    no_treatment_vulns = filter_vulns_utils.filter_no_treatment_vulns(
        open_vulns
    )
    if not no_treatment_vulns:
        return None
    treatment_dates: list[datetime] = [
        vuln.treatment.modified_date
        for vuln in no_treatment_vulns
        if vuln.treatment
    ]
    vulns_info = [
        (
            date,
            vuln.finding_id,
        )
        for vuln, date in zip(no_treatment_vulns, treatment_dates)
    ]
    oldest_date, oldest_finding_id = min(vulns_info)
    oldest_finding: Finding = next(
        finding for finding in findings if finding.id == oldest_finding_id
    )
    return {
        "oldest_name": str(oldest_finding.title),
        "oldest_age": int((datetime_utils.get_now() - oldest_date).days),
    }


async def get_oldest_open_vulnerability_report_date(
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = filter_vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_oldest_report_dates(open_vulns)

    return min(report_dates) if report_dates else None


async def get_oldest_vulnerability_report_date(
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    released_vulns = filter_vulns_utils.filter_released_vulns(vulns)
    report_dates = vulns_utils.get_oldest_report_dates(released_vulns)

    return min(report_dates) if report_dates else None


def check_hold(vuln: Vulnerability) -> bool:
    return (
        vuln.verification is not None
        and vuln.verification.status == VulnerabilityVerificationStatus.ON_HOLD
    )


async def get_max_open_severity_score(
    loaders: Dataloaders,
    finding_id: str,
) -> Decimal:
    finding = await loaders.finding.load(finding_id)
    if finding is None or findings_utils.is_deleted(finding):
        return Decimal("0.0")

    vulns = await get_open_vulnerabilities(loaders, finding.id)
    if not vulns:
        return Decimal("0.0")

    vulns_score = [
        vuln.severity_score.temporal_score
        if vuln.severity_score
        else finding.severity_score.temporal_score
        for vuln in vulns
    ]

    return Decimal(max(vulns_score))


async def get_total_open_cvssf(
    loaders: Dataloaders,
    finding_id: str,
) -> Decimal:
    finding = await loaders.finding.load(finding_id)
    if finding is None or findings_utils.is_deleted(finding):
        return Decimal("0.0")

    vulns = await get_open_vulnerabilities(loaders, finding.id)
    if not vulns:
        return Decimal("0.0")

    vulns_cvssf = [
        vuln.severity_score.cvssf
        if vuln.severity_score
        else finding.severity_score.cvssf
        for vuln in vulns
    ]

    return Decimal(sum(vulns_cvssf))


def _get_severity_level_summary(
    finding: Finding, vulns: Iterable[Vulnerability], severity_level: str
) -> SeverityLevelSummary:
    level_vulns = [
        vuln
        for vuln in vulns
        if cvss_utils.get_severity_level(
            vulns_utils.get_severity_temporal_score(vuln, finding)
        )
        == severity_level
    ]
    treatments_count = vulns_domain.get_treatments_count(level_vulns)

    return SeverityLevelSummary(
        accepted=treatments_count.accepted
        + treatments_count.accepted_undefined,
        closed=len(filter_vulns_utils.filter_closed_vulns(level_vulns)),
        total=len(level_vulns),
    )


async def get_severity_levels_info(
    loaders: Dataloaders,
    finding: Finding,
) -> SeverityLevelsInfo:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding.id)

    return SeverityLevelsInfo(
        critical=_get_severity_level_summary(finding, vulns, "critical"),
        high=_get_severity_level_summary(finding, vulns, "high"),
        medium=_get_severity_level_summary(finding, vulns, "medium"),
        low=_get_severity_level_summary(finding, vulns, "low"),
    )
