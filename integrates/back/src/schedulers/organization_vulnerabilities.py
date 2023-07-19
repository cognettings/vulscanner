from aioextensions import (
    collect,
    in_thread,
)
import aiofiles
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    HTTPClientError,
    ReadTimeoutError,
)
from context import (
    CI_COMMIT_REF_NAME,
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from contextlib import (
    suppress,
)
import csv
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from custom_utils import (
    analytics as analytics_utils,
    organizations as orgs_utils,
)
from custom_utils.datetime import (
    get_as_str,
    get_now,
)
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
    iterate_organizations_and_groups,
    update_url,
)
from organizations.utils import (
    get_organization,
)
import os
from reports.it_report import (
    ITReport,
)
from s3.operations import (
    sign_url,
)
from s3.resource import (
    get_s3_resource,
)
from schedulers.common import (
    info,
)
from settings.logger import (
    LOGGING,
)
import tarfile
import tempfile

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
TTL = 21600


async def upload_file(bucket: str, file_path: str, file_name: str) -> None:
    async with aiofiles.open(file_path, mode="rb") as file_object:
        client = await get_s3_resource()
        try:
            await client.upload_fileobj(
                file_object,
                bucket,
                file_name.lstrip("/"),
            )
        except ClientError as ex:
            LOGGER.exception(ex, extra={"extra": locals()})
            raise CustomUnavailabilityError() from ex


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        ClientPayloadError,
        ConnectionResetError,
        ConnectTimeoutError,
        CustomUnavailabilityError,
        HTTPClientError,
        ReadTimeoutError,
        ServerTimeoutError,
        UnavailabilityError,
    ),
    sleep_seconds=40,
    max_attempts=5,
)
async def _get_group_data(
    *, group_name: str, loaders: Dataloaders
) -> list[list[str]]:
    findings = await get_group_findings(group_name=group_name, loaders=loaders)
    report = ITReport(
        data=findings,
        group_name=group_name,
        loaders=loaders,
        treatments=set(VulnerabilityTreatmentStatus),
        states=set(
            [
                VulnerabilityStateStatus["SAFE"],
                VulnerabilityStateStatus["VULNERABLE"],
            ]
        ),
        verifications=set(),
        closing_date=None,
        finding_title="",
        age=None,
        min_severity=None,
        max_severity=None,
        last_report=None,
        min_release_date=None,
        max_release_date=None,
        location="",
        generate_raw_data=True,
    )
    await report.generate_data()

    return report.raw_data


@retry_on_exceptions(
    exceptions=(
        ClientConnectorError,
        ClientError,
        ClientPayloadError,
        ConnectionResetError,
        ConnectTimeoutError,
        CustomUnavailabilityError,
        HTTPClientError,
        ReadTimeoutError,
        ServerTimeoutError,
        UnavailabilityError,
    ),
    sleep_seconds=40,
    max_attempts=5,
)
async def get_data(
    *, groups: tuple[str, ...], loaders: Dataloaders, organization_name: str
) -> list[list[str]]:
    all_data: tuple[list[list[str]], ...] = await collect(
        tuple(
            _get_group_data(group_name=group_name, loaders=loaders)
            for group_name in groups
        ),
        workers=1,
    )
    report = ITReport(
        data=[],
        group_name=organization_name,
        loaders=loaders,
        treatments=set(VulnerabilityTreatmentStatus),
        states=set(
            [
                VulnerabilityStateStatus["SAFE"],
                VulnerabilityStateStatus["VULNERABLE"],
            ]
        ),
        verifications=set(),
        closing_date=None,
        finding_title="",
        age=None,
        min_severity=None,
        max_severity=None,
        last_report=None,
        min_release_date=None,
        max_release_date=None,
        location="",
        generate_raw_data=True,
    )
    await report.generate_data()

    header = report.raw_data
    rows: list[list[str]] = []
    for data in all_data:
        if len(data) > 1:
            rows.extend(data[1:])

    severity_column: int = 0
    with suppress(ValueError):
        severity_column = (
            header[0].index("Severity") if len(header) > 0 else severity_column
        )

    rows_ord: tuple[list[str], ...] = tuple(
        sorted(
            rows,
            key=lambda row: float(str(row[severity_column]))
            if analytics_utils.is_decimal(str(row[severity_column]))
            else float("0.0"),
            reverse=True,
        )
    )
    rows_formatted: list[list[str]] = [
        [str(index), *row[1:]] for index, row in enumerate(rows_ord, 1)
    ]

    return [
        *header,
        *rows_formatted,
    ]


def write_file(
    *, directory: str, csv_filename: str, rows: list[list[str]]
) -> None:
    with open(
        os.path.join(directory, csv_filename),
        mode="w",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(
            csv_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writerow(rows[0])
        writer.writerows(rows[1:])


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    folder_date: str = get_as_str(get_now(), date_format="%Y-%m-%d")
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))
    info(f"All group names: {len(all_group_names)}")
    async for org_id, org_name, org_groups in (
        iterate_organizations_and_groups(loaders)
    ):
        if orgs_utils.is_deleted(await get_organization(loaders, org_id)):
            continue

        info(f"Working on organization {org_name}, {len(org_groups)} groups")
        date: str = get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")
        rows: list[list[str]] = await get_data(
            groups=tuple(all_group_names.intersection(org_groups)),
            loaders=loaders,
            organization_name=org_name,
        )
        csv_filename = f"{org_id}-{date}.csv"
        info(f"File: {csv_filename}, rows processed: {len(rows)}")
        with tempfile.TemporaryDirectory(
            prefix="integrates_organization_vulns_", ignore_cleanup_errors=True
        ) as directory:
            await in_thread(
                write_file,
                directory=directory,
                csv_filename=csv_filename,
                rows=rows,
            )

            with tarfile.open(
                os.path.join(directory, f"{org_id}-{date}.tar.gz"), "w:gz"
            ) as tar_file:
                tar_file.add(
                    os.path.join(directory, csv_filename), arcname=csv_filename
                )

            filename: str = (
                f"{CI_COMMIT_REF_NAME}/reports/organizations"
                f"/{folder_date}/{org_id}-{date}.tar.gz"
            )
            await upload_file(
                FI_AWS_S3_MAIN_BUCKET,
                str(tar_file.name),
                f"{FI_AWS_S3_PATH_PREFIX}analytics/{filename}",
            )
            signed_url: str = await sign_url(
                f"analytics/{filename}",
                TTL,
            )
            await update_url(
                org_id,
                org_name,
                signed_url,
            )
