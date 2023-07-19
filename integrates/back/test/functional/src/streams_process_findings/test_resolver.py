from . import (
    get_result,
)
from asyncio import (
    sleep,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
)
from db_model.types import (
    SeverityScore,
)
from decimal import (
    Decimal,
)
import pytest
from search.operations import (
    search,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_findings")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "severity",
        "severity_score",
        "threat",
        "cvss_vector",
        "total_previous_findings",
    ],
    [
        [
            "admin@gmail.com",
            "This is an attack vector",
            CVSS31Severity(
                attack_complexity=Decimal("0.77"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.22"),
                confidentiality_impact=Decimal("0.22"),
                exploitability=Decimal("0.94"),
                integrity_impact=Decimal("0.22"),
                privileges_required=Decimal("0.62"),
                severity_scope=Decimal("0"),
                remediation_level=Decimal("0.95"),
                report_confidence=Decimal("1"),
                user_interaction=Decimal("0.85"),
            ),
            SeverityScore(
                base_score=Decimal("6.3"),
                temporal_score=Decimal("5.7"),
                cvss_v3="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/"
                "E:P/RL:O/RC:C",
                cvssf=Decimal("10.556"),
            ),
            "Threat test",
            "",
            0,
        ],
        [
            "admin@gmail.com",
            "This is an attack vector 2",
            # severity is equivalent to vulnerability 011 in criteria
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("0.85"),
                availability_impact=Decimal("0.22"),
                confidentiality_impact=Decimal("0.22"),
                exploitability=Decimal("0.94"),
                integrity_impact=Decimal("0.22"),
                privileges_required=Decimal("0.62"),
                severity_scope=Decimal("0"),
                remediation_level=Decimal("0.95"),
                report_confidence=Decimal("1"),
                user_interaction=Decimal("0.85"),
            ),
            SeverityScore(
                base_score=Decimal("5"),
                temporal_score=Decimal("4.5"),
                cvss_v3="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/"
                "E:P/RL:O/RC:C",
                cvssf=Decimal("2"),
            ),
            "Threat test 2",
            "",
            1,
        ],
        [
            "admin@gmail.com",
            "This is an attack vector 3",
            CVSS31Severity(),
            SeverityScore(
                base_score=Decimal("8.0"),
                temporal_score=Decimal("8.0"),
                cvss_v3="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H",
                cvssf=Decimal("256"),
            ),
            "Threat test 3",
            # F005 Privilege escalation
            "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H/E:X/RL:X/RC:X",
            2,
        ],
    ],
)
# pylint: disable=too-many-arguments
async def test_streams_process_findings(
    populate: bool,
    email: str,
    description: str,
    severity: CVSS31Severity,
    severity_score: SeverityScore,
    threat: str,
    cvss_vector: str,
    total_previous_findings: int,
) -> None:
    assert populate

    search_result = await search(index="findings", limit=10)

    assert search_result.total == total_previous_findings

    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        severity=severity,
        threat=threat,
        cvss_vector=cvss_vector,
    )

    assert "errors" not in result
    assert "success" in result["data"]["addFinding"]

    await sleep(5)

    query: str = f""""
    "match": {{
        "group_name": "group1",
        "description": "{description}",
        "threat": "{threat}"
    }}
    """
    search_result = await search(index="findings", limit=10, query=query)
    item = next(
        finding
        for finding in search_result.items
        if finding["description"] == description
        and finding["threat"] == threat
    )

    assert search_result.total == total_previous_findings + 1
    assert (
        Decimal(str(item["severity_score"]["base_score"]))
        == severity_score.base_score
    )
    assert (
        Decimal(str(item["severity_score"]["temporal_score"]))
        == severity_score.temporal_score
    )
    assert (
        Decimal(str(item["severity_score"]["cvssf"])) == severity_score.cvssf
    )
    assert item["state"]["status"] == FindingStateStatus.CREATED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_findings")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "threat",
    ],
    [
        [
            "user@gmail.com",
            "This is an attack vector",
            "Threat test",
        ],
    ],
)
async def test_streams_process_findings_no_add(
    populate: bool, email: str, description: str, threat: str
) -> None:
    assert populate

    search_result = await search(index="findings", limit=10)

    assert search_result

    prev_total_findings = search_result.total

    result: dict[str, Any] = await get_result(
        user=email, description=description, threat=threat
    )
    search_result = await search(index="findings", limit=10)

    assert "errors" in result
    assert search_result.total == prev_total_findings
