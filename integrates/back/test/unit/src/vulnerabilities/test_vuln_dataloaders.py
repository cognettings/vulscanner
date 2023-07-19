from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.constants import (
    ACCEPTED_TREATMENT_STATUSES,
    ZR_FILTER_STATUSES,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
)
from itertools import (
    chain,
)
import pytest


@pytest.mark.asyncio
async def test_vulnerability_dataloader_parity() -> None:
    group_name = "unittesting"
    loaders: Dataloaders = get_new_context()
    # Chaining Finding vuln dataloaders
    all_findings: list[Finding] = await loaders.group_findings.load(group_name)
    all_finding_vulnerabilities = tuple(
        chain.from_iterable(
            await loaders.finding_vulnerabilities_all.load_many(
                {finding.id for finding in all_findings}
            )
        )
    )
    nz_vulnerabilities = [
        vulnerability
        for vulnerability in all_finding_vulnerabilities
        if (
            not vulnerability.zero_risk
            or vulnerability.zero_risk.status not in ZR_FILTER_STATUSES
        )
    ]
    group_vulnerabilities_connection = (
        await loaders.group_vulnerabilities.load(
            GroupVulnerabilitiesRequest(
                group_name=group_name,
                state_status=None,
                paginate=False,
            )
        )
    )
    group_vulnerabilities = tuple(
        edge.node for edge in group_vulnerabilities_connection.edges
    )
    assert sorted(nz_vulnerabilities) == sorted(group_vulnerabilities)


@pytest.mark.asyncio
async def test_vulnerability_dataloader_parity_with_status() -> None:
    group_name = "unittesting"
    loaders: Dataloaders = get_new_context()
    # Chaining Finding vuln dataloaders
    all_findings: list[Finding] = await loaders.group_findings.load(group_name)
    all_finding_vulnerabilities = tuple(
        chain.from_iterable(
            await loaders.finding_vulnerabilities_all.load_many(
                {finding.id for finding in all_findings}
            )
        )
    )
    filtered_finding_vulns = tuple(
        filter(
            lambda vuln: vuln.state.status
            == VulnerabilityStateStatus.VULNERABLE
            and (
                (
                    vuln.treatment
                    and vuln.treatment.status
                    not in ACCEPTED_TREATMENT_STATUSES
                )
                or vuln.treatment is None
            )
            and (
                (
                    vuln.zero_risk
                    and vuln.zero_risk.status not in ZR_FILTER_STATUSES
                )
                or vuln.zero_risk is None
            ),
            all_finding_vulnerabilities,
        )
    )

    # Group vulnerabilities dataloader (Forces)
    group_vulnerabilities_connection = (
        await loaders.group_vulnerabilities.load(
            GroupVulnerabilitiesRequest(
                group_name=group_name,
                is_accepted=False,
                state_status=VulnerabilityStateStatus.VULNERABLE,
                paginate=False,
            )
        )
    )
    vulnerable_locations_without_treatment = tuple(
        edge.node for edge in group_vulnerabilities_connection.edges
    )

    assert sorted(filtered_finding_vulns) == sorted(
        vulnerable_locations_without_treatment
    )
