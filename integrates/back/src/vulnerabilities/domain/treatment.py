from aioextensions import (
    collect,
    schedule,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidNotificationRequest,
    InvalidVulnsNumber,
    SameValues,
    VulnNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    validations_deco,
    vulnerabilities as vulns_utils,
)
from custom_utils.findings import (
    is_finding_released,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model import (
    utils as db_model_utils,
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Notification,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    RootRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from group_access import (
    domain as group_access_domain,
)
from itertools import (
    islice,
)
from mailer import (
    utils as mailer_utils,
    vulnerabilities as vulns_mailer,
)
from stakeholders.domain import (
    get_stakeholder,
)
from vulnerabilities.domain.core import (
    get_updated_manager_mail_content,
    get_vulnerability,
    group_vulnerabilities,
    should_send_update_treatment,
)
from vulnerabilities.domain.utils import (
    format_vulnerability_locations,
    get_finding,
    get_valid_assigned,
    validate_acceptance,
)
from vulnerabilities.domain.validations import (
    validate_accepted_treatment_change,
)
from vulnerabilities.types import (
    VulnerabilityTreatmentToUpdate,
)


async def add_vulnerability_treatment(
    *,
    modified_by: str,
    vulnerability: Vulnerability,
    treatment: VulnerabilityTreatmentToUpdate,
) -> None:
    await vulns_model.update_treatment(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        treatment=VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED
            if treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
            else None,
            accepted_until=treatment.accepted_until,
            justification=treatment.justification,
            assigned=treatment.assigned or modified_by,
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            status=treatment.status,
        ),
    )


async def add_vulnerability_treatment_new(
    *,
    modified_by: str,
    vulnerability: Vulnerability,
    treatment: VulnerabilityTreatmentToUpdate,
) -> None:
    await vulns_model.update_treatment(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        treatment=VulnerabilityTreatment(
            acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED
            if treatment.status
            in (
                VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                VulnerabilityTreatmentStatus.ACCEPTED,
            )
            else None,
            accepted_until=treatment.accepted_until,
            justification=treatment.justification,
            assigned=treatment.assigned or modified_by,
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            status=treatment.status,
        ),
    )


def get_treatment_change(
    vulnerability: Vulnerability, min_date: datetime
) -> tuple[str, Vulnerability] | None:
    if vulnerability.treatment is not None:
        last_treatment_date = vulnerability.treatment.modified_date
        if last_treatment_date > min_date:
            treatment = str(vulnerability.treatment.status.value)
            status = (
                f"_{vulnerability.treatment.acceptance_status.value}"
                if vulnerability.treatment.acceptance_status is not None
                else ""
            )
            return treatment + status, vulnerability
        return None
    return None


async def get_treatment_changes(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> int:
    historic = await loaders.vulnerability_historic_treatment.load(vuln.id)
    if historic:
        first_treatment = historic[0]
        return (
            len(historic) - 1
            if first_treatment.status == VulnerabilityTreatmentStatus.UNTREATED
            else len(historic)
        )
    return 0


async def _handle_vulnerability_acceptance(
    *,
    loaders: Dataloaders,
    finding_id: str,
    new_treatment: VulnerabilityTreatment,
    vulnerability: Vulnerability,
) -> None:
    treatments_to_add: tuple[VulnerabilityTreatment, ...] = tuple()
    if (
        new_treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
        and vulnerability.treatment
        and vulnerability.treatment.assigned
    ):
        treatments_to_add = (
            new_treatment._replace(assigned=vulnerability.treatment.assigned),
        )
    elif (
        new_treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.REJECTED
    ):
        # Restore previous treatment as request was REJECTED
        treatment_loader = loaders.vulnerability_historic_treatment
        historic_treatment = await treatment_loader.load(vulnerability.id)
        if len(historic_treatment) > 1:
            treatments_to_add = (
                new_treatment,
                historic_treatment[-2]._replace(
                    modified_date=new_treatment.modified_date,
                ),
            )
        else:
            treatments_to_add = (
                new_treatment,
                VulnerabilityTreatment(
                    modified_date=new_treatment.modified_date,
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    modified_by=new_treatment.modified_by,
                ),
            )

    current_value = vulnerability
    treatments_to_add = db_model_utils.adjust_historic_dates(treatments_to_add)
    if len(treatments_to_add) == 1:
        await vulns_model.update_treatment(
            current_value=current_value,
            finding_id=finding_id,
            vulnerability_id=vulnerability.id,
            treatment=treatments_to_add[0],
        )
        return
    if len(treatments_to_add) == 2:
        await collect(
            (
                vulns_model.update_treatment(
                    current_value=current_value,
                    finding_id=finding_id,
                    vulnerability_id=vulnerability.id,
                    treatment=treatments_to_add[-1],
                ),
                vulns_model.add_historic_entry(
                    entry=treatments_to_add[0],
                    vulnerability_id=current_value.id,
                ),
            )
        )
        return
    # Use for-await as update order is relevant for typed vuln
    for treatment in treatments_to_add:
        if isinstance(treatment, VulnerabilityTreatment):
            await vulns_model.update_treatment(
                current_value=current_value,
                finding_id=finding_id,
                vulnerability_id=vulnerability.id,
                treatment=treatment,
            )
            current_value = current_value._replace(treatment=treatment)


@validations_deco.validate_length_deco("justification", max_length=10000)
@validations_deco.validate_fields_deco(["justification"])
async def handle_vulnerabilities_acceptance(
    *,
    loaders: Dataloaders,
    accepted_vulns: list[str],
    finding_id: str,
    justification: str,
    rejected_vulns: list[str],
    user_email: str,
) -> None:
    today = datetime_utils.get_utc_now()

    all_vulns = accepted_vulns + rejected_vulns
    max_number_of_vulns = 32
    if len(all_vulns) > max_number_of_vulns:
        raise InvalidVulnsNumber(number_of_vulns=max_number_of_vulns)

    all_vulnerabilities = await loaders.vulnerability.load_many(all_vulns)
    vulnerabilities: list[Vulnerability] = [
        vulnerability
        for vulnerability in all_vulnerabilities
        if vulnerability is not None
    ]
    if len(all_vulnerabilities) != len(vulnerabilities):
        raise VulnNotFound()
    if any(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.finding_id != finding_id
    ):
        raise VulnNotFound()
    for vuln in vulnerabilities:
        validate_acceptance(vuln)

    rejected_treatment = VulnerabilityTreatment(
        acceptance_status=VulnerabilityAcceptanceStatus.REJECTED,
        justification=justification,
        modified_date=today,
        modified_by=user_email,
        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    )
    approved_treatment = VulnerabilityTreatment(
        acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
        justification=justification,
        modified_date=today,
        modified_by=user_email,
        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
    )
    await collect(
        tuple(
            _handle_vulnerability_acceptance(
                loaders=loaders,
                finding_id=finding_id,
                new_treatment=approved_treatment
                if vuln.id in accepted_vulns
                else rejected_treatment,
                vulnerability=vuln,
            )
            for vuln in vulnerabilities
        ),
        workers=32,
    )


async def send_treatment_change_mail(
    *,
    loaders: Dataloaders,
    assigned: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str,
    min_date: datetime,
    modified_by: str,
) -> bool:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    changes = list(
        filter(None, [get_treatment_change(vuln, min_date) for vuln in vulns])
    )
    treatments = {change[0] for change in changes}
    for treatment in treatments:
        treatments_change = [
            change for change in changes if change[0] == treatment
        ]
        updated_vulns = [change[1] for change in treatments_change]
        if treatment == "ACCEPTED_UNDEFINED_APPROVED":
            await send_treatment_report_mail(
                loaders=loaders,
                modified_by=modified_by,
                finding_id=finding_id,
                justification=(
                    updated_vulns[0].treatment.justification
                    if updated_vulns and updated_vulns[0].treatment is not None
                    else ""
                ),
                updated_vulns=updated_vulns,
                is_approved=True,
            )
            continue
        if treatment == "ACCEPTED_UNDEFINED_SUBMITTED":
            await send_treatment_report_mail(
                loaders=loaders,
                modified_by=modified_by,
                finding_id=finding_id,
                justification=(
                    updated_vulns[0].treatment.justification
                    if updated_vulns and updated_vulns[0].treatment is not None
                    else ""
                ),
                updated_vulns=updated_vulns,
                is_approved=False,
            )
            continue

        await should_send_update_treatment(
            loaders=loaders,
            assigned=assigned,
            finding_id=finding_id,
            finding_title=finding_title,
            group_name=group_name,
            justification=justification,
            treatment=treatment,
            updated_vulns=updated_vulns,
            modified_by=modified_by,
        )

    return bool(treatments)


async def send_treatment_report_mail(
    *,
    loaders: Dataloaders,
    modified_by: str | None,
    justification: str | None,
    finding_id: str,
    updated_vulns: Iterable[Vulnerability],
    is_approved: bool = False,
) -> None:
    finding = await get_finding(loaders, finding_id)
    vulns_grouped = group_vulnerabilities(updated_vulns)
    vulns_roots = await loaders.root.load_many(
        [
            RootRequest(
                group_name=finding.group_name, root_id=vuln.root_id or ""
            )
            for vuln in vulns_grouped
        ]
    )
    vulns_data = vulns_utils.format_vulnerabilities(vulns_grouped, vulns_roots)
    mail_content = get_updated_manager_mail_content(vulns_data)
    users_email, managers_email = await collect(
        (
            mailer_utils.get_group_emails_by_notification(
                loaders=loaders,
                group_name=finding.group_name,
                notification="treatment_report",
            ),
            get_managers_by_size(loaders, finding.group_name, 3),
        )
    )
    schedule(
        vulns_mailer.send_mail_treatment_report(
            loaders=loaders,
            finding_id=finding_id,
            finding_title=finding.title,
            group_name=finding.group_name,
            justification=justification,
            managers_email=managers_email,
            modified_by=modified_by,
            modified_date=datetime_utils.get_utc_now(),
            location=mail_content,
            email_to=users_email,
            is_approved=is_approved,
        )
    )


async def get_managers_by_size(
    loaders: Dataloaders, group_name: str, list_size: int
) -> list[str]:
    """Returns a list of managers with an specific length for the array"""
    managers = list(
        islice(
            await group_access_domain.get_managers(loaders, group_name),
            list_size,
        )
    )
    return managers


def is_value_the_same(
    *,
    vulnerability: Vulnerability,
    treatment: VulnerabilityTreatmentToUpdate,
    valid_assigned: str,
) -> bool:
    if (
        vulnerability.treatment
        and vulnerability.treatment.status == treatment.status
        and vulnerability.treatment.justification == treatment.justification
        and vulnerability.treatment.assigned == valid_assigned
        and vulnerability.treatment.accepted_until == treatment.accepted_until
    ):
        return True

    if (
        vulnerability.treatment
        and treatment.status == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vulnerability.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
    ):
        return True

    return False


@validations_deco.validate_fields_deco(
    ["treatment.justification", "treatment.assigned"]
)
@validations_deco.validate_length_deco(
    "treatment.justification", max_length=10000
)
async def update_vulnerabilities_treatment(
    *,
    loaders: Dataloaders,
    finding: Finding,
    finding_severity: Decimal,
    modified_by: str,
    vulnerability_id: str,
    treatment: VulnerabilityTreatmentToUpdate,
) -> None:
    vulnerability = await get_vulnerability(loaders, vulnerability_id)
    vulns_utils.validate_closed(vulnerability)
    vulns_utils.validate_released(vulnerability)
    if vulnerability.finding_id != finding.id:
        raise VulnNotFound()
    valid_assigned = await get_valid_assigned(
        loaders=loaders,
        assigned=treatment.assigned or modified_by,
        email=modified_by,
        group_name=finding.group_name,
    )
    if is_value_the_same(
        vulnerability=vulnerability,
        treatment=treatment,
        valid_assigned=valid_assigned,
    ):
        raise SameValues()

    if treatment.status == VulnerabilityTreatmentStatus.ACCEPTED:
        if not treatment.accepted_until:
            raise InvalidAcceptanceDays("Acceptance parameter missing")
        historic_treatment = (
            await loaders.vulnerability_historic_treatment.load(
                vulnerability.id
            )
        )
        await validate_accepted_treatment_change(
            loaders=loaders,
            accepted_until=treatment.accepted_until,
            finding_severity=finding_severity,
            group_name=finding.group_name,
            historic_treatment=historic_treatment,
        )

    await add_vulnerability_treatment(
        modified_by=modified_by,
        treatment=treatment._replace(assigned=valid_assigned),
        vulnerability=vulnerability,
    )


def are_all_approved(*, vulnerabilities: list[Vulnerability]) -> bool:
    return all(
        vuln.treatment
        and vuln.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
        for vuln in vulnerabilities
    )


async def validate_and_send_notification_request(
    loaders: Dataloaders,
    finding: Finding,
    responsible: str,
    vulnerabilities: list[str],
) -> None:
    # Validate finding with vulns in group
    finding_vulns: list[
        Vulnerability
    ] = await loaders.finding_vulnerabilities_all.load(finding.id)
    assigned_vulns: list[Vulnerability] = list(
        vuln
        for vuln in finding_vulns
        for vulnerability_id in vulnerabilities
        if vuln.id == vulnerability_id
    )
    if len(assigned_vulns) != len(vulnerabilities):
        raise InvalidNotificationRequest(
            "Some of the provided vulns ids don't match existing vulns"
        )
    assigned = ""
    # Validate assigned
    if assigned_vulns[0].treatment:
        assigned = str(assigned_vulns[0].treatment.assigned)
        justification = str(assigned_vulns[0].treatment.justification)
    if not assigned:
        raise InvalidNotificationRequest(
            "Some of the provided vulns don't have any assigned hackers"
        )
    # Validate recent changes in treatment
    for vuln in assigned_vulns:
        if vuln.treatment:
            if not (
                timedelta(minutes=10)
                > datetime_utils.get_utc_now() - vuln.treatment.modified_date
                and vuln.treatment.assigned == assigned
            ):
                raise InvalidNotificationRequest(
                    "Too much time has passed to notify some of these changes"
                )
            if vuln.treatment.assigned != assigned:
                raise InvalidNotificationRequest(
                    "Not all the vulns provided have the same assigned hacker"
                )
    where_str = format_vulnerability_locations(
        list(vuln.state.where for vuln in assigned_vulns)
    )

    stakeholder = await get_stakeholder(loaders, assigned)
    await send_treatment_change_mail(
        loaders=loaders,
        assigned=assigned,
        finding_id=finding.id,
        finding_title=finding.title,
        group_name=finding.group_name,
        justification=justification,
        min_date=datetime.now(timezone.utc) - timedelta(minutes=20),
        modified_by=responsible,
    )
    if (
        Notification.VULNERABILITY_ASSIGNED
        in stakeholder.state.notifications_preferences.email
        and not are_all_approved(vulnerabilities=assigned_vulns)
    ):
        await vulns_mailer.send_mail_assigned_vulnerability(
            loaders=loaders,
            email_to=[assigned],
            is_finding_released=is_finding_released(finding),
            group_name=finding.group_name,
            finding_id=finding.id,
            finding_title=finding.title,
            responsible=responsible,
            where=where_str,
        )
