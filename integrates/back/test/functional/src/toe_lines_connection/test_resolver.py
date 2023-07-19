from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
        ["customer_manager@fluidattacks.com"],
        ["hacker@fluidattacks.com"],
        ["reattacker@fluidattacks.com"],
        ["resourcer@fluidattacks.com"],
        ["reviewer@fluidattacks.com"],
    ],
)
async def test_get_toe_lines(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email, group_name="group1")
    lines = result["data"]["group"]["toeLinesConnection"]["edges"]
    assert lines[1]["node"]["attackedAt"] == "2021-01-20T05:00:00+00:00"
    assert lines[1]["node"]["attackedBy"] == "test@test.com"
    assert lines[1]["node"]["attackedLines"] == 23
    assert lines[1]["node"]["bePresent"] is False
    assert lines[1]["node"]["bePresentUntil"] == "2021-01-19T15:41:04+00:00"
    assert lines[1]["node"]["comments"] == "comment 1"
    assert lines[1]["node"]["filename"] == "test1/test.sh"
    assert lines[1]["node"]["firstAttackAt"] == "2020-01-19T15:41:04+00:00"
    assert lines[1]["node"]["lastAuthor"] == "customer1@gmail.com"
    assert lines[1]["node"]["lastCommit"] == "f9e4beb"
    assert lines[1]["node"]["loc"] == 4324
    assert lines[1]["node"]["modifiedDate"] == "2020-11-16T15:41:04+00:00"
    assert lines[1]["node"]["seenAt"] == "2020-01-01T15:41:04+00:00"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@gmail.com"],
        ["architect@fluidattacks.com"],
        ["service_forces@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_fail(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(user=email, group_name="group1")
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_root(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "rootId": "63298a73-9dff-46cf-b42d-9b2f01a56690",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    lines = result["data"]["group"]["toeLinesConnection"]["edges"]
    assert lines[0]["node"]["attackedAt"] == "2021-02-20T05:00:00+00:00"
    assert (
        lines[0]["node"]["root"]["id"]
        == "63298a73-9dff-46cf-b42d-9b2f01a56690"
    )
    assert lines[0]["node"]["attackedBy"] == "test2@test.com"
    assert lines[0]["node"]["attackedLines"] == 4
    assert lines[0]["node"]["bePresent"] is True
    assert lines[0]["node"]["bePresentUntil"] is None
    assert lines[0]["node"]["comments"] == "comment 2"
    assert lines[0]["node"]["filename"] == "test2/test#.config"
    assert lines[0]["node"]["firstAttackAt"] == "2020-02-19T15:41:04+00:00"
    assert lines[0]["node"]["lastAuthor"] == "customer2@gmail.com"
    assert lines[0]["node"]["lastCommit"] == "e17059d"
    assert lines[0]["node"]["loc"] == 180
    assert lines[0]["node"]["modifiedDate"] == "2020-11-15T15:41:04+00:00"
    assert lines[0]["node"]["seenAt"] == "2020-02-01T15:41:04+00:00"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_filename(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "filename": "test3",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "filename"
        ]
        == "test2/test#.config"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_min_loc(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "minLoc": 4324,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "loc"
        ]
        == 4324
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_max_loc(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "maxLoc": 180,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "loc"
        ]
        == 180
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_has_vulns(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "hasVulnerabilities": True,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 0

    variables = {
        "hasVulnerabilities": False,
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_from_date(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "fromModifiedDate": "2020-11-17T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "modifiedDate"
        ]
        == "2020-11-17T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_to_date(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "toModifiedDate": "2020-11-15T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "modifiedDate"
        ]
        == "2020-11-15T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_last_commit(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "lastCommit": "f9e4beb",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastCommit"
        ]
        == "f9e4beb"
    )

    variables = {
        "lastCommit": "e17059d",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastCommit"
        ]
        == "e17059d"
    )

    variables = {
        "lastCommit": "a281ru5",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastCommit"
        ]
        == "a281ru5"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_last_author(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "lastAuthor": "customer1",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastAuthor"
        ]
        == "customer1@gmail.com"
    )

    variables = {
        "lastAuthor": "customer2",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastAuthor"
        ]
        == "customer2@gmail.com"
    )

    variables = {
        "lastAuthor": "customer3@gmail.com",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "lastAuthor"
        ]
        == "customer3@gmail.com"
    )

    variables = {
        "lastAuthor": "customer",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_from_seen_at(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "fromSeenAt": "2020-02-01T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "seenAt"
        ]
        == "2020-02-01T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_to_seen_at(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "toSeenAt": "2019-01-01T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "seenAt"
        ]
        == "2019-01-01T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_min_attacked_lines(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "minAttackedLines": 120,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedLines"
        ]
        == 120
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_max_attacked_lines(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "maxAttackedLines": 4,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedLines"
        ]
        == 4
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_attacked_by(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "attackedBy": "test@test.com",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedBy"
        ]
        == "test@test.com"
    )

    variables = {
        "attackedBy": "test2",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedBy"
        ]
        == "test2@test.com"
    )

    variables = {
        "attackedBy": "test3",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedBy"
        ]
        == "test3@test.com"
    )

    variables = {
        "attackedBy": "test",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_comments(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "comments": "comment 1",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "comments"
        ]
        == "comment 1"
    )

    variables = {
        "comments": "comment",
    }
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_from_first_attack_at(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "fromFirstAttackAt": "2020-02-19T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "firstAttackAt"
        ]
        == "2020-02-19T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_to_first_attack_at(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "toFirstAttackAt": "2020-01-14T15:41:04+00:00",
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "firstAttackAt"
        ]
        == "2020-01-14T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_min_sorts_risk_level(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "minSortsRiskLevel": 80,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "sortsRiskLevel"
        ]
        == 80
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_max_sorts_risk_level(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "maxSortsRiskLevel": -1,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "sortsRiskLevel"
        ]
        == -1
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_be_present(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "bePresent": True,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 2

    variables["bePresent"] = False
    result = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_from_attacked_at(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {"fromAttackedAt": "2021-02-20T05:00:00+00:00"}
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedAt"
        ]
        == "2021-02-20T05:00:00+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_to_attacked_at(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {"toAttackedAt": "2021-01-20T05:00:00+00:00"}
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "attackedAt"
        ]
        == "2021-01-20T05:00:00+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_from_be_present_until(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "fromBePresentUntil": "2022-01-19T15:41:04+00:00"
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "bePresentUntil"
        ]
        == "2022-01-19T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_to_be_present_until(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "toBePresentUntil": "2021-01-19T15:41:04+00:00"
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "bePresentUntil"
        ]
        == "2021-01-19T15:41:04+00:00"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_descending_order_toe_lines(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "sort": {"field": "SORTS_RISK_LEVEL", "order": "DESC"}
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "sortsRiskLevel"
        ]
        == 80
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_ascending_order_toe_lines(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {
        "sort": {"field": "SORTS_RISK_LEVEL", "order": "ASC"}
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "sortsRiskLevel"
        ]
        == -1
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_descending_order_loc(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {"sort": {"field": "LOC", "order": "DESC"}}
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "loc"
        ]
        == 4324
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_ascending_order_loc(populate: bool, email: str) -> None:
    variables: dict[str, Any] = {"sort": {"field": "LOC", "order": "ASC"}}
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    assert len(result["data"]["group"]["toeLinesConnection"]["edges"]) == 3
    assert (
        result["data"]["group"]["toeLinesConnection"]["edges"][0]["node"][
            "loc"
        ]
        == 180
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_min_coverage(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "minCoverage": 49,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    edges = result["data"]["group"]["toeLinesConnection"]["edges"]
    assert edges[0]["node"]["attackedLines"] == 120
    assert edges[0]["node"]["loc"] == 243


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines_connection")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_get_toe_lines_by_max_coverage(
    populate: bool, email: str
) -> None:
    variables: dict[str, Any] = {
        "maxCoverage": 1,
    }
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group_name="group1",
        variables=variables,
    )
    edges = result["data"]["group"]["toeLinesConnection"]["edges"]
    assert edges[0]["node"]["attackedLines"] == 23
    assert edges[0]["node"]["loc"] == 4324
