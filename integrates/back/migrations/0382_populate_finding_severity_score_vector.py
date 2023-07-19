# pylint: disable=invalid-name
"""
Populate field cvss_v3 in map severity_score for all findings.
This field contains the CVSS 3.1 vector string that later will be
pass down to all vulnerabilities.

Execution Time:    2023-04-19 at 18:25:46 UTC
Finalization Time: 2023-04-19 at 18:37:12 UTC

Execution Time:    2023-05-30 at 20:27:43 UTC
Finalization Time: 2023-05-30 at 20:35:35 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_utils import (
    cvss as cvss_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingMetadataToUpdate,
)
from db_model.types import (
    SeverityScore,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(finding: Finding) -> None:
    if finding.severity == CVSS31Severity():
        # Severity still not populated
        severity_score = SeverityScore()
    else:
        cvss3_vector = cvss_utils.parse_cvss31_severity_legacy(
            finding.severity
        )
        severity_score = cvss_utils.get_severity_score_from_cvss_vector(
            cvss3_vector
        )

    if finding.severity_score == severity_score:
        return

    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=FindingMetadataToUpdate(severity_score=severity_score),
    )
    print(f"Finding updated {finding.id=} {severity_score=}")


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings_all.load(group_name)
    if not group_findings:
        return

    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=16,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                progress=count / len(group_names),
            )
            for count, group in enumerate(group_names)
        ),
        workers=1,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
