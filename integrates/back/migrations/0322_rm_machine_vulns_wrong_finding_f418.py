# pylint: disable=invalid-name
# type: ignore
"""
Remove vulnerabilities reported by Machine to a wrong finding (F418)
and queue execution for the correct finding (F427) in all of the groups roots
so they are reported correctly

Execution Time:    2022-11-15 at 12:48:46 UTC
Finalization Time: 2022-11-15 at 12:49:45 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
)
from machine.jobs import (
    queue_job_new,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_finding_unreliable_indicators,
)
from vulnerabilities.domain import (
    remove_vulnerability,
)


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    findings = await loaders.group_drafts_and_findings.load_many_chained(
        list(groups)
    )
    findings_418 = [
        finding for finding in findings if finding.title.startswith("418")
    ]
    findings_vulns = await loaders.finding_vulnerabilities.load_many(
        [finding.id for finding in findings_418]
    )
    total_findings = len(findings_418)
    groups_with_issues = set()
    for idx, (finding, vulns) in enumerate(zip(findings_418, findings_vulns)):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name} ({idx+1}/{total_findings})..."
        )
        wrong_vulns = [
            vuln
            for vuln in vulns
            if (
                vuln.skims_method is not None
                and vuln.skims_method.endswith("docker_port_exposed")
            )
        ]
        if wrong_vulns:
            print("\t" + f"{len(wrong_vulns)} vulnerabilities with errors")
            await collect(
                (
                    remove_vulnerability(
                        loaders,
                        finding.id,
                        vuln.id,
                        VulnerabilityStateReason.REPORTING_ERROR,
                        "jecheverri@fluidattacks.com",
                        True,
                    )
                    for vuln in wrong_vulns
                ),
                workers=15,
            )
            await update_finding_unreliable_indicators(
                finding.id,
                {
                    EntityAttr.closed_vulnerabilities,
                    EntityAttr.newest_vulnerability_report_date,
                    EntityAttr.oldest_open_vulnerability_report_date,
                    EntityAttr.oldest_vulnerability_report_date,
                    EntityAttr.open_vulnerabilities,
                    EntityAttr.status,
                    EntityAttr.where,
                    EntityAttr.treatment_summary,
                    EntityAttr.verification_summary,
                },
            )
            groups_with_issues.add(finding.group_name)
    print(groups_with_issues)
    await collect(
        (
            queue_job_new(group, loaders, ["F427"])
            for group in groups_with_issues
        ),
        workers=15,
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
