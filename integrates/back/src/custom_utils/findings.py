from aioextensions import (
    collect,
)
import aiofiles
from context import (
    FI_INTEGRATES_CRITERIA_REQUIREMENTS,
    FI_INTEGRATES_CRITERIA_VULNERABILITIES,
)
from custom_exceptions import (
    InvalidFileStructure,
    InvalidFindingTitle,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingEvidence,
    FindingVerificationSummary,
)
from db_model.groups.types import (
    Group,
)
import io
import re
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)
import yaml


async def append_records_to_file(
    records: list[dict[str, str]], new_file: UploadFile
) -> UploadFile:
    header = records[0].keys()
    values = [list(v) for v in [record.values() for record in records]]
    new_file_records: bytes = await new_file.read()
    await new_file.seek(0)
    new_file_header = new_file_records.decode("utf-8").split("\n")[0]
    new_file_records_str = r"\n".join(
        new_file_records.decode("utf-8").split("\n")[1:]
    )
    records_str = ""
    for record in values:
        records_str += repr(str(",".join(record)) + "\n").replace("'", "")
    aux = records_str
    records_str = (
        str(",".join(header))
        + r"\n"
        + aux
        + new_file_records_str.replace("'", "")
    )
    if new_file_header != str(",".join(header)):
        raise InvalidFileStructure()
    buff = io.BytesIO(
        records_str.encode("latin1").decode("unicode_escape").encode("utf-8")
    )
    uploaded_file = UploadFile(filename=new_file.filename)
    await uploaded_file.write(buff.read())
    await uploaded_file.seek(0)
    return uploaded_file


async def get_vulns_file() -> dict:
    """Parses the vulns info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_VULNERABILITIES, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())


async def get_requirements_file() -> dict[str, Any]:
    """Parses the requirements info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_REQUIREMENTS, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())


async def is_valid_finding_title(
    loaders: Dataloaders, title: str, vulns_info: dict | None = None
) -> bool:
    """
    Validates that new Draft and Finding titles conform to the standard
    format and are present in the whitelist.
    """
    if re.match(r"^\d{3}\. .+", title):
        if not vulns_info:
            vulns_info = await loaders.vulnerabilities_file.load("")
        try:
            vuln_number: str = title[:3]
            expected_vuln_title: str = vulns_info[vuln_number]["en"]["title"]
            if title == f"{vuln_number}. {expected_vuln_title}":
                return True
            # Invalid non-standard title
            raise InvalidFindingTitle()
        # Invalid vuln number
        except KeyError as error:
            raise InvalidFindingTitle() from error
    # Invalid format
    raise InvalidFindingTitle()


async def is_valid_finding_titles(
    loaders: Dataloaders, titles: list[str]
) -> bool:
    vulns_info = await loaders.vulnerabilities_file.load("")
    return all(
        await collect(
            is_valid_finding_title(
                loaders=loaders, title=title, vulns_info=vulns_info
            )
            for title in titles
        )
    )


def get_updated_evidence_date(
    finding: Finding, evidence: FindingEvidence
) -> datetime:
    updated_date = evidence.modified_date
    if is_finding_released(finding):
        release_date = get_finding_release_date(finding)
        if release_date and release_date > evidence.modified_date:
            updated_date = release_date

    return updated_date


def format_evidence(
    finding: Finding, evidence: FindingEvidence | None
) -> dict[str, Any]:
    if evidence is None:
        return {
            "date": None,
            "description": None,
            "is_draft": None,
            "url": None,
        }

    return {
        "date": datetime_utils.get_as_str(
            get_updated_evidence_date(finding, evidence)
        ),
        "description": evidence.description,
        "is_draft": evidence.is_draft,
        "url": evidence.url,
    }


def get_formatted_evidence(parent: Finding) -> dict[str, dict[str, Any]]:
    return {
        "animation": format_evidence(parent, parent.evidences.animation),
        "evidence_1": format_evidence(parent, parent.evidences.evidence1),
        "evidence_2": format_evidence(parent, parent.evidences.evidence2),
        "evidence_3": format_evidence(parent, parent.evidences.evidence3),
        "evidence_4": format_evidence(parent, parent.evidences.evidence4),
        "evidence_5": format_evidence(parent, parent.evidences.evidence5),
        "exploitation": format_evidence(parent, parent.evidences.exploitation),
    }


def is_deleted(finding: Finding) -> bool:
    return finding.state.status in {
        FindingStateStatus.DELETED,
        FindingStateStatus.MASKED,
    }


def is_verified(
    verification_summary: FindingVerificationSummary,
) -> bool:
    return verification_summary.requested == 0


def filter_findings_not_in_groups(
    groups: list[Group],
    findings: list[Finding],
) -> list[Finding]:
    return list(
        finding
        for finding in findings
        if finding.group_name not in set(group.name for group in groups)
    )


def is_finding_released(finding: Finding) -> bool:
    return bool(
        finding.unreliable_indicators.unreliable_open_vulnerabilities
        + finding.unreliable_indicators.unreliable_closed_vulnerabilities
        + finding.unreliable_indicators.open_vulnerabilities
        + finding.unreliable_indicators.closed_vulnerabilities
    )


def get_finding_release_date(finding: Finding) -> datetime | None:
    indicators = finding.unreliable_indicators
    return indicators.oldest_vulnerability_report_date


async def get_group_findings(
    *,
    group_name: str,
    loaders: Dataloaders,
) -> list[Finding]:
    findings = await loaders.group_findings.load(group_name.lower())

    return get_group_released_findings(findings=findings)


def get_group_released_findings(
    *,
    findings: list[Finding],
) -> list[Finding]:
    return [finding for finding in findings if is_finding_released(finding)]


async def get_finding_criteria_cwe_ids(
    loaders: Dataloaders, title: str
) -> list[str]:
    criteria_vulns = await loaders.vulnerabilities_file.load("")
    criteria_reqs = await loaders.requirements_file.load("")
    vulnerability_type = title.split(". ")[0]
    if vulnerability_type not in criteria_vulns:
        return []

    requirements = criteria_vulns[vulnerability_type]["requirements"]
    cwe_ids: list[str] = []
    for requirement in requirements:
        if requirement not in criteria_reqs:
            continue

        references: list[str] = criteria_reqs[requirement]["references"]
        cwe_ids.extend(
            [
                f'CWE-{reference.split(".")[1]}'
                for reference in references
                if reference.startswith("cwe.")
            ]
        )

    return cvss_utils.parse_cwe_ids(cwe_ids) or []
