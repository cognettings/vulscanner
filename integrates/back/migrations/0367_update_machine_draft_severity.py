# pylint: disable=invalid-name
# type: ignore
"""
Add the severity score to all findings

Execution Time:    2023-03-01 at 18:41:23 UTC
Finalization Time: 2023-03-01 at 18:44:39 UTC

Second execution accounting for trial supended groups
and the fix in severity score calculation.

Execution Time:    2023-03-31 at 20:41:48 UTC
Finalization Time: 2023-03-31 at 21:07:54 UTC
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
    FindingMetadataToUpdate,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await get_all_group_names(loaders)
    groups_findings = await loaders.group_drafts_and_findings_all.load_many(
        group_names
    )

    total_groups: int = len(group_names)
    for idx, (group_name, group_findings) in enumerate(
        zip(group_names, groups_findings)
    ):
        print(f"Processing group {group_name} ({idx+1}/{total_groups})...")
        futures = [
            findings_model.update_metadata(
                group_name=group_name,
                finding_id=finding.id,
                metadata=FindingMetadataToUpdate(
                    severity_score=cvss_utils.get_severity_score_summary(
                        finding.severity
                    )
                ),
            )
            for finding in group_findings
            if finding.severity_score
            != cvss_utils.get_severity_score_summary(finding.severity)
        ]
        await collect(futures, workers=15)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
