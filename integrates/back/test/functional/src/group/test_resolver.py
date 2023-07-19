# pylint: disable=too-many-lines,import-error
from . import (
    get_forces_vulnerabilities,
    get_group_data,
    get_group_findings,
    get_group_forces,
    get_group_vulnerability_drafts,
    get_language_query,
    get_result,
)
from asyncio import (
    sleep,
)
from back.test.functional.src.upload_file import (
    get_group_vulnerabilities,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from organizations.utils import (
    get_organization,
)
import pytest
import simplejson as json
from typing import (
    Any,
)


def _get_key(item: Any) -> str:
    return str(item["node"]["where"])


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces(populate: bool, email: str) -> None:
    assert populate
    await sleep(5)
    group_name: str = "group1"
    result: dict = await get_group_forces(
        user=email, group=group_name, first=2, after=None
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 2
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert executions[1]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586390400000", "EXEC#b4c385a485464198a7511bc947fb7bf0"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is True
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=2,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 2
    assert executions[0]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert executions[1]["node"]["date"] == "2020-04-05T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586044800000", "EXEC#c1a30d853bb8474db28afd8212cf1707"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is True
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=2,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 4
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert executions[1]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert executions[2]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert executions[3]["node"]["date"] == "2020-04-05T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586044800000", "EXEC#c1a30d853bb8474db28afd8212cf1707"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces_date(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result = await get_group_forces(
        user=email,
        group=group_name,
        first=1,
        from_date="2020-04-09T00:00:00+00:00",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586736000000", "EXEC#01a92115f1f14cc8a7376ea96d962cf4"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is True
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        from_date="2020-04-09T00:00:00+00:00",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586390400000", "EXEC#b4c385a485464198a7511bc947fb7bf0"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        from_date="2020-04-09T00:00:00+00:00",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=None,
        from_date="2020-04-06T00:00:00+00:00",
        to_date="2020-04-10T00:00:00+00:00",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 2
    assert executions[0]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert executions[1]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586217600000", "EXEC#7ed594b55f144db88495f36348689577"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=5,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        from_date="2020-04-09T00:00:00+00:00",
        to_date="2020-04-10T00:00:00+00:00",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces_repo(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict = await get_group_forces(
        user=email,
        group=group_name,
        first=5,
        git_repo="Repository2",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-05T00:00:00+00:00"
    assert executions[0]["node"]["gitRepo"] == "Repository2"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586044800000", "EXEC#c1a30d853bb8474db28afd8212cf1707"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=5,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        git_repo="Repository2",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=5,
        git_repo="Repository11",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces_strictness(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict = await get_group_forces(
        user=email,
        group=group_name,
        first=2,
        strictness="strict",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 2
    assert executions[0]["node"]["strictness"] == "strict"
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert executions[1]["node"]["strictness"] == "strict"
    assert executions[1]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586217600000", "EXEC#7ed594b55f144db88495f36348689577"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is True
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        strictness="strict",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["strictness"] == "strict"
    assert executions[0]["node"]["date"] == "2020-04-05T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586044800000", "EXEC#c1a30d853bb8474db28afd8212cf1707"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        strictness="strict",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=20,
        strictness="lax",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert executions[0]["node"]["strictness"] == "lax"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586390400000", "EXEC#b4c385a485464198a7511bc947fb7bf0"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces_status(populate: bool, email: str) -> None:
    assert populate
    result: dict = await get_group_forces(
        user=email,
        group="group1",
        first=20,
        status="vulnerable",
    )
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 3
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert (
        executions[0]["node"]["vulnerabilities"][
            "numOfAcceptedVulnerabilities"
        ]
        == 1
    )
    assert (
        executions[0]["node"]["vulnerabilities"]["numOfOpenVulnerabilities"]
        == 2
    )
    assert (
        executions[0]["node"]["vulnerabilities"]["numOfClosedVulnerabilities"]
        == 1
    )
    assert executions[1]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert (
        executions[1]["node"]["vulnerabilities"][
            "numOfAcceptedVulnerabilities"
        ]
        == 0
    )
    assert (
        executions[1]["node"]["vulnerabilities"]["numOfOpenVulnerabilities"]
        == 2
    )
    assert (
        executions[1]["node"]["vulnerabilities"]["numOfClosedVulnerabilities"]
        == 2
    )

    result = await get_group_forces(
        user=email,
        group="group1",
        first=20,
        status="safe",
    )
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert (
        executions[0]["node"]["vulnerabilities"][
            "numOfAcceptedVulnerabilities"
        ]
        == 0
    )
    assert (
        executions[0]["node"]["vulnerabilities"]["numOfOpenVulnerabilities"]
        == 0
    )
    assert (
        executions[0]["node"]["vulnerabilities"]["numOfClosedVulnerabilities"]
        == 3
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_forces_execution_type(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict = await get_group_forces(
        user=email,
        group=group_name,
        first=2,
        execution_type="dynamic",
    )
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 2
    assert executions[0]["node"]["kind"] == "dynamic"
    assert executions[0]["node"]["date"] == "2020-04-13T00:00:00+00:00"
    assert executions[1]["node"]["kind"] == "dynamic"
    assert executions[1]["node"]["date"] == "2020-04-09T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586390400000", "EXEC#b4c385a485464198a7511bc947fb7bf0"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is True
    )
    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        execution_type="dynamic",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["kind"] == "dynamic"
    assert executions[0]["node"]["date"] == "2020-04-05T00:00:00+00:00"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586044800000", "EXEC#c1a30d853bb8474db28afd8212cf1707"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        after=json.loads(
            result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
                "endCursor"
            ]
        ),
        execution_type="dynamic",
    )
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        execution_type="static",
    )
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 1
    assert executions[0]["node"]["date"] == "2020-04-07T00:00:00+00:00"
    assert executions[0]["node"]["kind"] == "static"
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == '["1586217600000", "EXEC#7ed594b55f144db88495f36348689577"]'
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )

    result = await get_group_forces(
        user=email,
        group=group_name,
        first=10,
        execution_type="anotherstatic",
    )
    executions = result["data"]["group"]["forcesExecutionsConnection"]["edges"]
    assert len(executions) == 0
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "endCursor"
        ]
        == "[]"
    )
    assert (
        result["data"]["group"]["forcesExecutionsConnection"]["pageInfo"][
            "hasNextPage"
        ]
        is False
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email", "length", "can_get_rejected_vulns", "can_get_submitted_vulns"],
    [
        ["user@gmail.com", 2, False, False],
        ["hacker@fluidattacks.com", 3, True, True],
    ],
)
async def test_get_group_findings(
    populate: bool,
    email: str,
    length: int,
    can_get_rejected_vulns: bool,
    can_get_submitted_vulns: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict = await get_group_findings(
        user=email,
        group=group_name,
        can_get_rejected_vulns=can_get_rejected_vulns,
        can_get_submitted_vulns=can_get_submitted_vulns,
    )

    assert result["data"]["group"]["name"] == group_name
    assert "errors" not in result
    assert len(result["data"]["group"]["findings"]) == length
    findings = result["data"]["group"]["findings"]
    if email == "hacker@fluidattacks.com":
        assert "rejectedVulnerabilities" in str(findings)
        assert "submittedVulnerabilities" in str(findings)
        assert findings[0]["rejectedVulnerabilities"] == 1
        assert findings[1]["rejectedVulnerabilities"] == 0
        assert findings[2]["rejectedVulnerabilities"] == 0
        assert findings[0]["submittedVulnerabilities"] == 1
        assert findings[1]["submittedVulnerabilities"] == 0
        assert findings[2]["submittedVulnerabilities"] == 0
    elif email == "user@gmail.com":
        assert "rejectedVulnerabilities" not in str(findings)
        assert "submittedVulnerabilities" not in str(findings)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email", "verification_status", "length", "state"],
    [
        ["admin@gmail.com", "Requested", 1, "Requested"],
        ["admin@gmail.com", "On_hold", 1, "On_hold"],
        ["admin@gmail.com", "NotRequested", 1, "Verified"],
    ],
)
async def test_get_group_vulnerabilities_verification(
    populate: bool,
    email: str,
    verification_status: str,
    length: int,
    state: str,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict = await get_group_vulnerabilities(
        user=email,
        group_name=group_name,
        verification_status=verification_status,
    )

    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    assert len(result["data"]["group"]["vulnerabilities"]["edges"]) == length
    assert (
        result["data"]["group"]["vulnerabilities"]["edges"][0]["node"][
            "verification"
        ]
        == state
    )
    assert (
        result["data"]["group"]["vulnerabilities"]["edges"][0]["node"]["state"]
        == "VULNERABLE"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    consult: str = "This is a test comment"
    finding: str = "475041521"
    event: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Document not found"
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["hasMachine"]
    assert result["data"]["group"]["managed"]
    assert result["data"]["group"]["openVulnerabilities"] == 2
    assert result["data"]["group"]["closedVulnerabilities"] == 1
    assert result["data"]["group"]["lastClosedVulnerability"] == 40
    assert result["data"]["group"]["lastClosedVulnerabilityFinding"] == {
        "id": "475041521"
    }
    assert result["data"]["group"]["maxOpenSeverity"] == 4.3
    assert result["data"]["group"]["maxOpenSeverityFinding"] == {
        "id": "475041521"
    }
    assert result["data"]["group"]["meanRemediate"] == 2
    assert result["data"]["group"]["meanRemediateCriticalSeverity"] is None
    assert result["data"]["group"]["meanRemediateHighSeverity"] is None
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 3
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 4
    assert result["data"]["group"]["openFindings"] == 2
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["userDeletion"] is None
    assert result["data"]["group"]["tags"] == ["testing"]
    assert result["data"]["group"]["description"] == "this is group1"
    assert result["data"]["group"]["serviceAttributes"] == [
        "can_report_vulnerabilities",
        "can_request_zero_risk",
        "has_asm",
        "has_forces",
        "has_service_white",
        "has_squad",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]
    assert result["data"]["group"]["organization"] == "orgtest"
    assert result["data"]["group"]["userRole"] == email.split("@")[0]
    assert consult in [
        consult["content"] for consult in result["data"]["group"]["consulting"]
    ]
    assert finding in [
        finding["id"] for finding in result["data"]["group"]["findings"]
    ]
    assert event in [
        event["id"] for event in result["data"]["group"]["events"]
    ]
    assert result["data"]["group"]["roots"] == [
        {
            "createdAt": "2020-11-19T13:37:10+00:00",
            "createdBy": "admin@gmail.com",
            "id": "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "lastEditedAt": "2020-11-19T13:37:10+00:00",
            "lastEditedBy": "admin@gmail.com",
            "vulnerabilities": [
                {"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a"},
                {"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b"},
                {"id": "c188fac2-99b9-483d-8af3-76efbf7715dd"},
            ],
        }
    ]
    vulnerabilities_edges: list[dict[str, dict[str, str | None]]] = result[
        "data"
    ]["group"]["vulnerabilities"]["edges"]
    forces_vulnerabilities_edges: list[
        dict[str, dict[str, str | None]]
    ] = result["data"]["group"]["forcesVulnerabilities"]["edges"]
    assert vulnerabilities_edges == [
        {
            "node": {
                "id": "c188fac2-99b9-483d-8af3-76efbf7715dd",
                "state": "VULNERABLE",
                "treatmentStatus": "ACCEPTED",
                "zeroRisk": None,
            },
        },
        {
            "node": {
                "id": "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                "state": "VULNERABLE",
                "treatmentStatus": "UNTREATED",
                "zeroRisk": None,
            },
        },
        {
            "node": {
                "id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b",
                "state": "VULNERABLE",
                "treatmentStatus": "ACCEPTED",
                "zeroRisk": None,
            },
        },
    ]
    assert forces_vulnerabilities_edges == [
        edge
        for edge in vulnerabilities_edges
        if edge["node"]["treatmentStatus"] != "ACCEPTED"
        and edge["node"]["zeroRisk"] is None
    ]
    assert result["data"]["group"]["language"] == "EN"
    assert result["data"]["group"]["groupContext"] == "This is a dummy context"
    assert result["data"]["group"]["service"] == "WHITE"
    assert result["data"]["group"]["tier"] == "SQUAD"
    assert result["data"]["group"]["businessId"] == "1867"
    assert result["data"]["group"]["businessName"] == "Testing Company"
    assert result["data"]["group"]["sprintDuration"] == 3
    assert (
        result["data"]["group"]["sprintStartDate"]
        == "2022-06-06T00:00:00+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_group_forces_token(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    assert result["data"]["group"]["forcesToken"] is not None
    test_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJjaXBABCXYZ"
    assert result["data"]["group"]["forcesToken"] == test_token


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email", "group_name", "is_inheritance"],
    [
        ["admin@gmail.com", "group1", True],
        ["admin@gmail.com", "group5", False],
    ],
)
async def test_get_group_policies_inheritance(
    populate: bool, email: str, group_name: str, is_inheritance: bool
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(user=email, group=group_name)
    if is_inheritance:
        organization = await get_organization(loaders, organization_id)
        assert (
            result["data"]["group"]["maxAcceptanceDays"]
            == organization.policies.max_acceptance_days
        )
        assert str(result["data"]["group"]["maxAcceptanceSeverity"]) == str(
            organization.policies.max_acceptance_severity
        )
        assert (
            result["data"]["group"]["maxNumberAcceptances"]
            == organization.policies.max_number_acceptances
        )
        assert str(result["data"]["group"]["minAcceptanceSeverity"]) == str(
            organization.policies.min_acceptance_severity
        )
        assert str(result["data"]["group"]["minBreakingSeverity"]) == str(
            organization.policies.min_breaking_severity
        )
        assert (
            result["data"]["group"]["vulnerabilityGracePeriod"]
            == organization.policies.vulnerability_grace_period
        )
    else:
        group = await loaders.group.load(group_name)
        assert group
        assert group.policies
        assert (
            result["data"]["group"]["maxAcceptanceDays"]
            == group.policies.max_acceptance_days
        )
        assert str(result["data"]["group"]["maxAcceptanceSeverity"]) == str(
            group.policies.max_acceptance_severity
        )
        assert (
            result["data"]["group"]["maxNumberAcceptances"]
            == group.policies.max_number_acceptances
        )
        assert str(result["data"]["group"]["minAcceptanceSeverity"]) == str(
            group.policies.min_acceptance_severity
        )
        assert str(result["data"]["group"]["minBreakingSeverity"]) == str(
            group.policies.min_breaking_severity
        )
        assert (
            result["data"]["group"]["vulnerabilityGracePeriod"]
            == group.policies.vulnerability_grace_period
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_group_vulnerabilities(populate: bool, email: str) -> None:
    assert populate
    group_vulns: dict = await get_group_vulnerabilities(
        user=email, group_name="group1", treatment_status="NEW"
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilities"]["edges"],
        key=_get_key,
    ) == [
        {
            "node": {
                "state": "VULNERABLE",
                "treatmentStatus": "UNTREATED",
                "verification": "Verified",
                "where": "192.168.1.20",
            }
        }
    ]

    group_vulns = await get_group_vulnerabilities(
        user=email, group_name="group1", treatment_status="IN_PROGRESS"
    )
    assert "errors" not in group_vulns
    assert (
        sorted(
            group_vulns["data"]["group"]["vulnerabilities"]["edges"],
            key=_get_key,
        )
        == []
    )

    group_vulns = await get_group_vulnerabilities(
        user=email, group_name="group1", treatment_status="ACCEPTED"
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilities"]["edges"],
        key=_get_key,
    ) == sorted(
        [
            {
                "node": {
                    "state": "SAFE",
                    "treatmentStatus": "ACCEPTED",
                    "verification": None,
                    "where": "192.168.1.1",
                }
            },
            {
                "node": {
                    "state": "VULNERABLE",
                    "treatmentStatus": "ACCEPTED",
                    "verification": "Requested",
                    "where": "192.168.1.2",
                }
            },
            {
                "node": {
                    "state": "VULNERABLE",
                    "treatmentStatus": "ACCEPTED",
                    "verification": "On_hold",
                    "where": "192.168.1.3",
                }
            },
        ],
        key=_get_key,
    )

    group_vulns = await get_group_vulnerabilities(
        user=email, group_name="group1", treatment_status="ACCEPTED_UNDEFINED"
    )
    assert "errors" not in group_vulns
    assert (
        sorted(
            group_vulns["data"]["group"]["vulnerabilities"]["edges"],
            key=_get_key,
        )
        == []
    )

    group_vulns = await get_group_vulnerabilities(
        user=email, group_name="group1", treatment_status="UNTREATED"
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilities"]["edges"],
        key=_get_key,
    ) == [
        {
            "node": {
                "state": "VULNERABLE",
                "treatmentStatus": "UNTREATED",
                "verification": "Verified",
                "where": "192.168.1.20",
            }
        }
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@fluidattacks.com"],
    ],
)
async def test_get_group_vulnerability_drafts(
    populate: bool, email: str
) -> None:
    assert populate
    group_vulns = await get_group_vulnerability_drafts(
        user=email,
        group_name="group1",
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilityDrafts"]["edges"],
        key=_get_key,
    ) == [
        {
            "node": {
                "state": "REJECTED",
                "where": "192.168.1.3",
                "specific": "2324",
            }
        },
        {
            "node": {
                "state": "SUBMITTED",
                "where": "192.168.1.3",
                "specific": "2323",
            }
        },
    ]

    group_vulns = await get_group_vulnerability_drafts(
        user=email, group_name="group1", state_status="SUBMITTED"
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilityDrafts"]["edges"],
        key=_get_key,
    ) == sorted(
        [
            {
                "node": {
                    "state": "SUBMITTED",
                    "where": "192.168.1.3",
                    "specific": "2323",
                }
            },
        ],
        key=_get_key,
    )

    group_vulns = await get_group_vulnerability_drafts(
        user=email, group_name="group1", state_status="REJECTED"
    )
    assert "errors" not in group_vulns
    assert sorted(
        group_vulns["data"]["group"]["vulnerabilityDrafts"]["edges"],
        key=_get_key,
    ) == [
        {
            "node": {
                "state": "REJECTED",
                "where": "192.168.1.3",
                "specific": "2324",
            }
        },
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_forces_vulnerabilities(populate: bool, email: str) -> None:
    assert populate
    forces_open_vulns: dict = await get_forces_vulnerabilities(
        user=email, group_name="group1", state_status="VULNERABLE"
    )
    assert forces_open_vulns["data"]["group"]["forcesVulnerabilities"][
        "edges"
    ] == [
        {
            "node": {
                "state": "VULNERABLE",
                "treatmentStatus": "UNTREATED",
                "where": "192.168.1.20",
                "specific": "9999",
                "rootNickname": "",
                "zeroRisk": None,
            },
        }
    ]

    # Both safe and accepted vulns will be empty because they have treatments
    forces_safe_vulns: dict = await get_forces_vulnerabilities(
        user=email, group_name="group1", state_status="SAFE"
    )
    assert (
        forces_safe_vulns["data"]["group"]["forcesVulnerabilities"]["edges"]
        == []
    )

    forces_accepted_vulns: dict = await get_forces_vulnerabilities(
        user=email, group_name="group1", state_status="SAFE"
    )
    assert (
        forces_accepted_vulns["data"]["group"]["forcesVulnerabilities"][
            "edges"
        ]
        == []
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_language_query(populate: bool, email: str) -> None:
    assert populate
    result: dict = await get_language_query(user=email, group_name="group1")
    assert result["data"]["group"]["language"] == "EN"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_group_data(
    populate: bool,
    email: str,
    snapshot: Any,
) -> None:
    """
    Test for GetGroupData
    in /front/.../GroupSettingsView/queries.ts
    """
    group_name: str = "group1"
    assert populate
    result: dict = await get_group_data(
        user=email,
        group_name=group_name,
    )
    json_result = str(json.dumps(result, indent=2))
    snapshot.assert_match(json_result, "snapshot.json")
