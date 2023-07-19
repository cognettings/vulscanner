from batch.dal import (
    delete_action,
    is_action_by_key,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    UnavailabilityError,
)
from custom_utils.reports import (
    sign_url,
    upload_report,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
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
import json
import logging
import logging.config
from notifications import (
    domain as notifications_domain,
)
import os
from reports import (
    domain as reports_domain,
)
from reports.enums import (
    ReportType,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


upload_report_file = retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=4,
    sleep_seconds=1,
)(upload_report)


async def get_report(  # pylint: disable=too-many-locals
    *,  # NOSONAR
    item: BatchProcessing,
    report_type: ReportType,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
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
) -> str:
    report_file_name: str | None = None
    try:
        report_file_name = await reports_domain.get_group_report_url(
            report_type=report_type,
            group_name=item.entity,
            user_email=item.subject,
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
        if report_file_name is not None:
            uploaded_file_name = await upload_report_file(report_file_name)
    except ErrorUploadingFileS3 as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    group_name=item.entity,
                    user_email=item.subject,
                )
            ),
        )
        return ""
    else:
        return uploaded_file_name
    finally:
        if report_file_name and os.path.exists(report_file_name):
            os.unlink(report_file_name)


async def send_report(  # pylint: disable=too-many-locals
    *,  # NOSONAR
    item: BatchProcessing,
    report_type: ReportType,
    report_url: str,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
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
) -> None:
    loaders = get_new_context()
    translations: dict[ReportType, str] = {
        ReportType.CERT: "Certificate",
        ReportType.DATA: "Group Data",
        ReportType.PDF: "Executive",
        ReportType.XLS: "Technical",
    }
    is_in_db = await is_action_by_key(key=item.key)
    if is_in_db:
        message = (
            f"Send {report_type} report requested by "
            + f"{item.subject} for group {item.entity}"
            + get_filter_message(
                report_type=report_type,
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
        )
        LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]))
        await notifications_domain.new_password_protected_report(
            loaders=loaders,
            user_email=item.subject,
            group_name=item.entity,
            file_type=translations[report_type],
            file_link=await sign_url(report_url),
        )
        await delete_action(
            action_name=item.action_name,
            additional_info=item.additional_info,
            entity=item.entity,
            subject=item.subject,
            time=item.time,
        )


def _get_filter_message(value: object | None, text: str) -> str:
    if value is not None:
        return text

    return ""


def get_filter_message(
    *,
    report_type: ReportType,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
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
) -> str:
    if closing_date:
        states = set(
            [
                VulnerabilityStateStatus["SAFE"],
            ]
        )
        treatments = set(VulnerabilityTreatmentStatus)
        if verifications != set(
            [
                VulnerabilityVerificationStatus["VERIFIED"],
            ]
        ):
            verifications = set()

    message: str = ""
    if list(sorted(states)) != list(
        sorted(
            set(
                [
                    VulnerabilityStateStatus["SAFE"],
                    VulnerabilityStateStatus["VULNERABLE"],
                ]
            )
        )
    ):
        message += f" States: {states}."
    if sorted(list(treatments)) != sorted(
        list(set(VulnerabilityTreatmentStatus))
    ):
        message += f" Treatments: {treatments}."
    if verifications:
        message += f" Verifications: {verifications}."
    message += _get_filter_message(
        closing_date, f" Closing date: {closing_date}."
    )
    if finding_title:
        message += f" Finding type code: {finding_title}."
    if age is not None:
        message += f" Age in days: {age}."
    message += _get_filter_message(
        min_severity, f" Minimum CVSS 3.1 score: {min_severity}."
    )
    message += _get_filter_message(
        max_severity, f" Maximum CVSS 3.1 score: {max_severity}."
    )
    message += _get_filter_message(
        last_report, f" Last Report in days: {last_report}."
    )
    message += _get_filter_message(
        min_release_date, f" Minimum release date: {min_release_date}."
    )
    message += _get_filter_message(
        max_release_date, f" Maximum release date: {max_release_date}."
    )
    if location:
        message += f" Location: {location}."

    return (
        f". With the following filters:{message}"
        if report_type == ReportType.XLS and message
        else ""
    )


async def send_group_toe_lines_report(
    *,
    item: BatchProcessing,
    report_type: ReportType,
    report_url: str,
) -> None:
    loaders = get_new_context()
    translations: dict[ReportType, str] = {
        ReportType.TOE_LINES: "Group Toe Lines",
    }
    is_in_db = await is_action_by_key(key=item.key)
    if is_in_db:
        message = (
            f"Send {report_type} report requested by "
            f"{item.subject} for group {item.entity}"
        )
        LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]))
        await notifications_domain.new_password_protected_report(
            loaders=loaders,
            user_email=item.subject,
            group_name=item.entity,
            file_type=translations[report_type],
            file_link=await sign_url(report_url),
            include_report=False,
        )


async def _get_group_toe_lines_report(*, item: BatchProcessing) -> str:
    report_file_name: str | None = None
    try:
        report_file_name = await reports_domain.get_toe_lines_report(
            group_name=item.entity,
            email=item.subject,
        )
        if report_file_name is not None:
            uploaded_file_name = await upload_report_file(report_file_name)
    except ErrorUploadingFileS3 as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    group_name=item.entity,
                    user_email=item.subject,
                )
            ),
        )
        return ""
    else:
        return uploaded_file_name
    finally:
        if report_file_name and os.path.exists(report_file_name):
            os.unlink(report_file_name)


async def get_group_toe_lines_report(
    *,
    item: BatchProcessing,
    report_type: ReportType,
) -> None:
    LOGGER_TRANSACTIONAL.info(
        ":".join(
            [
                item.subject,
                f"Processing {report_type} report requested by "
                + f"{item.subject} for group {item.entity}",
            ]
        )
    )
    report_url = await _get_group_toe_lines_report(
        item=item,
    )
    if report_url:
        await send_group_toe_lines_report(
            item=item,
            report_type=report_type,
            report_url=report_url,
        )


async def report(  # pylint: disable=too-many-locals
    *, item: BatchProcessing
) -> None:
    additional_info: dict = json.loads(item.additional_info)
    report_type = ReportType[additional_info["report_type"]]
    if report_type == ReportType.TOE_LINES:
        return await get_group_toe_lines_report(
            item=item,
            report_type=report_type,
        )

    treatments = {
        VulnerabilityTreatmentStatus[treatment]
        for treatment in additional_info["treatments"]
    }
    states = {
        VulnerabilityStateStatus[state] for state in additional_info["states"]
    }
    verifications = {
        VulnerabilityVerificationStatus[verification]
        for verification in additional_info["verifications"]
    }
    closing_date: datetime | None = (
        datetime.fromisoformat(
            str(additional_info["closing_date"])
        ).astimezone(tz=timezone.utc)
        if additional_info["closing_date"]
        else None
    )
    finding_title: str = additional_info.get("finding_title", "")
    age: int | None = additional_info.get("age", None)
    min_severity: Decimal | None = (
        Decimal(additional_info["min_severity"]).quantize(Decimal("0.1"))
        if additional_info.get("min_severity", None) is not None
        else None
    )
    max_severity: Decimal | None = (
        Decimal(additional_info["max_severity"]).quantize(Decimal("0.1"))
        if additional_info.get("max_severity", None) is not None
        else None
    )
    last_report: int | None = additional_info.get("last_report", None)
    min_release_date: datetime | None = (
        datetime.fromisoformat(
            str(additional_info.get("min_release_date"))
        ).astimezone(tz=timezone.utc)
        if additional_info.get("min_release_date") is not None
        else None
    )
    max_release_date: datetime | None = (
        datetime.fromisoformat(
            str(additional_info["max_release_date"])
        ).astimezone(tz=timezone.utc)
        if additional_info.get("max_release_date") is not None
        else None
    )
    location: str = additional_info.get("location", "")

    LOGGER_TRANSACTIONAL.info(
        ":".join(
            [
                item.subject,
                f"Processing {report_type} report requested by "
                + f"{item.subject} for group {item.entity}"
                + get_filter_message(
                    report_type=report_type,
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
                ),
            ]
        )
    )
    report_url = await get_report(
        item=item,
        report_type=report_type,
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
    if report_url:
        await send_report(
            item=item,
            report_type=report_type,
            report_url=report_url,
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
