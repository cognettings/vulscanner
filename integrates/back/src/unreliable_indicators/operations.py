from . import (
    model as unreliable_indicators_model,
)
from aioextensions import (
    collect,
    resolve,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    IndicatorAlreadyUpdated,
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    events as events_model,
    findings as findings_model,
    roots as roots_model,
    vulnerabilities as vulns_model,
)
from db_model.events.types import (
    EventRequest,
    EventUnreliableIndicatorsToUpdate,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerificationSummary,
)
from db_model.roots.types import (
    RootUnreliableIndicatorsToUpdate,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityUnreliableIndicatorsToUpdate,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from events import (
    domain as events_domain,
)
from findings import (
    domain as findings_domain,
)
from functools import (
    partial,
)
import logging
import logging.config
from roots import (
    update as roots_update,
    utils as roots_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Awaitable,
    cast,
    Iterable,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.types import (
    Treatments,
    Verifications,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


@retry_on_exceptions(
    exceptions=(
        IndicatorAlreadyUpdated,
        UnavailabilityError,
    ),
    max_attempts=20,
    sleep_seconds=0,
)
async def update_event_unreliable_indicators(
    loaders: Dataloaders,
    event_id: str,
    group_name: str,
    attrs_to_update: set[EntityAttr],
) -> None:
    event = await events_domain.get_event(
        loaders, EventRequest(event_id=event_id, group_name=group_name)
    )
    indicators = {}

    if EntityAttr.solving_date in attrs_to_update:
        indicators[EntityAttr.solving_date] = events_domain.get_solving_date(
            loaders, event.id
        )

    result = dict(zip(indicators.keys(), await collect(indicators.values())))

    await events_model.update_unreliable_indicators(
        current_value=event,
        indicators=EventUnreliableIndicatorsToUpdate(
            unreliable_solving_date=result.get(EntityAttr.solving_date),
            clean_unreliable_solving_date=(
                EntityAttr.solving_date in result
                and result[EntityAttr.solving_date] is None
            ),
        ),
    )


async def update_events_unreliable_indicators(
    event_ids: list[tuple[str, str]],
    attrs_to_update: set[EntityAttr],
) -> None:
    loaders = get_new_context()
    await collect(
        tuple(
            update_event_unreliable_indicators(
                loaders,
                event_id,
                group_name,
                attrs_to_update,
            )
            for group_name, event_id in set(event_ids)
        )
    )


def _format_unreliable_status(status: str | None) -> FindingStatus | None:
    unreliable_status = None
    if status:
        unreliable_status = FindingStatus[status.upper()]
    return unreliable_status


def _format_unreliable_treatment_summary(
    treatment_summary: Treatments | None,
) -> FindingTreatmentSummary | None:
    unreliable_treatment_summary = None
    if treatment_summary:
        unreliable_treatment_summary = FindingTreatmentSummary(
            accepted=treatment_summary.accepted,
            accepted_undefined=treatment_summary.accepted_undefined,
            in_progress=treatment_summary.in_progress,
            untreated=treatment_summary.untreated,
        )
    return unreliable_treatment_summary


def _format_unreliable_verification_summary(
    verification_summary: Verifications | None,
) -> FindingVerificationSummary | None:
    unreliable_verification_summary = None
    if verification_summary:
        unreliable_verification_summary = FindingVerificationSummary(
            requested=verification_summary.requested,
            on_hold=verification_summary.on_hold,
            verified=verification_summary.verified,
        )
    return unreliable_verification_summary


async def update_findings_unreliable_indicators(
    finding_ids: list[str],
    attrs_to_update: set[EntityAttr],
) -> None:
    await collect(
        tuple(
            update_finding_unreliable_indicators(
                finding_id,
                attrs_to_update,
            )
            for finding_id in set(finding_ids)
        )
    )


@retry_on_exceptions(
    exceptions=(
        IndicatorAlreadyUpdated,
        UnavailabilityError,
    ),
    max_attempts=20,
    sleep_seconds=0,
)
async def update_finding_unreliable_indicators(
    finding_id: str,
    attrs_to_update: set[EntityAttr],
) -> None:
    loaders = get_new_context()
    finding = await findings_domain.get_finding(loaders, finding_id)
    indicator_functions: dict[EntityAttr, partial] = {
        EntityAttr.closed_vulnerabilities: partial(
            findings_domain.get_closed_vulnerabilities_len,
            loaders,
            finding.id,
        ),
        EntityAttr.max_open_severity_score: partial(
            findings_domain.get_max_open_severity_score,
            loaders,
            finding.id,
        ),
        EntityAttr.newest_vulnerability_report_date: partial(
            findings_domain.get_newest_vulnerability_report_date,
            loaders,
            finding.id,
        ),
        EntityAttr.oldest_open_vulnerability_report_date: partial(
            findings_domain.get_oldest_open_vulnerability_report_date,
            loaders,
            finding.id,
        ),
        EntityAttr.oldest_vulnerability_report_date: partial(
            findings_domain.get_oldest_vulnerability_report_date,
            loaders,
            finding.id,
        ),
        EntityAttr.open_vulnerabilities: partial(
            findings_domain.get_open_vulnerabilities_len,
            loaders,
            finding.id,
        ),
        EntityAttr.rejected_vulnerabilities: partial(
            findings_domain.get_rejected_vulnerabilities,
            loaders,
            finding.id,
        ),
        EntityAttr.status: partial(
            findings_domain.get_status,
            loaders,
            finding.id,
        ),
        EntityAttr.submitted_vulnerabilities: partial(
            findings_domain.get_submitted_vulnerabilities,
            loaders,
            finding.id,
        ),
        EntityAttr.total_open_cvssf: partial(
            findings_domain.get_total_open_cvssf,
            loaders,
            finding.id,
        ),
        EntityAttr.treatment_summary: partial(
            findings_domain.get_treatment_summary,
            loaders,
            finding.id,
        ),
        EntityAttr.verification_summary: partial(
            findings_domain.get_verification_summary,
            loaders,
            finding.id,
        ),
        EntityAttr.where: partial(
            findings_domain.get_where,
            loaders,
            finding.id,
        ),
    }
    indicators: dict[EntityAttr, Any] = {
        indicator: indicator_function()
        for indicator, indicator_function in indicator_functions.items()
        if indicator in attrs_to_update
    }
    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators_to_update = FindingUnreliableIndicatorsToUpdate(
        unreliable_closed_vulnerabilities=result.get(
            EntityAttr.closed_vulnerabilities
        ),
        unreliable_max_open_severity_score=result.get(
            EntityAttr.max_open_severity_score
        ),
        unreliable_newest_vulnerability_report_date=result.get(
            EntityAttr.newest_vulnerability_report_date
        ),
        unreliable_oldest_open_vulnerability_report_date=result.get(
            EntityAttr.oldest_open_vulnerability_report_date
        ),
        unreliable_oldest_vulnerability_report_date=result.get(
            EntityAttr.oldest_vulnerability_report_date
        ),
        unreliable_open_vulnerabilities=result.get(
            EntityAttr.open_vulnerabilities
        ),
        unreliable_rejected_vulnerabilities=result.get(
            EntityAttr.rejected_vulnerabilities
        ),
        unreliable_status=_format_unreliable_status(
            result.get(EntityAttr.status)
        ),
        unreliable_submitted_vulnerabilities=result.get(
            EntityAttr.submitted_vulnerabilities
        ),
        unreliable_total_open_cvssf=result.get(EntityAttr.total_open_cvssf),
        unreliable_treatment_summary=_format_unreliable_treatment_summary(
            result.get(EntityAttr.treatment_summary)
        ),
        unreliable_verification_summary=(
            _format_unreliable_verification_summary(
                result.get(EntityAttr.verification_summary)
            )
        ),
        unreliable_where=result.get(EntityAttr.where),
        clean_unreliable_newest_vulnerability_report_date=(
            EntityAttr.newest_vulnerability_report_date in result
            and result[EntityAttr.newest_vulnerability_report_date] is None
        ),
        clean_unreliable_oldest_open_vulnerability_report_date=(
            EntityAttr.oldest_open_vulnerability_report_date in result
            and result[EntityAttr.oldest_open_vulnerability_report_date]
            is None
        ),
        clean_unreliable_oldest_vulnerability_report_date=(
            EntityAttr.oldest_vulnerability_report_date in result
            and result[EntityAttr.oldest_vulnerability_report_date] is None
        ),
    )
    await findings_model.update_unreliable_indicators(
        current_value=finding.unreliable_indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=indicators_to_update,
    )


async def update_vulnerabilities_unreliable_indicators(
    vulnerability_ids: list[str],
    attrs_to_update: set[EntityAttr],
) -> None:
    # Placed the loader here since the same finding_historic_verification is
    # shared by many vulnerabilities
    loaders = get_new_context()
    await collect(
        tuple(
            update_vulnerability_unreliable_indicators(
                loaders,
                vulnerability_id,
                attrs_to_update,
            )
            for vulnerability_id in set(vulnerability_ids)
        ),
        workers=32,
    )


async def update_root_unreliable_indicators(
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    attrs_to_update: set[EntityAttr],
) -> None:
    root = await roots_utils.get_root(loaders, root_id, group_name)
    indicators = {}

    if EntityAttr.last_status_update in attrs_to_update:
        indicators[
            EntityAttr.last_status_update
        ] = roots_update.get_last_status_update_date(loaders, root.id)

    result = dict(zip(indicators.keys(), await collect(indicators.values())))

    with suppress(IndicatorAlreadyUpdated):
        await roots_model.update_unreliable_indicators(
            current_value=root,
            indicators=RootUnreliableIndicatorsToUpdate(
                unreliable_last_status_update=result.get(
                    EntityAttr.last_status_update
                ),
            ),
        )


async def update_roots_unreliable_indicators(
    root_ids: list[tuple[str, str]],
    attrs_to_update: set[EntityAttr],
) -> None:
    loaders = get_new_context()
    await collect(
        tuple(
            update_root_unreliable_indicators(
                loaders,
                group_name,
                root_id,
                attrs_to_update,
            )
            for group_name, root_id in set(root_ids)
        )
    )


@retry_on_exceptions(
    exceptions=(
        IndicatorAlreadyUpdated,
        UnavailabilityError,
    ),
    max_attempts=20,
    sleep_seconds=float("0.2"),
)
async def update_vulnerability_unreliable_indicators(
    loaders: Dataloaders,
    vulnerability_id: str,
    attrs_to_update: set[EntityAttr],
) -> None:
    try:
        vulnerability = await vulns_domain.get_vulnerability(
            loaders, vulnerability_id
        )
    except VulnNotFound as exc:
        LOGGER.exception(
            exc, extra=dict(extra=dict(vulnerability_id=vulnerability_id))
        )
        return

    indicators = _get_new_vulnerability_indicators(
        loaders, attrs_to_update, vulnerability
    )
    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators_to_udpate = VulnerabilityUnreliableIndicatorsToUpdate(
        unreliable_closing_date=result.get(EntityAttr.closing_date),
        unreliable_efficacy=result.get(EntityAttr.efficacy),
        unreliable_last_reattack_date=result.get(
            EntityAttr.last_reattack_date
        ),
        unreliable_last_reattack_requester=result.get(
            EntityAttr.last_reattack_requester
        ),
        unreliable_last_requested_reattack_date=result.get(
            EntityAttr.last_requested_reattack_date
        ),
        unreliable_reattack_cycles=result.get(EntityAttr.reattack_cycles),
        unreliable_report_date=result.get(EntityAttr.report_date),
        unreliable_treatment_changes=result.get(EntityAttr.treatment_changes),
        clean_unreliable_closing_date=(
            EntityAttr.closing_date in result
            and result[EntityAttr.closing_date] is None
        ),
        clean_unreliable_last_reattack_date=(
            EntityAttr.last_reattack_date in result
            and result[EntityAttr.last_reattack_date] is None
        ),
        clean_unreliable_last_requested_reattack_date=(
            EntityAttr.last_requested_reattack_date in result
            and result[EntityAttr.last_requested_reattack_date] is None
        ),
    )

    await vulns_model.update_unreliable_indicators(
        current_value=vulnerability,
        indicators=indicators_to_udpate,
    )


def _get_new_vulnerability_indicators(
    loaders: Dataloaders,
    attrs_to_update: set[EntityAttr],
    vulnerability: Vulnerability,
) -> dict[EntityAttr, Any]:
    indicators: dict[EntityAttr, Any] = {}
    if EntityAttr.closing_date in attrs_to_update:
        indicators[EntityAttr.closing_date] = vulns_domain.get_closing_date(
            vulnerability
        )

    if EntityAttr.efficacy in attrs_to_update:
        indicators[EntityAttr.efficacy] = vulns_domain.get_efficacy(
            loaders, vulnerability
        )

    if EntityAttr.last_reattack_date in attrs_to_update:
        indicators[
            EntityAttr.last_reattack_date
        ] = vulns_domain.get_last_reattack_date(loaders, vulnerability)

    if EntityAttr.last_reattack_requester in attrs_to_update:
        indicators[
            EntityAttr.last_reattack_requester
        ] = vulns_domain.get_reattack_requester(loaders, vulnerability)

    if EntityAttr.last_requested_reattack_date in attrs_to_update:
        indicators[
            EntityAttr.last_requested_reattack_date
        ] = vulns_domain.get_last_requested_reattack_date(
            loaders, vulnerability
        )

    if EntityAttr.reattack_cycles in attrs_to_update:
        indicators[
            EntityAttr.reattack_cycles
        ] = vulns_domain.get_reattack_cycles(loaders, vulnerability)

    if EntityAttr.report_date in attrs_to_update:
        indicators[EntityAttr.report_date] = vulns_domain.get_report_date(
            vulnerability
        )

    if EntityAttr.treatment_changes in attrs_to_update:
        indicators[
            EntityAttr.treatment_changes
        ] = vulns_domain.get_treatment_changes(loaders, vulnerability)

    return indicators


async def _collect_handling_errors(
    awaitables: Iterable[Awaitable[Any]], error_message: str
) -> None:
    """Temporal method for using collect function but handling errors"""
    for item in resolve(awaitables, workers=1024):
        try:
            await item
        except Exception as error:  # pylint: disable=broad-except
            error_body = {
                "type": type(error).__name__,
                "message": f"{error}",
                "cause": error.__cause__,
                "context": error.__context__,
            }
            extra = dict(extra=error_body)
            LOGGER.error(error_message, extra=extra)


async def update_unreliable_indicators_by_deps(
    dependency: EntityDependency, **args: list[Any]
) -> None:
    entities_to_update = (
        unreliable_indicators_model.get_entities_to_update_by_dependency(
            dependency, **args
        )
    )
    updates = []
    dependent_updates = []

    if Entity.event in entities_to_update:
        updates.append(
            update_events_unreliable_indicators(
                entities_to_update[Entity.event].entity_ids[EntityId.ids],
                entities_to_update[Entity.event].attributes_to_update,
            )
        )

    if Entity.finding in entities_to_update:
        dependent_updates.append(
            update_findings_unreliable_indicators(
                entities_to_update[Entity.finding].entity_ids[EntityId.ids],
                entities_to_update[Entity.finding].attributes_to_update,
            )
        )

    if Entity.root in entities_to_update:
        updates.append(
            update_roots_unreliable_indicators(
                cast(
                    list[tuple[str, str]],
                    entities_to_update[Entity.root].entity_ids[EntityId.ids],
                ),
                entities_to_update[Entity.root].attributes_to_update,
            )
        )

    if Entity.vulnerability in entities_to_update:
        updates.append(
            update_vulnerabilities_unreliable_indicators(
                entities_to_update[Entity.vulnerability].entity_ids[
                    EntityId.ids
                ],
                entities_to_update[Entity.vulnerability].attributes_to_update,
            )
        )

    await _collect_handling_errors(
        awaitables=updates,
        error_message="Updating unreliable indicators failed",
    )
    await _collect_handling_errors(
        awaitables=dependent_updates,
        error_message="Updating unreliable indicators failed",
    )
