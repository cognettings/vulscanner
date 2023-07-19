# pylint: disable=invalid-name
"""
Populate the is_draft attribute in finding evidences.

Execution Time:    2023-05-15 at 13:48:18 UTC
Finalization Time: 2023-05-15 at 13:56:45 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingEvidenceName,
)
from db_model.findings.types import (
    Finding,
    FindingEvidenceToUpdate,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def process_finding(finding: Finding) -> None:
    await collect(
        findings_model.update_evidence(
            current_value=evidence,
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[evidence_id],
            evidence=FindingEvidenceToUpdate(is_draft=evidence.is_draft),
        )
        for evidence_id, evidence in finding.evidences._asdict().items()
        if evidence is not None
    )


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
        workers=64,
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
        workers=4,
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
