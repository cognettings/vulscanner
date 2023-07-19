# pylint: disable=invalid-name
"""
Add Exploit Code Maturity (E) to cvss vector.

Execution Time:    2023-04-26 at 16:12:54 UTC
Finalization Time: 2023-04-26 at 16:31:12 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from class_types.types import (
    Item,
)
from custom_utils import (
    cvss as cvss_utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from dynamodb import (
    keys,
    operations,
)
from organizations.domain import (
    get_all_group_names,
)
import time


async def get_finding_vulnerabilities_items(
    finding_id: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def persist_vulnerability_parameters(
    vulnerability: Vulnerability,
    cvss_v3: str | None,
) -> bool:
    old_severity_score = vulnerability.severity_score
    severity_score = None
    if cvss_v3:
        cvss_utils.validate_cvss_vector(cvss_v3)
        severity_score = cvss_utils.get_severity_score_from_cvss_vector(
            cvss_v3
        )
    if severity_score is None:
        return False
    if vulnerability.severity_score == severity_score:
        return False

    await vulns_model.update_metadata(
        vulnerability_id=vulnerability.id,
        finding_id=vulnerability.finding_id,
        metadata=VulnerabilityMetadataToUpdate(
            severity_score=severity_score,
        ),
    )
    print(
        f"Vuln updated {vulnerability.id=}, "
        f"from {old_severity_score=} to {severity_score=}"
    )

    return True


def set_exploitability_unproven(cvss_vector: str | None) -> str | None:
    if cvss_vector:
        metrics = cvss_vector.split("/")

        for idx, metric in enumerate(metrics):
            if metric.startswith("E:"):
                metrics[idx] = "E:U"
                break
        else:
            metrics.append("E:U")
        return "/".join(metrics)
    return None


async def process_vulnerability_item(item: Item) -> bool:
    vulnerability: Vulnerability = format_vulnerability(item)
    updated_severity_score = set_exploitability_unproven(
        vulnerability.severity_score.cvss_v3
        if vulnerability.severity_score
        else None
    )
    return await persist_vulnerability_parameters(
        vulnerability=vulnerability, cvss_v3=updated_severity_score
    )


async def process_finding(finding: Finding) -> None:
    items = await get_finding_vulnerabilities_items(finding_id=finding.id)
    if not items:
        return

    results = list(
        await collect(
            tuple(process_vulnerability_item(item) for item in items),
            workers=16,
        )
    )
    print(
        f"Finding updated {finding.id=} {len(items)=} {results.count(True)=}"
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)
    if not group_findings:
        return
    findings_filtered = [
        fin
        for fin in group_findings
        if fin.title
        in {
            "011. Use of software with known vulnerabilities",
            "393. Use of software with known vulnerabilities "
            "in development",
        }
        and fin.state.source == Source.MACHINE
    ]
    if not findings_filtered:
        return

    await collect(
        tuple(
            process_finding(finding=finding) for finding in findings_filtered
        ),
        workers=2,
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
        workers=8,
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
