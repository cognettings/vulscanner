from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    FindingNotFound,
    GroupNotFound,
    InvalidCommentParent,
    InvalidVulnerabilityRequirement,
    PermissionDenied,
    RepeatedFindingDescription,
    RepeatedFindingMachineDescription,
    RepeatedFindingThreat,
    RequiredUnfulfilledRequirements,
)
from custom_utils import (
    datetime as datetime_utils,
    filter_vulnerabilities as filter_vulns_utils,
    findings as findings_utils,
    machine as machine_utils,
    validations_deco,
    vulnerabilities as vulns_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingEvidences,
    FindingMetadataToUpdate,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesRequest,
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    Vulnerability,
)
from finding_comments import (
    domain as comments_domain,
)
from findings import (
    storage as findings_storage,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
)
from vulnerabilities import (
    domain as vulns_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def validate_finding_requirements(
    loaders: Dataloaders, title: str, unfulfilled_requirements: list[str]
) -> None:
    if not unfulfilled_requirements:
        raise RequiredUnfulfilledRequirements()
    vulnerabilities_file = await loaders.vulnerabilities_file.load("")
    criteria_vulnerability_id = title.split(".")[0].strip()
    criteria_vulnerability = vulnerabilities_file[criteria_vulnerability_id]
    criteria_vulnerabilily_requirements: list[str] = (
        criteria_vulnerability["requirements"]
        if criteria_vulnerability
        else []
    )
    if not set(unfulfilled_requirements).issubset(
        criteria_vulnerabilily_requirements
    ):
        raise InvalidVulnerabilityRequirement()


async def validate_duplicated_finding(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    title: str,
    description: str,
    threat: str,
    severity: CVSS31Severity,
    current_finding: Finding | None = None,
) -> None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    group_findings = await loaders.group_findings.load(group_name)
    same_type_of_findings = (
        [
            finding
            for finding in group_findings
            if finding.id != current_finding.id
            and (
                finding.title.split(".")[0].strip()
                == title.split(".")[0].strip()
            )
        ]
        if current_finding
        else [
            finding
            for finding in group_findings
            if finding.title.split(".")[0].strip()
            == title.split(".")[0].strip()
        ]
    )
    for finding in same_type_of_findings:
        if finding.description.strip() == description.strip() and not (
            current_finding is not None
            and current_finding.description.split() == description.split()
        ):
            raise RepeatedFindingDescription()
        if finding.threat.strip() == threat.strip():
            raise RepeatedFindingThreat()

    await validate_machine_description(
        loaders,
        title,
        description,
        threat,
        severity,
        group,
        same_type_of_findings,
    )


async def validate_machine_description(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    title: str,
    description: str,
    threat: str,
    severity: CVSS31Severity,
    group: Group,
    same_type_of_findings: list[Finding],
) -> None:
    criteria_vulnerabilities = await loaders.vulnerabilities_file.load("")
    criteria_vulnerability: dict[str, Any] = criteria_vulnerabilities[
        title.split(".")[0].strip()
    ]
    duplicated_findings = [
        finding
        for finding in same_type_of_findings
        if machine_utils.has_machine_description(
            finding._replace(
                description=description, threat=threat, severity=severity
            ),
            criteria_vulnerability,
            str(group.language.value).lower(),
        )
    ]
    if duplicated_findings:
        raise RepeatedFindingMachineDescription()


async def get_finding(loaders: Dataloaders, finding_id: str) -> Finding:
    finding = await loaders.finding.load(finding_id)
    if finding is None or findings_utils.is_deleted(finding):
        LOGGER.exception(
            "Finding not found",
            extra={
                "extra": {
                    "finding_id": finding_id,
                    "group_name": finding.group_name
                    if finding is not None
                    else "unknown",
                }
            },
        )
        raise FindingNotFound()

    return finding


async def remove_all_evidences(finding_id: str, group_name: str) -> None:
    file_names = await findings_storage.search_evidence(
        f"{group_name}/{finding_id}"
    )
    await collect(
        findings_storage.remove_evidence(
            f'{group_name}/{finding_id}/{file_name.split("/")[-1]}'
        )
        for file_name in file_names
    )
    metadata = FindingMetadataToUpdate(evidences=FindingEvidences())
    await findings_model.update_metadata(
        group_name=group_name,
        finding_id=finding_id,
        metadata=metadata,
    )


@authz.validate_handle_comment_scope_deco(
    "loaders",
    "comment_data.content",
    "user_email",
    "group_name",
    "comment_data.parent_id",
)
@validations_deco.validate_length_deco("content", max_length=20000)
async def add_comment(
    loaders: Dataloaders,
    user_email: str,
    comment_data: FindingComment,
    finding_id: str,
    group_name: str,
) -> None:
    param_type = comment_data.comment_type
    parent_comment = (
        str(comment_data.parent_id) if comment_data.parent_id else "0"
    )
    if param_type == CommentType.OBSERVATION:
        enforcer = await authz.get_group_level_enforcer(loaders, user_email)
        if not enforcer(group_name, "post_finding_observation"):
            raise PermissionDenied()
    if parent_comment != "0":
        all_finding_comments: list[
            FindingComment
        ] = await comments_domain.get_unformatted_comments(
            loaders=loaders,
            comment_type=comment_data.comment_type,
            finding_id=finding_id,
        )
        finding_comments = {comment.id for comment in all_finding_comments}
        if parent_comment not in finding_comments:
            raise InvalidCommentParent()
    await comments_domain.add(loaders, comment_data, notify=True)


async def remove_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
    justification: VulnerabilityStateReason,
    email: str,
) -> None:
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    await collect(
        tuple(
            vulns_domain.remove_vulnerability(
                loaders=loaders,
                finding_id=finding_id,
                vulnerability_id=vulnerability.id,
                justification=justification,
                email=email,
                include_closed_vuln=True,
            )
            for vulnerability in vulnerabilities
        ),
        workers=8,
    )


def get_report_days(report_date: datetime | None) -> int:
    """Gets amount of days from a report date."""
    return (
        (datetime_utils.get_utc_now() - report_date).days if report_date else 0
    )


async def get_status(loaders: Dataloaders, finding_id: str) -> str:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    if not vulns:
        return "DRAFT"
    open_vulns = filter_vulns_utils.filter_open_vulns(vulns)
    return "VULNERABLE" if open_vulns else "SAFE"


async def get_finding_open_age(loaders: Dataloaders, finding_id: str) -> int:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = filter_vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        return (datetime_utils.get_now() - oldest_report_date).days
    return 0


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
) -> list[Vulnerability]:
    connection: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_released_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding_id,
                paginate=False,
                state_status=VulnerabilityStateStatus.VULNERABLE,
            )
        )
    )

    return [edge.node for edge in connection.edges]


async def get_open_vulnerabilities_len(
    loaders: Dataloaders, finding_id: str
) -> int:
    return len(await get_open_vulnerabilities(loaders, finding_id))


async def get_rejected_vulnerabilities(
    loaders: Dataloaders, finding_id: str
) -> int:
    drafts = await loaders.finding_vulnerabilities_draft_c.load_nodes(
        FindingVulnerabilitiesRequest(finding_id=finding_id)
    )
    return len(
        [
            draft
            for draft in drafts
            if draft.state.status is VulnerabilityStateStatus.REJECTED
        ]
    )


async def get_vulnerabilities_to_reattack(
    loaders: Dataloaders,
    finding_id: str,
) -> list[Vulnerability]:
    finding_vulns = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    return filter_vulns_utils.filter_open_vulns(
        filter_vulns_utils.filter_remediated(finding_vulns)
    )
