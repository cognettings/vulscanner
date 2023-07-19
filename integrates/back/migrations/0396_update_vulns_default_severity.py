# pylint: disable=invalid-name
"""
Add RL:O and RC:C to cvss vector for SCA vulns that do not have it set
from the advisories.

Start Time:    2023-05-25 at 12:50:25 UTC
Finalization Time: 2023-05-25 at 13:06:25 UTC
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_exceptions import (
    InvalidCVSS3VectorString,
)
from custom_utils import (
    cvss as cvss_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from organizations import (
    domain as orgs_domain,
)
import time
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_finding_unreliable_indicators,
)


def set_default_temporal_scores(cvss_vector: str) -> str:
    metrics = cvss_vector.split("/")

    if first_match := next(
        (met for met in metrics if met.startswith("E:")), None
    ):
        metrics[metrics.index(first_match)] = "E:U"
    else:
        metrics.append("E:U")

    if not any(met for met in metrics if met.startswith("RL:")):
        metrics.append("RL:O")

    if not any(met for met in metrics if met.startswith("RC:")):
        metrics.append("RC:C")

    return "/".join(metrics)


def get_updated_severity(old_score: SeverityScore) -> SeverityScore | None:
    updated_cvss = set_default_temporal_scores(old_score.cvss_v3)
    try:
        cvss_utils.validate_cvss_vector(updated_cvss)
    except InvalidCVSS3VectorString:
        return None

    return cvss_utils.get_severity_score_from_cvss_vector(updated_cvss)


async def process_group(loaders: Dataloaders, group: str) -> None:
    print(f"Processing {group}")
    updated_csv = []
    group_findings = await loaders.group_findings.load(group)
    findings = [
        fin
        for fin in group_findings
        if fin.title[0:3] in {"011", "393"}
        and fin.creation
        and fin.creation.modified_by == "machine@fluidattacks.com"
    ]

    findings_vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings]
    )

    machine_vulns_to_update = [
        vuln
        for vuln in findings_vulns
        if (
            vuln.hacker_email == "machine@fluidattacks.com"
            or vuln.state.source == Source.MACHINE
        )
        and vuln.severity_score
    ]

    for vuln in machine_vulns_to_update:
        if (
            (old_score := vuln.severity_score)
            and (upd_score := get_updated_severity(old_score))
            and vuln.severity_score != upd_score
        ):
            await vulns_model.update_metadata(
                vulnerability_id=vuln.id,
                finding_id=vuln.finding_id,
                metadata=VulnerabilityMetadataToUpdate(
                    severity_score=upd_score,
                ),
            )

            updated_csv.append(
                [
                    vuln.group_name,
                    vuln.id,
                    vuln.severity_score.temporal_score,
                    upd_score.cvss_v3,
                    upd_score.temporal_score,
                ]
            )

    for finding in findings:
        await update_finding_unreliable_indicators(
            finding.id,
            {
                EntityAttr.max_open_severity_score,
            },
        )

    with open("updated_vulns.csv", "a+", encoding="utf-8") as handler:
        writer = csv.writer(handler)
        writer.writerows(updated_csv)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    await collect(
        [process_group(loaders, group) for group in groups], workers=15
    )


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
