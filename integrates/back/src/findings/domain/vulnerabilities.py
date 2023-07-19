from .utils import (
    get_finding,
)
from aioextensions import (
    collect,
    schedule,
)
from botocore.exceptions import (
    ClientError,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    VulnNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    validations_deco,
    vulnerabilities as vulns_utils,
)
from dataloaders import (
    Dataloaders,
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
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    FindingVerification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesRequest,
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
)
from finding_comments import (
    domain as comments_domain,
)
from findings.domain import (
    core as finding_domain,
)
from findings.types import (
    Tracking,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_job_new,
)
from mailer import (
    findings as findings_mail,
)
from time import (
    time,
)
from typing import (
    Any,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def get_closed_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
) -> list[Vulnerability]:
    connection: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_released_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding_id,
                paginate=False,
                state_status=VulnerabilityStateStatus.SAFE,
            )
        )
    )

    return [edge.node for edge in connection.edges]


async def get_closed_vulnerabilities_len(
    loaders: Dataloaders,
    finding_id: str,
) -> int:
    return len(await get_closed_vulnerabilities(loaders, finding_id))


async def get_submitted_vulnerabilities(
    loaders: Dataloaders, finding_id: str
) -> int:
    drafts = await loaders.finding_vulnerabilities_draft_c.load_nodes(
        FindingVulnerabilitiesRequest(finding_id=finding_id)
    )
    return len(
        [
            draft
            for draft in drafts
            if draft.state.status is VulnerabilityStateStatus.SUBMITTED
        ]
    )


def get_tracking_vulnerabilities(
    vulns_state: Iterable[Iterable[VulnerabilityState]],
    vulns_treatment: Iterable[Iterable[VulnerabilityTreatment]],
) -> list[Tracking]:
    """Get tracking vulnerabilities dictionary."""
    states_actions = vulns_utils.get_state_actions(vulns_state)
    treatments_actions = vulns_utils.get_treatment_actions(vulns_treatment)
    tracking_actions = list(
        sorted(
            states_actions + treatments_actions,
            key=lambda action: datetime_utils.get_from_str(
                action.date, "%Y-%m-%d"
            ),
        )
    )

    return [
        Tracking(
            cycle=index,
            open=action.times if action.action == "VULNERABLE" else 0,
            closed=action.times if action.action == "SAFE" else 0,
            date=action.date,
            accepted=action.times if action.action == "ACCEPTED" else 0,
            accepted_undefined=(
                action.times if action.action == "ACCEPTED_UNDEFINED" else 0
            ),
            assigned=action.assigned,
            justification=action.justification,
            safe=action.times if action.action == "SAFE" else 0,
            vulnerable=action.times if action.action == "VULNERABLE" else 0,
        )
        for index, action in enumerate(tracking_actions)
    ]


# Validate justification length and vet characters in it
@validations_deco.validate_length_deco(
    "justification", min_length=11, max_length=10000
)
@validations_deco.validate_fields_deco(["justification"])
async def request_vulnerabilities_verification(  # noqa pylint: disable=too-many-arguments, too-many-locals
    loaders: Dataloaders,
    finding_id: str,
    user_info: dict[str, str],
    justification: str,
    vulnerability_ids: set[str],
    is_closing_event: bool = False,
) -> None:
    finding = await get_finding(loaders, finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    for vuln in vulnerabilities:
        vulns_utils.validate_released(vuln)
    vulnerabilities = list(
        await collect(
            tuple(
                vulns_utils.validate_requested_verification(
                    loaders, vuln, is_closing_event
                )
                for vuln in vulnerabilities
            )
        )
    )
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()
    root_ids = {
        vuln.root_id
        for vuln in vulnerabilities
        if vuln.root_id and not finding_domain.check_hold(vuln)
    }
    roots = await loaders.group_roots.load(finding.group_name)
    root_nicknames: tuple[str, ...] = tuple(
        root.state.nickname for root in roots if root.id in root_ids
    )
    if root_nicknames and FI_ENVIRONMENT == "production":
        with suppress(ClientError):
            if finding_code := get_finding_code_from_title(finding.title):
                await queue_job_new(
                    group_name=finding.group_name,
                    roots=list(root_nicknames),
                    finding_codes=[
                        finding_code,
                    ],
                    dataloaders=loaders,
                    clone_before=True,
                )
    comment_id = str(round(time() * 1000))
    user_email: str = user_info["user_email"]
    requester_email: str = user_info["user_email"]
    if is_closing_event:
        requester_email = (
            vulnerabilities[
                0
            ].unreliable_indicators.unreliable_last_reattack_requester
            or await vulns_domain.get_reattack_requester(
                loaders, vulnerabilities[0]
            )
            or requester_email
        )
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=requester_email,
        modified_date=datetime_utils.get_utc_now(),
        status=FindingVerificationStatus.REQUESTED,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=datetime_utils.get_utc_now(),
    )
    await comments_domain.add(loaders, comment_data)
    await collect(map(vulns_domain.request_verification, vulnerabilities))
    if any(not finding_domain.check_hold(vuln) for vuln in vulnerabilities):
        schedule(
            findings_mail.send_mail_remediate_finding(
                loaders,
                user_email,
                finding.id,
                finding.title,
                finding.group_name,
                justification,
            )
        )


# Validate justification length and vet characters in it
@validations_deco.validate_length_deco(
    "justification", min_length=11, max_length=10000
)
@validations_deco.validate_fields_deco(["justification"])
async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    context: Any | None = None,
    finding_id: str,
    user_info: dict[str, str],
    justification: str,
    open_vulns_ids: list[str],
    closed_vulns_ids: list[str],
    vulns_to_close_from_file: list[Vulnerability],
    loaders: Dataloaders,
    is_reattack_open: bool | None = None,
    is_closing_event: bool = False,
) -> None:
    # All vulns must be open before verifying them
    # we will just keep them open or close them
    # in either case, their historic_verification is updated to VERIFIED
    loaders.finding.clear(finding_id)
    finding = await get_finding(loaders, finding_id)
    vulnerability_ids = open_vulns_ids + closed_vulns_ids
    vulnerabilities = [
        vuln
        for vuln in await loaders.finding_vulnerabilities_all.load(finding_id)
        if vuln.id in vulnerability_ids
    ]
    # Sometimes vulns on hold end up being closed before the event is solved
    # Therefore, this allows these vulns to be auto-verified when it happens
    if not is_closing_event:
        vulnerabilities = [
            vulns_utils.validate_reattack_requested(vuln)
            for vuln in vulnerabilities
        ]
        vulnerabilities = [
            vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
        ]
    for vuln in vulnerabilities:
        vulns_utils.validate_released(vuln)

    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_utc_now()
    modified_by = user_info["user_email"]

    # Modify the verification state to mark the finding as verified
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=modified_by,
        modified_date=today,
        status=FindingVerificationStatus.VERIFIED,
        vulnerability_ids=set(vulnerability_ids),
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )

    if is_reattack_open is None:
        set_open_vulns_ids = set(open_vulns_ids)
        set_closed_vulns_ids = set(closed_vulns_ids)
        open_vulnerabilities = [
            vuln for vuln in vulnerabilities if vuln.id in set_open_vulns_ids
        ]
        closed_vulnerabilities = [
            vuln for vuln in vulnerabilities if vuln.id in set_closed_vulns_ids
        ]
        await finding_domain.add_reattack_justification(
            loaders=loaders,
            finding_id=finding_id,
            open_vulnerabilities=open_vulnerabilities,
            closed_vulnerabilities=closed_vulnerabilities,
            comment_type=CommentType.VERIFICATION,
            email=modified_by,
            full_name=" ".join(
                [user_info["first_name"], user_info["last_name"]]
            ),
            observations=justification,
        )
    # Modify the verification state to mark all passed vulns as verified
    await collect(map(vulns_domain.verify_vulnerability, vulnerabilities))
    # Open vulns that remain open are not modified in the DB
    # Open vulns that were closed must be persisted to the DB as closed
    await vulns_domain.verify(
        context=context,
        loaders=loaders,
        modified_date=today,
        closed_vulns_ids=closed_vulns_ids,
        vulns_to_close_from_file=vulns_to_close_from_file,
    )
