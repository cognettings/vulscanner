# pylint:disable=cyclic-import
from . import (
    validations as events_validations,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from custom_exceptions import (
    EventAlreadyClosed,
    EventHasNotBeenSolved,
    EventNotFound,
    EventVerificationAlreadyRequested,
    EventVerificationNotRequested,
    GroupNotFound,
    InvalidCommentParent,
    InvalidDate,
    InvalidEventSolvingReason,
    InvalidFileSize,
    InvalidFileType,
    InvalidParameter,
    RequiredFieldToBeUpdate,
    VulnNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    files as files_utils,
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
    events as events_model,
    findings as findings_model,
)
from db_model.event_comments.types import (
    EventComment,
    EventCommentsRequest,
)
from db_model.events.enums import (
    EventEvidenceId,
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventMetadataToUpdate,
    EventRequest,
    EventState,
    GroupEventsRequest,
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
    Vulnerability,
)
from event_comments import (
    domain as event_comments_domain,
)
from events.constants import (
    FILE_EVIDENCE_IDS,
    IMAGE_EVIDENCE_IDS,
    SOLUTION_REASON_BY_EVENT_TYPE,
)
from events.types import (
    EventAttributesToUpdate,
)
from finding_comments import (
    domain as finding_comments_domain,
)
from findings import (
    domain as findings_domain,
)
from findings.domain.evidence import (
    validate_evidence_name,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from mailer import (
    events as events_mail,
)
import pytz
import random
from roots import (
    utils as roots_utils,
)
from s3 import (
    operations as s3_ops,
)
from sessions import (
    domain as sessions_domain,
)
from settings import (
    LOGGING,
    TIME_ZONE,
)
from starlette.datastructures import (
    UploadFile,
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def save_evidence(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"evidences/{file_name}",
    )


async def search_evidence(file_name: str) -> list[str]:
    return await s3_ops.list_files(f"evidences/{file_name}")


async def remove_file_evidence(file_name: str) -> None:
    await s3_ops.remove_file(file_name)


async def get_event(loaders: Dataloaders, request: EventRequest) -> Event:
    event = await loaders.event.load(request)
    if event is None:
        raise EventNotFound()

    return event


@authz.validate_handle_comment_scope_deco(
    "loaders", "content", "email", "group_name", "parent_comment"
)
async def _check_invalid_comment(  # pylint: disable=unused-argument
    *,
    loaders: Dataloaders,
    content: str,
    email: str,
    group_name: str,
    parent_comment: str,
    event_id: str,
) -> None:
    if parent_comment != "0":
        event_comments = await loaders.event_comments.load(
            EventCommentsRequest(event_id=event_id, group_name=group_name)
        )
        event_comments_ids = [comment.id for comment in event_comments]

        if parent_comment not in event_comments_ids:
            raise InvalidCommentParent()


@validations_deco.validate_length_deco(
    "comment_data.content", max_length=20000
)
@validations_deco.validate_fields_deco(["comment_data.content"])
async def add_comment(
    *,
    loaders: Dataloaders,
    comment_data: EventComment,
    email: str,
    event_id: str,
    group_name: str,
    parent_comment: str,
) -> None:
    parent_comment = str(parent_comment)
    content = comment_data.content
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    group_name = event.group_name

    await _check_invalid_comment(
        loaders=loaders,
        content=content,
        email=email,
        group_name=group_name,
        parent_comment=parent_comment,
        event_id=event_id,
    )

    await event_comments_domain.add(comment_data)


@validations_deco.validate_length_deco("detail", max_length=300)
@validations_deco.validate_fields_deco(["detail", "root_id"])
async def add_event(
    loaders: Dataloaders,
    hacker_email: str,
    group_name: str,
    **kwargs: Any,
) -> str:
    root_id: str | None = kwargs.get("root_id")
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    if root_id:
        root = await roots_utils.get_root(loaders, root_id, group_name)
        root_id = root.id
        if root.state.status != "ACTIVE":
            raise InvalidParameter(field="rootId")

    tzn = pytz.timezone(TIME_ZONE)
    event_date: datetime = kwargs["event_date"].astimezone(tzn)
    if event_date > datetime_utils.get_now():
        raise InvalidDate()

    created_date = datetime_utils.get_utc_now()
    event = Event(
        client=group.organization_id,
        created_by=hacker_email,
        created_date=created_date,
        description=kwargs["detail"],
        event_date=event_date,
        evidences=EventEvidences(),
        group_name=group_name,
        hacker=hacker_email,
        id=str(random.randint(10000000, 170000000)),  # nosec
        root_id=root_id,
        state=EventState(
            modified_by=hacker_email,
            modified_date=event_date,
            status=EventStateStatus.OPEN,
        ),
        type=EventType[kwargs["event_type"]],
    )
    await events_model.add(event=event)
    await events_model.update_state(
        current_value=event,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=created_date,
            status=EventStateStatus.CREATED,
        ),
    )

    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event.id,
            event_type=event.type,
            description=event.description,
            root_id=event.root_id,
            report_date=event.event_date.date(),
        )
    )

    return event.id


async def get_unsolved_events(
    loaders: Dataloaders, group_name: str
) -> list[Event]:
    events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    unsolved: list[Event] = [
        event
        for event in events
        if event.state.status == EventStateStatus.CREATED
    ]
    return unsolved


async def get_evidence_link(
    loaders: Dataloaders,
    event_id: str,
    file_name: str,
    group_name: str,
) -> str:
    await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    file_url = f"evidences/{group_name}/{event_id}/{file_name}"
    return await s3_ops.sign_url(file_url, 10)


async def get_solving_state(
    loaders: Dataloaders, event_id: str
) -> EventState | None:
    historic_states = await loaders.event_historic_state.load(event_id)
    for state in sorted(
        historic_states,
        key=lambda state: state.modified_date,
    ):
        if state.status == EventStateStatus.SOLVED:
            return state

    return None


async def get_solving_date(
    loaders: Dataloaders, event_id: str
) -> datetime | None:
    """Returns the date of the last closing state."""
    last_closing_state = await get_solving_state(loaders, event_id)

    return last_closing_state.modified_date if last_closing_state else None


async def has_access_to_event(
    loaders: Dataloaders, email: str, event_id: str, group_name: str
) -> bool:
    """Verify if the user has access to a event submission."""
    await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    return await authz.has_access_to_group(loaders, email, group_name)


async def remove_event(event_id: str, group_name: str) -> None:
    evidence_prefix = f"{group_name}/{event_id}"
    list_evidences = await search_evidence(evidence_prefix)
    await collect(
        [
            *[remove_file_evidence(file_name) for file_name in list_evidences],
            event_comments_domain.remove_comments(event_id, group_name),
        ]
    )
    await events_model.remove(event_id=event_id)
    LOGGER.info(
        "Event removed",
        extra={
            "extra": {
                "event_id": event_id,
                "group_name": group_name,
            }
        },
    )


async def remove_evidence(
    loaders: Dataloaders,
    evidence_id: EventEvidenceId,
    event_id: str,
    group_name: str,
) -> None:
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    group_name = event.group_name

    if (
        evidence := getattr(
            event.evidences, str(evidence_id.value).lower(), None
        )
    ) and isinstance(evidence, EventEvidence):
        full_name = f"evidences/{group_name}/{event_id}/{evidence.file_name}"
        await s3_ops.remove_file(full_name)
        await events_model.update_evidence(
            event_id=event_id,
            group_name=group_name,
            evidence_info=None,
            evidence_id=evidence_id,
        )


async def solve_event(  # pylint: disable=too-many-locals,too-many-arguments
    info: GraphQLResolveInfo,
    event_id: str,
    group_name: str,
    hacker_email: str,
    reason: EventSolutionReason,
    other: str | None,
) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    """Solves an Event, can either return two empty dicts or
    the `reattacks_dict[finding_id, set_of_respective_vuln_ids]`
    and the `verifications_dict[finding_id, list_of_respective_vuln_ids]`"""
    loaders: Dataloaders = info.context.loaders
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    other_reason: str = other if other else ""

    if event.state.status == EventStateStatus.SOLVED:
        raise EventAlreadyClosed()

    if reason not in SOLUTION_REASON_BY_EVENT_TYPE[event.type]:
        raise InvalidEventSolvingReason()

    affected_reattacks = await loaders.event_vulnerabilities_loader.load(
        event_id
    )
    has_reattacks: bool = len(affected_reattacks) > 0
    if has_reattacks:
        user_info = await sessions_domain.get_jwt_content(info.context)
        # For open vulns on hold
        reattacks_dict: dict[str, set[str]] = {}
        # For closed vulns on hold (yes, that can happen)
        verifications_dict: dict[str, list[str]] = {}
        for vuln in affected_reattacks:
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE:
                reattacks_dict.setdefault(vuln.finding_id, set()).add(vuln.id)
            elif vuln.state.status == VulnerabilityStateStatus.SAFE:
                verifications_dict.setdefault(vuln.finding_id, []).append(
                    vuln.id
                )

        for finding_id, reattack_ids in reattacks_dict.items():
            await findings_domain.request_vulnerabilities_verification(
                loaders=loaders,
                finding_id=finding_id,
                user_info=user_info,
                justification=(
                    f"Event #{event_id} was solved. The reattacks are back to "
                    "the Requested stage."
                ),
                vulnerability_ids=reattack_ids,
                is_closing_event=True,
            )
        for finding_id, verification_ids in verifications_dict.items():
            # Mark all closed vulns as verified
            await findings_domain.verify_vulnerabilities(
                context=info.context,
                finding_id=finding_id,
                user_info=user_info,
                justification=(
                    f"Event #{event_id} was solved. As these vulnerabilities "
                    "were closed, the reattacks are set to Verified."
                ),
                open_vulns_ids=[],
                closed_vulns_ids=verification_ids,
                vulns_to_close_from_file=[],
                is_closing_event=True,
                loaders=loaders,
            )

    await events_model.update_state(
        current_value=event,
        group_name=group_name,
        state=EventState(
            modified_by=hacker_email,
            modified_date=datetime_utils.get_utc_now(),
            other=other_reason,
            reason=reason,
            status=EventStateStatus.SOLVED,
        ),
    )

    schedule(
        events_mail.send_mail_event_report(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            event_type=event.type.value,
            description=event.description,
            root_id=event.root_id,
            reason=reason.value,
            other=other,
            is_closed=True,
            report_date=event.event_date.date(),
        )
    )

    if has_reattacks:
        return (reattacks_dict, verifications_dict)
    return ({}, {})


@validations_deco.validate_fields_deco(["comments"])
async def reject_solution(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    event_id: str,
    comments: str,
    group_name: str,
    stakeholder_email: str,
    stakeholder_full_name: str,
) -> None:
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    if event.state.status is not EventStateStatus.VERIFICATION_REQUESTED:
        raise EventVerificationNotRequested()

    comment_id: str = str(round(time() * 1000))
    parent_comment_id = (
        event.state.comment_id if event.state.comment_id else "0"
    )
    await add_comment(
        loaders=loaders,
        comment_data=EventComment(
            event_id=event.id,
            group_name=group_name,
            parent_id=parent_comment_id,
            id=comment_id,
            content=comments,
            creation_date=datetime_utils.get_utc_now(),
            email=stakeholder_email,
            full_name=stakeholder_full_name,
        ),
        email=stakeholder_email,
        event_id=event.id,
        group_name=group_name,
        parent_comment=parent_comment_id,
    )
    await events_model.update_state(
        current_value=event,
        group_name=event.group_name,
        state=EventState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            comment_id=comment_id,
            status=EventStateStatus.CREATED,
        ),
    )


@validations_deco.validate_fields_deco(["comments"])
async def request_verification(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    event_id: str,
    comments: str,
    group_name: str,
    stakeholder_email: str,
    stakeholder_full_name: str,
) -> None:
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    if event.state.status is EventStateStatus.SOLVED:
        raise EventAlreadyClosed()
    if event.state.status is EventStateStatus.VERIFICATION_REQUESTED:
        raise EventVerificationAlreadyRequested()

    comment_id: str = str(round(time() * 1000))
    await add_comment(
        loaders=loaders,
        comment_data=EventComment(
            event_id=event.id,
            group_name=group_name,
            parent_id="0",
            id=comment_id,
            content=comments,
            creation_date=datetime_utils.get_utc_now(),
            email=stakeholder_email,
            full_name=stakeholder_full_name,
        ),
        email=stakeholder_email,
        event_id=event.id,
        group_name=group_name,
        parent_comment="0",
    )
    await events_model.update_state(
        current_value=event,
        group_name=event.group_name,
        state=EventState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            comment_id=comment_id,
            status=EventStateStatus.VERIFICATION_REQUESTED,
        ),
    )


async def update_event(
    loaders: Dataloaders,
    event_id: str,
    group_name: str,
    stakeholder_email: str,
    attributes: EventAttributesToUpdate,
) -> None:
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    solving_reason = attributes.solving_reason or event.state.reason
    other_solving_reason = (
        attributes.other_solving_reason or event.state.other
        if solving_reason == EventSolutionReason.OTHER
        else None
    )
    event_type = attributes.event_type or event.type
    if all(attribute is None for attribute in attributes):
        raise RequiredFieldToBeUpdate()

    if attributes.event_type:
        events_validations.validate_type(attributes.event_type)

    if (
        solving_reason == EventSolutionReason.OTHER
        and not other_solving_reason
    ):
        raise InvalidParameter("otherSolvingReason")

    if (
        solving_reason is not None
        and event.state.status != EventStateStatus.SOLVED
    ):
        raise EventHasNotBeenSolved()

    if (
        event.state.status == EventStateStatus.SOLVED
        and solving_reason not in SOLUTION_REASON_BY_EVENT_TYPE[event_type]
    ):
        raise InvalidEventSolvingReason()

    if attributes.event_type:
        await events_model.update_metadata(
            event_id=event.id,
            group_name=event.group_name,
            metadata=EventMetadataToUpdate(type=attributes.event_type),
        )

    if (
        attributes.solving_reason != event.state.reason
        or attributes.other_solving_reason != event.state.other
    ):
        await events_model.update_state(
            current_value=event,
            group_name=event.group_name,
            state=EventState(
                modified_by=stakeholder_email,
                modified_date=datetime_utils.get_utc_now(),
                other=other_solving_reason,
                reason=solving_reason,
                status=event.state.status,
            ),
        )


async def replace_different_format(
    *, event: Event, evidence_id: EventEvidenceId, extension: str
) -> None:
    evidence: EventEvidence | None = getattr(
        event.evidences, str(evidence_id.value).lower()
    )
    if evidence:
        old_full_name = (
            f"evidences/{event.group_name}/{event.id}/{evidence.file_name}"
        )
        ends: str = old_full_name.rsplit(".", 1)[-1]
        if ends != old_full_name and f".{ends}" != extension:
            await remove_file_evidence(old_full_name)


def _get_file_name(
    group_name: str, event_id: str, value: str, extension: str
) -> str:
    return f"{group_name}_{event_id}_evidence_{value}{extension}"


@validations_deco.validate_sanitized_csv_input_deco(
    ["group_name", "event_id", "file_name"]
)
def _get_full_name(group_name: str, event_id: str, file_name: str) -> str:
    return f"{group_name}/{event_id}/{file_name}"


@validations_deco.validate_sanitized_csv_input_deco(
    ["event_id", "file.filename", "file.content_type"]
)
async def update_evidence(
    *,
    loaders: Dataloaders,
    event_id: str,
    evidence_id: EventEvidenceId,
    file: UploadFile,
    group_name: str,
    update_date: datetime,
) -> None:
    event = await get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    if event.state.status == EventStateStatus.SOLVED:
        raise EventAlreadyClosed()

    extension = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
        "video/webm": ".webm",
    }.get(file.content_type, "")
    group_name = event.group_name
    file_name = _get_file_name(
        group_name=group_name,
        event_id=event_id,
        value=str(evidence_id.value).lower(),
        extension=extension,
    )
    full_name = _get_full_name(
        group_name=group_name, event_id=event_id, file_name=file_name
    )

    await collect(
        (
            save_evidence(file, full_name),
            events_model.update_evidence(
                event_id=event_id,
                group_name=group_name,
                evidence_info=EventEvidence(
                    file_name=file_name,
                    modified_date=update_date,
                ),
                evidence_id=evidence_id,
            ),
        )
    )

    await replace_different_format(
        event=event, evidence_id=evidence_id, extension=extension
    )


@validations_deco.validate_file_name_deco("file.filename")
@validations_deco.validate_fields_deco(["file.content_type"])
async def validate_evidence(
    *,
    group_name: str,
    organization_name: str,
    evidence_id: EventEvidenceId,
    file: UploadFile,
) -> None:
    mib = 1048576

    if evidence_id in IMAGE_EVIDENCE_IDS:
        allowed_mimes = ["image/jpeg", "image/png", "video/webm"]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_IMAGE")
    elif evidence_id in FILE_EVIDENCE_IDS:
        allowed_mimes = [
            "application/csv",
            "application/pdf",
            "application/zip",
            "text/csv",
            "text/plain",
        ]
        if not await files_utils.assert_uploaded_file_mime(
            file, allowed_mimes
        ):
            raise InvalidFileType("EVENT_FILE")
    else:
        raise InvalidFileType("EVENT")

    if await files_utils.get_file_size(file) > 10 * mib:
        raise InvalidFileSize()

    validate_evidence_name(
        organization_name=organization_name.lower(),
        group_name=group_name.lower(),
        filename=file.filename.lower(),
    )


async def request_vulnerabilities_hold(
    loaders: Dataloaders,
    finding_id: str,
    event_id: str,
    user_info: dict[str, str],
    vulnerability_ids: set[str],
) -> None:
    vulnerabilities: tuple[Vulnerability, ...] | list[Vulnerability]
    justification: str = (
        f"These reattacks have been put on hold because of Event #{event_id}"
    )
    finding = await findings_domain.get_finding(loaders, finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    vulnerabilities = [
        vulns_utils.validate_requested_hold(vuln) for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    for vuln in vulnerabilities:
        vulns_utils.validate_released(vuln)

    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    user_email = str(user_info["user_email"])
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        status=FindingVerificationStatus.ON_HOLD,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    await collect(
        vulns_domain.request_hold(event_id, vuln) for vuln in vulnerabilities
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        creation_date=datetime_utils.get_utc_now(),
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
    )
    await finding_comments_domain.add(loaders, comment_data)
