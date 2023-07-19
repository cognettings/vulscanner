# pylint: disable=invalid-name
# type: ignore
"""
Fix CVSS 3.1 severity metrics for all machine findings. In particular, the
Exploit Code Maturity (E) or "exploitability" metric that had an error as
identified in commit f2ae0d4d20313eea5f998ee1984d2817bfa4dd87.

Execution Time:    2023-03-31 at 15:46:28 UTC
Finalization Time: 2023-03-31 at 15:53:01 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_utils import (
    cvss as cvss_utils,
)
from custom_utils.findings import (
    get_vulns_file,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    Exploitability,
)
from db_model.findings.types import (
    Finding,
    FindingMetadataToUpdate,
)
from decimal import (
    Decimal,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(
    criteria_vulns_data: dict,
    finding: Finding,
) -> None:
    finding_code = finding.title.split(". ")[0].strip()
    criteria_vulnerability = criteria_vulns_data[finding_code]

    finding_severity = finding.severity
    if criteria_vulnerability["score"]["temporal"][
        "exploit_code_maturity"
    ] == "X" and finding.severity.exploitability == Decimal("0.94"):
        finding_severity = finding_severity._replace(
            exploitability=Exploitability.X.value
        )

    if finding.severity_score != cvss_utils.get_severity_score_summary(
        finding_severity
    ):
        await findings_model.update_metadata(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=FindingMetadataToUpdate(
                severity=finding_severity
                if finding_severity != finding.severity
                else None,
                severity_score=cvss_utils.get_severity_score_summary(
                    finding_severity
                ),
            ),
        )


async def process_group(
    loaders: Dataloaders,
    criteria_vulns_data: dict,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_drafts_and_findings_all.load(
        group_name
    )
    machine_findings = [
        finding
        for finding in group_findings
        if finding.creation and finding.creation.source == Source.MACHINE
    ]
    if not machine_findings:
        return

    await collect(
        tuple(
            process_finding(
                criteria_vulns_data=criteria_vulns_data,
                finding=finding,
            )
            for finding in machine_findings
        ),
        workers=16,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    criteria_vulns_data = await get_vulns_file()
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                criteria_vulns_data=criteria_vulns_data,
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
