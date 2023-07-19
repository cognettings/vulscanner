# pylint: disable=too-many-arguments
from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
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
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "severity",
        "severity_score",
        "threat",
        "cvss_vector",
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
        ],
    ],
)
async def test_add_finding(
    populate: bool,
    email: str,
    description: str,
    severity: CVSS31Severity,
    severity_score: SeverityScore,
    threat: str,
    cvss_vector: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        severity=severity,
        threat=threat,
        cvss_vector=cvss_vector,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFinding"]
    assert result["data"]["addFinding"]["success"]
    loaders = get_new_context()
    group_findings = await loaders.group_findings.load("group1")
    new_finding = next(
        finding
        for finding in group_findings
        if finding.description == description and finding.threat == threat
    )
    assert new_finding.state.status is FindingStateStatus.CREATED
    assert new_finding.severity_score
    assert new_finding.severity_score == severity_score


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "threat"],
    [
        ["user@gmail.com", "This is an attack vector", "Threat test"],
    ],
)
async def test_add_finding_access_denied(
    populate: bool, email: str, description: str, threat: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, description=description, threat=threat
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "threat", "min_time_to_remediate"],
    [
        [
            "admin@gmail.com",
            "min_time_to_remediate",
            "Threat test",
            0,
        ],
        [
            "admin@gmail.com",
            "min_time_to_remediate",
            "Threat test",
            -1,
        ],
    ],
)
async def test_add_finding_positive_min_time_to_remediate(
    populate: bool,
    email: str,
    description: str,
    threat: str,
    min_time_to_remediate: int,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        min_time_to_remediate=min_time_to_remediate,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Min time to remediate should be a positive number"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "threat", "unfulfilled_requirements"],
    [
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Threat test",
            ["-21"],
        ],
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Threat test",
            [""],
        ],
        [
            "admin@gmail.com",
            "unfulfilled_requirements",
            "Threat test",
            ["158", "21212121"],
        ],
    ],
)
async def test_add_finding_invalid_requirements_in_criteria(
    populate: bool,
    email: str,
    description: str,
    threat: str,
    unfulfilled_requirements: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The requirement is not valid in the vulnerability"
        or result["errors"][0]["message"]
        == "Exception - Invalid field length in form"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "threat", "title"],
    [
        [
            "admin@gmail.com",
            "invalid_title",
            "Threat test",
            "F001. Test",
        ],
        [
            "admin@gmail.com",
            "invalid_title",
            "Threat test",
            "Test",
        ],
        [
            "admin@gmail.com",
            "invalid_title",
            "Threat test",
            "001",
        ],
    ],
)
async def test_add_finding_invalid_title(
    populate: bool,
    email: str,
    description: str,
    threat: str,
    title: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        title=title,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The inserted Draft/Finding title is invalid"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "threat",
        "title",
        "unfulfilled_requirements",
    ],
    [
        [
            "admin@gmail.com",
            "duplicated_threat",
            "Updated threat",
            "001. SQL injection - C Sharp SQL API",
            ["169"],
        ],
    ],
)
async def test_add_finding_duplicated_threat(
    populate: bool,
    email: str,
    description: str,
    threat: str,
    title: str,
    unfulfilled_requirements: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        title=title,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Finding with the same threat already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "threat",
        "title",
        "unfulfilled_requirements",
    ],
    [
        [
            "admin@gmail.com",
            "I just have updated the description",
            "duplicated_description",
            "001. SQL injection - C Sharp SQL API",
            ["169"],
        ],
    ],
)
async def test_add_finding_duplicated_description(
    populate: bool,
    email: str,
    description: str,
    threat: str,
    title: str,
    unfulfilled_requirements: list[str],
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        title=title,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Finding with the same description already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    ["email", "description", "severity", "threat"],
    [
        [
            "admin@gmail.com",
            "invalid_severity",
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("10.1"),
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
            "Threat test",
        ],
        [
            "admin@gmail.com",
            "invalid_severity",
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("-1"),
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
            "Threat test",
        ],
        [
            "admin@gmail.com",
            "invalid_severity",
            CVSS31Severity(
                attack_complexity=Decimal("0.44"),
                attack_vector=Decimal("-0.01"),
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
            "Threat test",
        ],
    ],
)
async def test_add_finding_invalid_severity(
    populate: bool,
    email: str,
    description: str,
    severity: CVSS31Severity,
    threat: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        threat=threat,
        severity=severity,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Invalid, severity update values out of range"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "recommendation",
        "attack_vector_description",
        "unfulfilled_requirements",
        "threat",
    ],
    [
        [
            "admin@gmail.com",
            "",
            "recommendation",
            "attack_vector_description",
            ["001"],
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "",
            "attack_vector_description",
            ["001"],
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "recommendation",
            "",
            ["001"],
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "recommendation",
            "attack_vector_description",
            [],
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "recommendation",
            "attack_vector_description",
            ["001"],
            "",
        ],
    ],
)
async def test_add_finding_invalid_length(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    attack_vector_description: str,
    unfulfilled_requirements: list[str],
    threat: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        attack_vector_description=attack_vector_description,
        unfulfilled_requirements=unfulfilled_requirements,
        threat=threat,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Invalid field length in form"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding")
@pytest.mark.parametrize(
    [
        "email",
        "description",
        "recommendation",
        "attack_vector_description",
        "threat",
    ],
    [
        [
            "admin@gmail.com",
            "  ",
            "recommendation",
            "attack_vector_description",
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            " ",
            "attack_vector_description",
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "recommendation",
            "  ",
            "threat",
        ],
        [
            "admin@gmail.com",
            "description",
            "recommendation",
            "attack_vector_description",
            " ",
        ],
    ],
)
async def test_add_finding_invalid_empty(
    populate: bool,
    email: str,
    description: str,
    recommendation: str,
    attack_vector_description: str,
    threat: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        description=description,
        recommendation=recommendation,
        attack_vector_description=attack_vector_description,
        threat=threat,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Invalid characters"
