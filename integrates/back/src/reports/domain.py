from .report_types import (
    certificate as cert_report,
    data as data_report,
    technical as technical_report,
    unfulfilled_standards as unfulfilled_standards_report,
)
from aioextensions import (
    collect,
)
from custom_utils.findings import (
    get_group_findings,
)
from custom_utils.reports import (
    sign_url,
    upload_report,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from operator import (
    itemgetter,
)
from reports.enums import (
    ReportType,
)
from reports.report_types.toe_lines import (
    get_group_toe_lines_report,
)


async def get_group_report_url(  # pylint: disable=too-many-locals
    *,  # NOSONAR
    report_type: ReportType,
    group_name: str,
    user_email: str,
    treatments: set[VulnerabilityTreatmentStatus],
    states: set[VulnerabilityStateStatus],
    verifications: set[VulnerabilityVerificationStatus],
    closing_date: datetime | None,
    finding_title: str,
    age: int | None,
    min_severity: Decimal | None,
    max_severity: Decimal | None,
    last_report: int | None,
    min_release_date: datetime | None,
    max_release_date: datetime | None,
    location: str,
) -> str | None:
    loaders: Dataloaders = get_new_context()
    group_findings = await get_group_findings(
        group_name=group_name, loaders=loaders
    )
    group_findings_score = await collect(
        findings_domain.get_max_open_severity_score(loaders, finding.id)
        for finding in group_findings
    )
    findings_ord = tuple(
        finding
        for finding, _ in sorted(
            zip(group_findings, group_findings_score),
            key=itemgetter(1),
            reverse=True,
        )
    )

    if report_type == ReportType.XLS:
        return await technical_report.generate_xls_file(
            loaders=loaders,
            findings=findings_ord,
            group_name=group_name,
            treatments=treatments,
            states=states,
            verifications=verifications,
            closing_date=closing_date,
            finding_title=finding_title,
            age=age,
            min_severity=min_severity,
            max_severity=max_severity,
            last_report=last_report,
            min_release_date=min_release_date,
            max_release_date=max_release_date,
            location=location,
        )

    if not (group := await loaders.group.load(group_name)):
        return None

    if report_type == ReportType.PDF:
        return await technical_report.generate_pdf_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang=str(group.language.value).lower(),
            user_email=user_email,
        )
    if report_type == ReportType.CERT:
        return await cert_report.generate_cert_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang=str(group.language.value).lower(),
            user_email=user_email,
        )
    if report_type == ReportType.DATA:
        return await data_report.generate(
            loaders=loaders,
            findings_ord=findings_ord,
            group_name=group_name,
            group_description=group.description,
            requester_email=user_email,
        )

    return None


async def get_signed_unfulfilled_standard_report_url(
    loaders: Dataloaders,
    group_name: str,
    stakeholder_email: str,
    seconds: float = 300,
    unfulfilled_standards: set[str] | None = None,
) -> str:
    filename = await unfulfilled_standards_report.generate_pdf_file(
        loaders=loaders,
        group_name=group_name,
        stakeholder_email=stakeholder_email,
        unfulfilled_standards=unfulfilled_standards,
    )
    filename_to_store = await upload_report(filename)
    return await sign_url(filename_to_store, seconds=seconds)


async def get_toe_lines_report(
    *,
    group_name: str,
    email: str,
) -> str:
    loaders: Dataloaders = get_new_context()

    return await get_group_toe_lines_report(
        loaders=loaders,
        group_name=group_name,
        email=email,
    )
