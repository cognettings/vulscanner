# pylint:disable=too-many-lines
from aioextensions import (
    collect,
    schedule,
)
import authz
from authz.validations import (
    validate_fluidattacks_staff_on_group_deco,
    validate_role_fluid_reqs_deco,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from batch.types import (
    BatchProcessing,
)
import bugsnag
from collections import (
    Counter,
)
from collections.abc import (
    Awaitable,
    Callable,
)
from context import (
    BASE_URL,
    FI_ENVIRONMENT,
)
from custom_exceptions import (
    AlreadyPendingDeletion,
    BillingSubscriptionSameActive,
    ErrorUpdatingGroup,
    GroupHasPendingActions,
    GroupNotFound,
    InvalidAcceptanceSeverityRange,
    InvalidGroupName,
    InvalidGroupServicesConfig,
    InvalidGroupTier,
    InvalidManagedChange,
    InvalidParameter,
    RepeatedValues,
    StakeholderNotInOrganization,
    TrialRestriction,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
    filter_vulnerabilities as filter_vulns_utils,
    findings as findings_utils,
    groups as groups_utils,
    vulnerabilities as vulns_utils,
)
from custom_utils.findings import (
    get_group_findings,
)
from custom_utils.validations import (
    is_fluid_staff,
)
from custom_utils.validations_deco import (
    validate_alphanumeric_field_deco,
    validate_email_address_deco,
    validate_fields_deco,
    validate_file_exists_deco,
    validate_file_name_deco,
    validate_group_language_deco,
    validate_group_name_deco,
    validate_int_range_deco,
    validate_length_deco,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
from db_model import (
    forces as forces_model,
    groups as groups_model,
    toe_inputs as toe_inputs_model,
    toe_lines as toe_lines_model,
    toe_ports as toe_ports_model,
)
from db_model.constants import (
    POLICIES_FORMATTED,
)
from db_model.events.types import (
    GroupEventsRequest,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupInvitation,
)
from db_model.groups.constants import (
    MASKED,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateJustification,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupMetadataToUpdate,
    GroupState,
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
)
from db_model.types import (
    PoliciesToUpdate,
)
from db_model.utils import (
    get_min_iso_date,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from decimal import (
    Decimal,
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
import functools
from group_access import (
    domain as group_access_domain,
)
from group_comments import (
    domain as group_comments_domain,
)
import logging
import logging.config
from mailer import (
    groups as groups_mail,
    utils as mailer_utils,
)
from notifications import (
    domain as notifications_domain,
)
from organization_access import (
    domain as org_access,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
import re
from resources import (
    domain as resources_domain,
)
from roots import (
    domain as roots_domain,
)
from sessions import (
    domain as sessions_domain,
)
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from trials import (
    domain as trials_domain,
)
from typing import (
    Any,
)
from vulnerabilities.domain.validations import (
    get_policy_max_acceptance_severity,
    get_policy_min_acceptance_severity,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
TRANSACTIONS_LOGGER: logging.Logger = logging.getLogger("transactional")


async def get_group(loaders: Dataloaders, group_name: str) -> Group:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    return group


async def _has_repeated_tags(
    loaders: Dataloaders, group_name: str, tags: list[str]
) -> bool:
    has_repeated_tags = len(tags) != len(set(tags))
    if not has_repeated_tags:
        group = await loaders.group.load(group_name)
        existing_tags = group.state.tags if group else None
        all_tags = list(existing_tags or {}) + tags
        has_repeated_tags = len(all_tags) != len(set(all_tags))
    return has_repeated_tags


async def complete_register_for_group_invitation(
    loaders: Dataloaders,
    group_access: GroupAccess,
) -> None:
    invitation = group_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(
            Exception("Token already used"),
            metadata={
                "extra": {
                    "group_access": group_access,
                }
            },
            severity="warning",
        )
        return

    group_name = group_access.group_name
    email = group_access.email
    TRANSACTIONS_LOGGER.info(
        "User %s attempted to grant_group_level_role with access",
        email,
        extra={"extra": {"group_acces": group_access}},
    )
    if invitation:
        responsibility = invitation.responsibility
        role = invitation.role
        url_token = invitation.url_token

    await authz.grant_group_level_role(loaders, email, group_name, role)
    loaders.stakeholder.clear_all()
    loaders.group_access.clear_all()

    TRANSACTIONS_LOGGER.info(
        "User %s complete grant_group_level_role with access",
        email,
    )

    coroutines: list[Awaitable[None]] = []
    coroutines.append(
        group_access_domain.update(
            loaders=loaders,
            email=email,
            group_name=group_name,
            metadata=GroupAccessMetadataToUpdate(
                expiration_time=0,
                has_access=True,
                invitation=GroupInvitation(
                    is_used=True,
                    role=role,
                    url_token=url_token,
                    responsibility=responsibility,
                ),
                responsibility=responsibility,
                role=role,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_utc_now()
                ),
            ),
        )
    )
    group = await get_group(loaders, group_name)
    organization_id = group.organization_id
    if not await org_access.has_access(loaders, organization_id, email):
        coroutines.append(
            orgs_domain.add_stakeholder(
                loaders=loaders,
                organization_id=organization_id,
                email=email,
                role="user",
            )
        )

    if not await stakeholders_domain.exists(loaders, email):
        await collect(
            [
                stakeholders_domain.register(email),
                authz.grant_user_level_role(email, "user"),
            ]
        )

    loaders.stakeholder.clear(email)
    stakeholder = await loaders.stakeholder.load(email)
    if stakeholder and not stakeholder.is_registered:
        coroutines.append(stakeholders_domain.register(email))

    if stakeholder and not stakeholder.enrolled:
        coroutines.append(
            stakeholders_domain.update(
                email=email,
                metadata=StakeholderMetadataToUpdate(
                    enrolled=True,
                ),
            )
        )

    await collect(coroutines)


async def reject_register_for_group_invitation(
    loaders: Dataloaders,
    group_access: GroupAccess,
) -> None:
    invitation = group_access.invitation

    if invitation and invitation.is_used:
        bugsnag.notify(
            Exception("Token already used"),
            metadata={
                "extra": {
                    "group_access": group_access,
                }
            },
            severity="warning",
        )

    await group_access_domain.remove_access(
        loaders=loaders,
        email=group_access.email,
        group_name=group_access.group_name,
    )


def validate_group_services_config_deco(
    has_machine_field: str,
    has_squad_field: str,
    has_arm_field: str | bool,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            has_machine = bool(kwargs.get(has_machine_field))
            has_squad = bool(kwargs.get(has_squad_field))
            has_arm = has_arm_field
            if isinstance(has_arm_field, str):
                has_arm = bool(kwargs.get(has_arm_field))
            if has_squad:
                if not has_arm:
                    raise InvalidGroupServicesConfig(
                        "Squad is only available when ASM is too"
                    )
                if not has_machine:
                    raise InvalidGroupServicesConfig(
                        "Squad is only available when Machine is too"
                    )
            return func(*args, **kwargs)

        return decorated

    return wrapper


@validate_group_name_deco("group_name")
@validate_fields_deco(["description"])
@validate_length_deco("group_name", min_length=4, max_length=20)
@validate_length_deco("description", max_length=200)
@validate_group_services_config_deco(
    "has_machine",
    "has_squad",
    has_arm_field=True,
)
async def add_group(
    *,
    loaders: Dataloaders,
    description: str,
    email: str,
    granted_role: str,
    group_name: str,
    organization_name: str,
    service: GroupService,
    has_machine: bool = False,
    has_squad: bool = False,
    language: GroupLanguage = GroupLanguage.EN,
    subscription: GroupSubscriptionType = GroupSubscriptionType.CONTINUOUS,
    tier: GroupTier = GroupTier.FREE,
) -> None:
    if not description.strip() or not group_name.strip():
        raise InvalidParameter()

    organization = await orgs_utils.get_organization(
        loaders, organization_name
    )
    if not await org_access.has_access(loaders, organization.id, email):
        raise StakeholderNotInOrganization(organization.id)

    if await exists(loaders, group_name):
        raise InvalidGroupName.new()

    if await trials_domain.in_trial(loaders, email, organization):
        managed = GroupManaged.TRIAL
        if (
            await loaders.organization_groups.load(organization.id)
            or has_squad
            or not has_machine
            or service != GroupService.WHITE
            or subscription != GroupSubscriptionType.CONTINUOUS
        ):
            raise TrialRestriction()
    else:
        managed = GroupManaged.MANAGED

    await groups_model.add(
        group=Group(
            created_by=email,
            created_date=datetime_utils.get_utc_now(),
            description=description,
            language=language,
            name=group_name,
            state=GroupState(
                has_machine=has_machine,
                has_squad=has_squad,
                managed=managed,
                modified_by=email,
                modified_date=datetime_utils.get_utc_now(),
                service=service,
                status=GroupStateStatus.ACTIVE,
                tier=tier,
                type=subscription,
            ),
            organization_id=organization.id,
            sprint_duration=1,
            sprint_start_date=get_min_iso_date(datetime_utils.get_utc_now()),
        )
    )
    await orgs_domain.add_group_access(loaders, organization.id, group_name)

    # Admins are not granted access to the group
    # they are omnipresent
    if granted_role != "admin":
        await group_access_domain.update(
            loaders=loaders,
            email=email,
            group_name=group_name,
            metadata=GroupAccessMetadataToUpdate(
                has_access=True,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_utc_now()
                ),
            ),
        )
        # Only Fluid staff can be customer managers
        # Customers are granted the user manager role
        role: str = (
            "customer_manager" if is_fluid_staff(email) else "user_manager"
        )
        await authz.grant_group_level_role(loaders, email, group_name, role)

    # Notify us in case the stakeholder wants any Fluid Service
    await notifications_domain.new_group(
        description=description,
        group_name=group_name,
        has_machine=has_machine,
        has_squad=has_squad,
        organization=organization_name,
        requester_email=email,
        service=service,
        subscription=subscription,
    )


async def deactivate_all_roots(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    other: str = "",
    reason: str = "",
) -> None:
    all_group_roots = await loaders.group_roots.load(group_name)
    await collect(
        [
            roots_domain.deactivate_root(
                group_name=group_name,
                other=other,
                reason=reason,
                root=root,
                email=email,
            )
            for root in all_group_roots
        ]
    )


async def remove_group(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    justification: GroupStateJustification,
    validate_pending_actions: bool = True,
) -> None:
    """
    Update group state to DELETED and update some related resources.
    For production, remember to remove additional resources
    (stakeholder, findings, vulns ,etc) via the batch action
    remove_group_resources.
    """
    loaders.group.clear(group_name)
    group = await get_group(loaders, group_name)
    if group.state.status == GroupStateStatus.DELETED:
        raise AlreadyPendingDeletion()

    await groups_model.update_state(
        group_name=group_name,
        organization_id=group.organization_id,
        state=group.state._replace(
            comments=comments,
            modified_date=datetime_utils.get_utc_now(),
            has_machine=False,
            has_squad=False,
            justification=justification,
            modified_by=email,
            status=GroupStateStatus.DELETED,
        ),
    )

    await batch_dal.put_action(
        action=Action.REMOVE_GROUP_RESOURCES,
        entity=group_name,
        subject=email,
        additional_info=f"validate_pending_actions:{validate_pending_actions}",
        queue=IntegratesBatchQueue.SMALL,
        product_name=Product.INTEGRATES,
    )
    if FI_ENVIRONMENT == "development":
        await remove_resources(
            loaders=loaders,
            email=email,
            group_name=group_name,
        )


@validate_fields_deco(["comments"])
@validate_length_deco("comments", max_length=250)
async def update_group_managed(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    managed: GroupManaged,
    justification: GroupStateJustification = GroupStateJustification.NONE,
) -> None:
    group = await get_group(loaders, group_name)

    if managed != group.state.managed:
        if (
            managed == GroupManaged.MANAGED
            and group.state.managed == GroupManaged.UNDER_REVIEW
        ) or (
            managed == GroupManaged.UNDER_REVIEW
            and group.state.managed
            in {GroupManaged.MANAGED, GroupManaged.TRIAL}
        ):
            await update_state(
                group_name=group_name,
                organization_id=group.organization_id,
                state=GroupState(
                    comments=comments,
                    modified_date=datetime_utils.get_utc_now(),
                    has_machine=group.state.has_machine,
                    has_squad=group.state.has_squad,
                    managed=managed,
                    payment_id=group.state.payment_id,
                    justification=justification,
                    modified_by=email,
                    service=group.state.service,
                    status=GroupStateStatus.ACTIVE,
                    tags=group.state.tags,
                    tier=group.state.tier,
                    type=group.state.type,
                ),
            )
        else:
            raise InvalidManagedChange()

        if managed == GroupManaged.MANAGED:
            organization = await orgs_utils.get_organization(
                loaders, group.organization_id
            )
            await notifications_domain.request_managed(
                group_name=group_name,
                managed=managed,
                organization_name=organization.name,
                requester_email=email,
            )


@validate_fields_deco(["comments"])
@validate_length_deco("comments", max_length=250)
async def update_group_payment_id(
    *,
    group: Group,
    comments: str,
    email: str,
    group_name: str,
    payment_id: str,
    managed: GroupManaged,
) -> None:
    if payment_id != group.state.payment_id:
        await update_state(
            group_name=group_name,
            organization_id=group.organization_id,
            state=GroupState(
                comments=comments,
                modified_date=datetime_utils.get_utc_now(),
                has_machine=group.state.has_machine,
                has_squad=group.state.has_squad,
                managed=managed,
                justification=GroupStateJustification.NONE,
                modified_by=email,
                payment_id=payment_id,
                service=group.state.service,
                status=GroupStateStatus.ACTIVE,
                tags=group.state.tags,
                tier=group.state.tier,
                type=group.state.type,
            ),
        )


@validate_fields_deco(["comments"])
@validate_length_deco("comments", max_length=250)
@validate_group_services_config_deco("has_machine", "has_squad", "has_arm")
async def update_group(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    has_arm: bool,
    has_machine: bool,
    has_squad: bool,
    justification: GroupStateJustification,
    service: GroupService | None,
    subscription: GroupSubscriptionType,
    tier: GroupTier = GroupTier.OTHER,
) -> None:
    group = await get_group(loaders, group_name)
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )

    if (
        group.state.type != GroupSubscriptionType.ONESHOT
        and subscription == GroupSubscriptionType.ONESHOT
    ):
        raise InvalidGroupServicesConfig(
            "OneShot service is no longer provided"
        )

    restricted_in_trial = (
        has_squad
        or not has_machine
        or service != GroupService.WHITE
        or subscription != GroupSubscriptionType.CONTINUOUS
    )
    if (
        has_arm
        and await trials_domain.in_trial(loaders, email, organization)
        and restricted_in_trial
    ):
        raise TrialRestriction()

    if service != group.state.service:
        await deactivate_all_roots(
            loaders=loaders,
            email=email,
            group_name=group_name,
            other=comments,
            reason=justification.value,
        )
    if tier == GroupTier.OTHER:
        tier = GroupTier.FREE

    if has_arm:
        await update_state(
            group_name=group_name,
            organization_id=group.organization_id,
            state=GroupState(
                comments=comments,
                modified_date=datetime_utils.get_utc_now(),
                has_machine=has_machine,
                has_squad=has_squad,
                managed=group.state.managed,
                justification=justification,
                modified_by=email,
                service=service,
                status=GroupStateStatus.ACTIVE,
                tags=group.state.tags,
                tier=tier,
                type=subscription,
            ),
        )
        await notifications_domain.update_group(
            loaders=loaders,
            comments=comments,
            group_name=group_name,
            group_state=group.state,
            had_arm=True,
            has_arm=has_arm,
            has_machine=has_machine,
            has_squad=has_squad,
            reason=justification.value,
            requester_email=email,
            service=service.value if service else "",
            subscription=str(subscription.value).lower(),
        )
        return

    await remove_group(
        loaders=loaders,
        comments=comments,
        email=email,
        group_name=group_name,
        justification=justification,
    )
    await notifications_domain.delete_group(
        loaders=loaders,
        deletion_date=datetime_utils.get_utc_now(),
        group=group,
        requester_email=email,
        reason=justification.value,
        comments=comments,
        attempt=True,
    )


async def update_group_tier(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    tier: GroupTier,
) -> None:
    """Set a new tier for a group."""
    if tier == GroupTier.MACHINE:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = True
        has_squad = False
        service = GroupService.WHITE
    elif tier == GroupTier.SQUAD:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = True
        has_squad = True
        service = GroupService.WHITE
    elif tier == GroupTier.ONESHOT:
        subscription = GroupSubscriptionType.ONESHOT
        has_machine = False
        has_squad = False
        service = GroupService.BLACK
    elif tier == GroupTier.FREE:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = False
        has_squad = False
        service = GroupService.WHITE
    else:
        raise InvalidGroupTier()

    await update_group(
        loaders=loaders,
        comments=comments,
        email=email,
        group_name=group_name,
        justification=GroupStateJustification.OTHER,
        has_arm=True,
        has_machine=has_machine,
        has_squad=has_squad,
        service=service,
        subscription=subscription,
        tier=tier,
    )


async def get_closed_vulnerabilities(
    loaders: Dataloaders, group_name: str
) -> int:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    findings_vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in group_findings]
        )
    )
    last_approved_status = [vuln.state.status for vuln in findings_vulns]

    return last_approved_status.count(VulnerabilityStateStatus.SAFE)


async def get_groups_by_stakeholder(
    loaders: Dataloaders,
    email: str,
    active: bool = True,
    organization_id: str = "",
) -> list[str]:
    group_names = await group_access_domain.get_stakeholder_groups_names(
        loaders, email, active
    )
    if organization_id:
        org_groups = await loaders.organization_groups.load(organization_id)
        org_group_names: set[str] = set(group.name for group in org_groups)
        group_names = [
            group_name
            for group_name in group_names
            if group_name in org_group_names
        ]

    group_level_roles = await authz.get_group_level_roles(
        loaders, email, group_names
    )

    return [
        group_name
        for role, group_name in zip(group_level_roles.values(), group_names)
        if bool(role)
    ]


async def get_vulnerabilities_with_pending_attacks(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> int:
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )

    return len(
        tuple(
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.verification
            and vulnerability.verification.status
            == VulnerabilityVerificationStatus.REQUESTED
        )
    )


async def get_max_severity(
    loaders: Dataloaders,
    group_name: str,
) -> Decimal:
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    max_severity: Decimal = max(
        map(
            lambda finding: cvss_utils.get_severity_score(finding.severity),
            findings,
        ),
        default=Decimal("0.0"),
    )
    return Decimal(max_severity).quantize(Decimal("0.1"))


async def get_mean_remediate_severity_cvssf(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: date | None = None,
) -> Decimal:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= cvss_utils.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: cvss_utils.get_cvssf_score(
            cvss_utils.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities_cvssf(
        findings_vulns,
        finding_cvssf,
        min_date,
    )


async def get_mean_remediate_non_treated_severity_cvssf(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: date | None = None,
) -> Decimal:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= cvss_utils.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: cvss_utils.get_cvssf_score(
            cvss_utils.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    non_confirmed_zr_vulns = filter_vulns_utils.filter_non_confirmed_zero_risk(
        findings_vulns
    )
    non_accepted_undefined_vulns = [
        vuln
        for vuln in non_confirmed_zr_vulns
        if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
    ]
    return vulns_utils.get_mean_remediate_vulnerabilities_cvssf(
        non_accepted_undefined_vulns,
        finding_cvssf,
        min_date,
    )


async def get_mean_remediate_severity(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: date | None = None,
) -> Decimal:
    """Get mean time to remediate."""
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= cvss_utils.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        findings_vulns,
        min_date,
    )


async def get_mean_remediate_non_treated_severity(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: date | None = None,
) -> Decimal:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= cvss_utils.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    non_confirmed_zr_vulns = filter_vulns_utils.filter_non_confirmed_zero_risk(
        findings_vulns
    )
    non_accepted_undefined_vulns = [
        vuln
        for vuln in non_confirmed_zr_vulns
        if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
    ]
    return vulns_utils.get_mean_remediate_vulnerabilities(
        non_accepted_undefined_vulns,
        min_date,
    )


async def get_open_findings(loaders: Dataloaders, group_name: str) -> int:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    finding_status = await collect(
        tuple(
            findings_domain.get_status(loaders, finding.id)
            for finding in group_findings
        ),
        workers=32,
    )
    return finding_status.count("VULNERABLE")


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    group_name: str,
) -> int:
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    findings_vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in group_findings]
        )
    )
    last_approved_status = [vuln.state.status for vuln in findings_vulns]

    return last_approved_status.count(VulnerabilityStateStatus.VULNERABLE)


@validate_length_deco("responsibility", min_length=1, max_length=50)
@validate_alphanumeric_field_deco("responsibility")
@validate_email_address_deco("email")
@validate_role_fluid_reqs_deco("email", "role")
async def invite_to_group(
    *,
    loaders: Dataloaders,
    email: str,
    responsibility: str,
    role: str,
    group_name: str,
    modified_by: str,
) -> None:
    group = await get_group(loaders, group_name)

    expiration_time, url_token = generate_invitation_token(
        group=group,
        email=email,
        role=role,
    )

    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            expiration_time=expiration_time,
            has_access=False,
            invitation=GroupInvitation(
                is_used=False,
                responsibility=responsibility,
                role=role,
                url_token=url_token,
            ),
            responsibility=responsibility,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )
    confirm_access_url = f"{BASE_URL}/confirm_access/{url_token}"
    reject_access_url = f"{BASE_URL}/reject_access/{url_token}"
    mail_to = [email]
    email_context: dict[str, str] = {
        "admin": email,
        "group": group_name,
        "responsible": modified_by,
        "group_description": group.description,
        "confirm_access_url": confirm_access_url,
        "reject_access_url": reject_access_url,
        "user_role": role.replace("_", " "),
    }
    schedule(
        groups_mail.send_mail_access_granted(loaders, mail_to, email_context)
    )


@validate_fluidattacks_staff_on_group_deco("group", "email", "role")
def generate_invitation_token(
    group: Group, email: str, role: str
) -> tuple[int, str]:
    if role:
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        url_token = sessions_domain.encode_token(
            expiration_time=expiration_time,
            payload={
                "group_name": group.name,
                "user_email": email,
            },
            subject="starlette_session",
        )
    return expiration_time, url_token


async def exists(
    loaders: Dataloaders,
    group_name: str,
) -> bool:
    try:
        await get_group(loaders, group_name)
        return True
    except GroupNotFound:
        return False


async def is_valid(
    loaders: Dataloaders,
    group_name: str,
) -> bool:
    if await exists(loaders, group_name):
        group = await loaders.group.load(group_name)
        if group and group.state.status == GroupStateStatus.ACTIVE:
            return True
    return False


async def mask_files(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    group = await get_group(loaders, group_name)
    resources_files = await resources_domain.search_file(f"{group_name}/")
    if resources_files:
        await collect(
            resources_domain.remove_file(file_name)
            for file_name in resources_files
        )
    if group.files:
        masked_files: list[GroupFile] = [
            GroupFile(
                description=MASKED,
                file_name=MASKED,
                modified_by=MASKED,
                modified_date=file.modified_date,
            )
            for file in group.files
        ]
        await update_metadata(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(files=masked_files),
            organization_id=group.organization_id,
        )


@validate_fields_deco(["description"])
@validate_length_deco("description", max_length=200)
@validate_file_name_deco("file_name")
def validate_file_data(
    *,
    description: str,
    file_name: str,
    email: str,
    modified_date: datetime,
) -> GroupFile:
    return GroupFile(
        description=description,
        file_name=file_name,
        modified_by=email,
        modified_date=modified_date,
    )


@validate_file_exists_deco("file_name", "group_files")
def assign_files_to_update(
    *,
    file_name: str,
    group_files: list[GroupFile],
) -> list[GroupFile]:
    if file_name and not group_files:
        files_to_update: list[GroupFile] = []
        return files_to_update
    return group_files


async def add_file(
    *,
    loaders: Dataloaders,
    description: str,
    email: str,
    file_name: str,
    group_name: str,
) -> None:
    group = await get_group(loaders, group_name)
    modified_date = datetime_utils.get_utc_now()
    group_file_to_add = validate_file_data(
        description=description,
        file_name=file_name,
        email=email,
        modified_date=modified_date,
    )
    files_to_update = assign_files_to_update(
        file_name=file_name,
        group_files=group.files,
    )
    if group.files:
        await send_mail_file_report(
            loaders=loaders,
            group_name=group_name,
            responsible=email,
            file_name=file_name,
            file_description=description,
            is_added=True,
            modified_date=modified_date.date(),
        )
    files_to_update.append(group_file_to_add)
    await update_metadata(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=files_to_update,
        ),
        organization_id=group.organization_id,
    )


async def remove_file(
    *,
    loaders: Dataloaders,
    email: str,
    file_name: str,
    group_name: str,
) -> None:
    group = await get_group(loaders, group_name)
    if not group.files:
        raise ErrorUpdatingGroup.new()

    file_to_remove: GroupFile | None = next(
        (file for file in group.files if file.file_name == file_name), None
    )
    if not file_to_remove:
        raise ErrorUpdatingGroup.new()

    file_url = f"{group_name}/{file_name}"
    await resources_domain.remove_file(file_url)
    await update_metadata(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=[
                file
                for file in group.files
                if file.file_name != file_to_remove.file_name
            ]
        ),
        organization_id=group.organization_id,
    )
    uploaded_date = (
        file_to_remove.modified_date.date()
        if file_to_remove.modified_date
        else None
    )
    await send_mail_file_report(
        loaders=loaders,
        group_name=group_name,
        responsible=email,
        file_name=file_name,
        file_description=file_to_remove.description,
        modified_date=datetime_utils.get_utc_now().date(),
        uploaded_date=uploaded_date,
    )


async def send_mail_file_report(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    file_name: str,
    file_description: str,
    is_added: bool = False,
    modified_date: date,
    uploaded_date: date | None = None,
) -> None:
    stakeholders_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="file_report",
    )

    await groups_mail.send_mail_file_report(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        is_added=is_added,
        file_name=file_name,
        file_description=file_description,
        report_date=modified_date,
        email_to=stakeholders_email,
        uploaded_date=uploaded_date,
    )


async def remove_all_stakeholders(
    *,
    loaders: Dataloaders,
    group_name: str,
    modified_by: str,
    send_reassignment_email: bool = False,
) -> None:
    """Revoke stakeholders access to group."""
    stakeholders_access = await loaders.group_stakeholders_access.load(
        group_name
    )
    await collect(
        tuple(
            remove_stakeholder(
                loaders=loaders,
                email_to_revoke=access.email,
                group_name=group_name,
                modified_by=modified_by,
                send_reassignment_email=send_reassignment_email,
            )
            for access in stakeholders_access
        ),
        workers=1,
    )


async def _remove_all_roots(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> None:
    await collect(
        tuple(
            roots_domain.remove_root(
                email=email,
                group_name=group_name,
                reason="GROUP_DELETED",
                root=root,
            )
            for root in await loaders.group_roots.load(group_name)
        ),
        workers=1,
    )


async def _remove_all_toe(
    *,
    group_name: str,
) -> None:
    await toe_inputs_model.remove_group_toe_inputs(group_name=group_name)
    await toe_lines_model.remove_group_toe_lines(group_name=group_name)
    await toe_ports_model.remove_group_toe_ports(group_name=group_name)
    LOGGER.info(
        "Group's toe removed",
        extra={"extra": {"group_name": group_name}},
    )


async def _remove_all_batch_actions(
    group_name: str,
    validate_pending_actions: bool,
) -> None:
    group_actions: list[BatchProcessing] = [
        action
        for action in await batch_dal.get_actions()
        if action.entity == group_name
        and action.action_name != Action.REMOVE_GROUP_RESOURCES
    ]
    if validate_pending_actions:
        cancelable_actions = {
            Action.CLONE_ROOTS,
            Action.EXECUTE_MACHINE,
            Action.REBASE,
            Action.REFRESH_TOE_INPUTS,
            Action.REFRESH_TOE_LINES,
            Action.REFRESH_TOE_PORTS,
        }
        pending_actions = [
            action
            for action in group_actions
            if action.action_name not in cancelable_actions
            and action.batch_job_id
        ]
        if pending_actions:
            raise GroupHasPendingActions(
                action_names=[action.action_name for action in pending_actions]
            )

    await collect(
        [
            batch_dal.delete_action(dynamodb_pk=action.key)
            for action in group_actions
        ]
    )
    await collect(
        [
            batch_dal.cancel_batch_job(
                job_id=action.batch_job_id,
                reason="GROUP_REMOVAL",
            )
            for action in group_actions
            if action.batch_job_id
        ]
    )
    LOGGER.info(
        "Group's batch actions removed",
        extra={
            "extra": {
                "group_name": group_name,
                "actions": [action.action_name for action in group_actions],
            }
        },
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=3,
    sleep_seconds=10,
)
async def remove_resources(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    validate_pending_actions: bool = False,
) -> None:
    loaders.group.clear(group_name)
    group = await get_group(loaders, group_name)
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    await remove_all_stakeholders(
        loaders=loaders,
        group_name=group_name,
        modified_by=email,
        send_reassignment_email=validate_pending_actions,
    )
    await _remove_all_batch_actions(
        group_name=group_name,
        validate_pending_actions=validate_pending_actions,
    )
    all_findings = await loaders.group_findings.load(group_name)
    await collect(
        tuple(
            findings_domain.mask_finding(loaders, finding, email)
            for finding in all_findings
        ),
        workers=4,
    )
    group_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    await collect(
        tuple(
            events_domain.remove_event(event.id, group_name)
            for event in group_events
        ),
        workers=4,
    )
    await group_comments_domain.remove_comments(group_name)
    await mask_files(loaders, group_name)
    await _remove_all_roots(
        loaders=loaders,
        email=email,
        group_name=group_name,
    )
    await _remove_all_toe(group_name=group_name)
    await forces_model.remove_group_forces_executions(group_name=group_name)
    await groups_model.remove(group_name=group_name)

    reason = (
        group.state.justification
        if group.state.justification
        else GroupStateJustification.OTHER
    )
    comments = group.state.comments or "No comment."
    await notifications_domain.delete_group(
        loaders=loaders,
        deletion_date=datetime_utils.get_utc_now(),
        group=group,
        requester_email=email,
        reason=reason.value,
        comments=comments,
        attempt=False,
    )
    LOGGER.info(
        "Remove group resources completed",
        extra={
            "extra": {
                "group_name": group.name,
                "organization_id": organization.id,
                "organization_name": organization.name,
            }
        },
    )


async def remove_stakeholder(
    *,
    loaders: Dataloaders,
    email_to_revoke: str,
    group_name: str,
    modified_by: str,
    send_reassignment_email: bool = False,
) -> None:
    """Revoke stakeholder access to group.
    If the stakeholder has no access to other active groups in the
    organization, revoke access to organization.
    If no active groups are left for the stakeholder at this point, remove
    the stakeholder completely.
    """
    await group_access_domain.remove_access(
        loaders, email_to_revoke, group_name
    )

    loaders = get_new_context()
    group = await get_group(loaders, group_name)
    organization_id = group.organization_id
    has_org_access = await org_access.has_access(
        loaders, organization_id, email_to_revoke
    )
    stakeholder_org_groups_names = await get_groups_by_stakeholder(
        loaders, email_to_revoke, organization_id=organization_id
    )
    stakeholder_org_groups = await collect(
        [
            get_group(loaders, stakeholder_org_group_name)
            for stakeholder_org_group_name in stakeholder_org_groups_names
        ]
    )
    has_groups_in_org = bool(
        groups_utils.filter_active_groups(stakeholder_org_groups)
    )
    if has_org_access and not has_groups_in_org:
        await orgs_domain.remove_access(
            organization_id=organization_id,
            email=email_to_revoke,
            modified_by=modified_by,
            send_reassignment_email=send_reassignment_email,
        )

    LOGGER.info(
        "Stakeholder removed from group",
        extra={
            "extra": {
                "email": email_to_revoke,
                "group_name": group_name,
                "modified_by": modified_by,
            }
        },
    )

    loaders = get_new_context()
    stakeholder_groups_names = await get_groups_by_stakeholder(
        loaders, email_to_revoke
    )
    all_groups_by_stakeholder = await collect(
        [
            get_group(loaders, stakeholder_group_name)
            for stakeholder_group_name in stakeholder_groups_names
        ]
    )
    all_active_groups_by_stakeholder = groups_utils.filter_active_groups(
        all_groups_by_stakeholder
    )
    has_groups_in_asm = bool(all_active_groups_by_stakeholder)
    if not has_groups_in_asm:
        await stakeholders_domain.remove(email_to_revoke)


async def unsubscribe_from_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
) -> None:
    await remove_stakeholder(
        loaders=loaders,
        email_to_revoke=email,
        group_name=group_name,
        modified_by=email,
        send_reassignment_email=True,
    )
    await send_mail_unsubscribed(
        loaders=loaders,
        group_name=group_name,
        email=email,
    )


async def send_mail_unsubscribed(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> None:
    report_date = datetime_utils.get_utc_now()
    stakeholders_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="user_unsubscribed",
    )

    await groups_mail.send_mail_stakeholder_unsubscribed(
        loaders=loaders,
        email=email,
        email_to=stakeholders_email,
        group_name=group_name,
        report_date=report_date.date(),
    )


@validate_length_deco("business_id", max_length=60)
@validate_length_deco("business_name", max_length=60)
@validate_fields_deco(["business_name"])
@validate_length_deco("description", max_length=200)
@validate_fields_deco(["description"])
@validate_group_language_deco("language")
@validate_int_range_deco(
    "sprint_duration", lower_bound=1, upper_bound=10, inclusive=True
)
def assign_metadata(
    *,
    business_id: str | None,
    business_name: str | None,
    description: str,
    language: str,
    sprint_start_date: datetime,
    sprint_duration: int | None,
    tzn: Any | None,
) -> GroupMetadataToUpdate:
    return GroupMetadataToUpdate(
        business_id=business_id,
        business_name=business_name,
        description=description,
        language=GroupLanguage[language.upper()],
        sprint_duration=sprint_duration if sprint_duration else None,
        sprint_start_date=get_min_iso_date(sprint_start_date.astimezone(tzn))
        if sprint_start_date
        else None,
    )


@validate_length_deco("metadata.context", max_length=20000)
@validate_length_deco("metadata.disambiguation", max_length=10000)
async def update_metadata(
    *,
    group_name: str,
    metadata: GroupMetadataToUpdate,
    organization_id: str,
) -> None:
    await groups_model.update_metadata(
        group_name=group_name,
        metadata=metadata,
        organization_id=organization_id,
    )


async def update_group_info(
    *,
    loaders: Dataloaders,
    group_name: str,
    metadata: GroupMetadataToUpdate,
    email: str,
) -> None:
    group = await get_group(loaders, group_name)

    stakeholders_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="updated_group_info",
    )

    await update_metadata(
        group_name=group_name,
        metadata=metadata,
        organization_id=group.organization_id,
    )

    if metadata:
        await groups_mail.send_mail_updated_group_information(
            loaders=loaders,
            group_name=group_name,
            responsible=email,
            group=group,
            metadata=metadata,
            report_date=datetime_utils.get_utc_now(),
            email_to=stakeholders_email,
        )


async def update_forces_access_token(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
    expiration_time: int,
    responsible: str,
) -> str:
    group = await get_group(loaders, group_name)
    had_token: bool = bool(group.agent_token)

    result = await stakeholders_domain.update_access_token(
        email=email,
        expiration_time=expiration_time,
        loaders=loaders,
        name="Forces Token",
    )
    await send_mail_devsecops_agent(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )

    return result


async def send_mail_devsecops_agent(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    report_date = datetime_utils.get_utc_now()
    stakeholders_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="devsecops_agent",
    )

    await groups_mail.send_mail_devsecops_agent_token(
        loaders=loaders,
        email=responsible,
        email_to=stakeholders_email,
        group_name=group_name,
        had_token=had_token,
        report_date=report_date.date(),
    )


async def update_state(
    *,
    group_name: str,
    state: GroupState,
    organization_id: str,
) -> None:
    await groups_model.update_state(
        group_name=group_name, state=state, organization_id=organization_id
    )


async def update_indicators(
    *,
    group_name: str,
    indicators: GroupUnreliableIndicators,
) -> None:
    await groups_model.update_unreliable_indicators(
        group_name=group_name, indicators=indicators
    )


async def set_pending_deletion_date(
    group: Group,
    modified_by: str,
    pending_deletion_date: datetime,
) -> None:
    """Update pending deletion date in group's state."""
    await update_state(
        group_name=group.name,
        organization_id=group.organization_id,
        state=group.state._replace(
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            pending_deletion_date=pending_deletion_date,
        ),
    )


async def remove_pending_deletion_date(
    group: Group,
    modified_by: str,
) -> None:
    """Clear pending deletion date in group's state."""
    await update_state(
        group_name=group.name,
        organization_id=group.organization_id,
        state=group.state._replace(
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            pending_deletion_date=None,
        ),
    )


async def update_group_tags(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
    updated_tags: set[str],
) -> None:
    group = await get_group(loaders, group_name)

    if updated_tags != group.state.tags:
        await update_state(
            group_name=group_name,
            organization_id=group.organization_id,
            state=GroupState(
                comments=group.state.comments,
                modified_date=datetime_utils.get_utc_now(),
                has_machine=group.state.has_machine,
                has_squad=group.state.has_squad,
                managed=group.state.managed,
                payment_id=group.state.payment_id,
                justification=GroupStateJustification.NONE,
                modified_by=email,
                service=group.state.service,
                status=GroupStateStatus.ACTIVE,
                tags=updated_tags,
                tier=group.state.tier,
                type=group.state.type,
            ),
        )


async def add_tags(
    *,
    loaders: Dataloaders,
    email: str,
    group: Group,
    tags_to_add: set[str],
) -> None:
    updated_tags = (
        group.state.tags.union(tags_to_add)
        if group.state.tags
        else tags_to_add
    )
    await update_group_tags(
        loaders=loaders,
        group_name=group.name,
        email=email,
        updated_tags=updated_tags,
    )
    schedule(
        send_mail_portfolio_report(
            loaders=loaders,
            group_name=group.name,
            responsible=email,
            portfolio=", ".join(tags_to_add),
            is_added=True,
            modified_date=datetime_utils.get_utc_now(),
        )
    )


async def remove_tag(
    *,
    loaders: Dataloaders,
    email: str,
    group: Group,
    tag_to_remove: str,
) -> None:
    if group.state.tags:
        updated_tags: set[str] = {
            tag for tag in group.state.tags if tag != tag_to_remove
        }
        await update_group_tags(
            loaders=loaders,
            group_name=group.name,
            email=email,
            updated_tags=updated_tags,
        )
        schedule(
            send_mail_portfolio_report(
                loaders=loaders,
                group_name=group.name,
                responsible=email,
                portfolio=tag_to_remove,
                modified_date=datetime_utils.get_utc_now(),
            )
        )


async def send_mail_portfolio_report(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    portfolio: str,
    is_added: bool = False,
    modified_date: datetime,
) -> None:
    stakeholders_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="portfolio_report",
    )

    await groups_mail.send_mail_portfolio_report(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        is_added=is_added,
        portfolio=portfolio,
        report_date=modified_date.date(),
        email_to=stakeholders_email,
    )


def validate_group_services_config(
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
) -> None:
    if has_squad:
        if not has_arm:
            raise InvalidGroupServicesConfig(
                "Squad is only available when ASM is too"
            )
        if not has_machine:
            raise InvalidGroupServicesConfig(
                "Squad is only available when Machine is too"
            )


async def validate_group_tags(
    loaders: Dataloaders, group_name: str, tags: list[str]
) -> list[str]:
    """Validate tags array."""
    pattern = re.compile("^[a-z0-9]+(?:-[a-z0-9]+)*$")
    if await _has_repeated_tags(loaders, group_name, tags):
        raise RepeatedValues()
    return [tag for tag in tags if pattern.match(tag)]


async def request_upgrade(
    *,
    loaders: Dataloaders,
    email: str,
    group_names: list[str],
) -> None:
    """
    Lead the stakeholder towards a subscription upgrade managed by our team.
    This is meant to be a temporary flow while the billing module gets ready.
    """
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    if not all(
        enforcer(group_name, "request_group_upgrade")
        for group_name in group_names
    ):
        raise GroupNotFound()

    groups = await collect(
        [get_group(loaders, group_name) for group_name in group_names]
    )
    if any(group.state.has_squad for group in groups):
        raise BillingSubscriptionSameActive()

    await notifications_domain.request_groups_upgrade(loaders, email, groups)


async def get_treatment_summary(
    loaders: Dataloaders,
    group_name: str,
) -> GroupTreatmentSummary:
    """Get the total vulnerability treatment."""
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    non_deleted_findings = tuple(
        finding
        for finding in findings
        if not findings_utils.is_deleted(finding)
    )
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in non_deleted_findings]
        )
    )
    treatment_counter = Counter(
        vuln.treatment.status
        for vuln in vulns
        if vuln.treatment
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    return GroupTreatmentSummary(
        accepted=treatment_counter[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment_counter[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        in_progress=treatment_counter[
            VulnerabilityTreatmentStatus.IN_PROGRESS
        ],
        untreated=treatment_counter[VulnerabilityTreatmentStatus.UNTREATED],
    )


async def get_oldest_finding_date(
    loaders: Dataloaders, group_name: str
) -> datetime | None:
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    findings_indicators = [
        finding.unreliable_indicators for finding in findings
    ]
    ages: list[datetime] = [
        finding_indicators.oldest_vulnerability_report_date
        for finding_indicators in findings_indicators
        if finding_indicators.oldest_vulnerability_report_date
    ]
    if ages:
        return min(ages)
    return None


async def update_policies(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    organization_id: str,
    policies_to_update: PoliciesToUpdate,
) -> None:
    validated_policies: dict[str, Any] = {}
    for attr, value in policies_to_update._asdict().items():
        if value is not None:
            value = (
                Decimal(value).quantize(Decimal("0.1"))
                if isinstance(value, float)
                else Decimal(value)
            )
            validated_policies[attr] = value
            validator_func = getattr(orgs_domain, f"validate_{attr}")
            validator_func(value)
    await validate_acceptance_severity_range(
        group_name=group_name, loaders=loaders, values=policies_to_update
    )

    if validated_policies:
        today = datetime_utils.get_utc_now()
        await groups_model.update_policies(
            group_name=group_name,
            modified_by=email,
            modified_date=today,
            organization_id=organization_id,
            policies=policies_to_update,
        )
        schedule(
            send_mail_policies(
                group_name=group_name,
                loaders=loaders,
                modified_date=today,
                new_policies=policies_to_update._asdict(),
                responsible=email,
            )
        )


async def validate_acceptance_severity_range(
    *, group_name: str, loaders: Dataloaders, values: PoliciesToUpdate
) -> bool:
    success: bool = True
    min_acceptance_severity = await get_policy_min_acceptance_severity(
        loaders=loaders, group_name=group_name
    )
    max_acceptance_severity = await get_policy_max_acceptance_severity(
        loaders=loaders, group_name=group_name
    )
    min_value = (
        values.min_acceptance_severity
        if values.min_acceptance_severity is not None
        else min_acceptance_severity
    )
    max_value = (
        values.max_acceptance_severity
        if values.max_acceptance_severity is not None
        else max_acceptance_severity
    )
    if (
        min_value is not None
        and max_value is not None
        and (min_value > max_value)
    ):
        raise InvalidAcceptanceSeverityRange()
    return success


async def send_mail_policies(
    *,
    group_name: str,
    loaders: Dataloaders,
    modified_date: datetime,
    new_policies: dict[str, Any],
    responsible: str,
) -> None:
    group_data = await get_group(loaders, group_name)
    organization_data = await orgs_utils.get_organization(
        loaders, group_data.organization_id
    )

    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = (
            group_data.policies._asdict().get(key)
            if group_data.policies
            else organization_data.policies._asdict().get(key)
        )
        if val is not None and val != old_value:
            policies_content[POLICIES_FORMATTED[key]] = {
                "from": old_value,
                "to": val,
            }

    email_context: dict[str, Any] = {
        "entity_name": group_name,
        "entity_type": "group",
        "policies_link": (
            f"{BASE_URL}/orgs/{organization_data.name}"
            f"/groups/{group_name}/scope"
        ),
        "policies_content": policies_content,
        "responsible": responsible,
        "date": datetime_utils.get_as_str(modified_date),
    }
    group_stakeholders = await group_access_domain.get_group_stakeholders(
        loaders, group_name
    )

    stakeholders_emails = [
        stakeholder.email
        for stakeholder in group_stakeholders
        if await group_access_domain.get_stakeholder_role(
            loaders, stakeholder.email, group_name, stakeholder.is_registered
        )
        in ["customer_manager", "user_manager"]
    ]

    if policies_content:
        await groups_mail.send_mail_updated_policies(
            loaders=loaders,
            email_to=stakeholders_emails,
            context=email_context,
        )
