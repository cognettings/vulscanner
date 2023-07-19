# pylint: disable=import-error, too-many-arguments
from . import (
    get_me_vulnerabilities_assigned_ids,
    get_result,
    get_tag,
    get_vulnerabilities,
)
from asyncio import (
    sleep,
)
from back.test.functional.src.add_group_tags import (
    get_result as add_tags,
)
from db_model.enums import (
    CredentialType,
)
import json
import pytest
from schedulers.update_portfolios import (
    main,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ("email", "tags_to_add", "group_name"),
    (
        ("admin@gmail.com", ["test-groups"], "group1"),
        ("admin@gmail.com", ["test-groups", "test-alone"], "group2"),
    ),
)
async def test_add_group_tags(
    populate: bool,
    email: str,
    tags_to_add: list[str],
    group_name: str,
) -> None:
    assert populate
    await sleep(2)

    result = await add_tags(
        user=email,
        group=group_name,
        tags=tags_to_add,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupTags"]
    assert result["data"]["addGroupTags"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    (
        "email",
        "role",
        "permissions",
        "phone",
        "groups_length",
        "assigned",
        "enrolled",
        "credentials",
        "tags_length",
        "group_tags",
    ),
    (
        (
            "admin@gmail.com",
            "admin",
            21,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "1111111111",
            },
            3,
            [],
            True,
            [],
            2,
            2,
        ),
        (
            "user@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182132",
            },
            1,
            [{"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b"}],
            True,
            [],
            1,
            2,
        ),
        (
            "user_manager@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "77777777777777",
            },
            1,
            [{"id": "de70c2f7-7ec7-49aa-9a84-aff4fbe5d1ad"}],
            False,
            [],
            1,
            2,
        ),
        (
            "vulnerability_manager@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "51",
                "countryCode": "PE",
                "nationalNumber": "1111111111111",
            },
            1,
            [{"id": "be09edb7-cd5c-47ed-bee4-97c645acdce8"}],
            False,
            [],
            1,
            2,
        ),
        (
            "hacker@gmail.com",
            "hacker",
            14,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182131",
            },
            2,
            [],
            False,
            [],
            1,
            2,
        ),
        (
            "reattacker@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "4444444444444",
            },
            1,
            [],
            False,
            [],
            1,
            2,
        ),
        (
            "resourcer@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "33333333333",
            },
            1,
            [],
            False,
            [],
            1,
            2,
        ),
        (
            "reviewer@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "7777777777",
            },
            2,
            [],
            False,
            [],
            1,
            2,
        ),
        ("service_forces@gmail.com", "user", 3, None, 1, [], False, [], 1, 2),
        (
            "customer_manager@fluidattacks.com",
            "hacker",
            14,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "9999999999999",
            },
            1,
            [],
            True,
            [
                {
                    "azureOrganization": None,
                    "isPat": False,
                    "isToken": True,
                    "key": None,
                    "name": "cred_https_token",
                    "oauthType": "",
                    "organization": {
                        "id": "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
                    },
                    "owner": "customer_manager@fluidattacks.com",
                    "password": None,
                    "token": "token test",
                    "type": CredentialType.HTTPS,
                    "user": None,
                },
            ],
            1,
            2,
        ),
    ),
)
async def test_get_me(  # noqa: pylint: disable=too-many-locals
    populate: bool,
    email: str,
    role: str,
    permissions: int,
    phone: dict[str, str],
    groups_length: int,
    assigned: list[dict[str, str]],
    enrolled: bool,
    credentials: list[dict[str, str]],
    tags_length: int,
    group_tags: int,
) -> None:
    assert populate
    await main()
    org_name: str = "orgtest"
    organization: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        user=email,
        org_id=organization,
    )
    assert "errors" not in result
    assert '{"hasAccessToken": false' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert result["data"]["me"]["enrolled"] == enrolled
    assert result["data"]["me"]["vulnerabilitiesAssigned"] == assigned
    assert result["data"]["me"]["credentials"] == credentials
    assert not result["data"]["me"]["isConcurrentSession"]
    assert len(result["data"]["me"]["notificationsPreferences"]["email"]) == 17
    assert result["data"]["me"]["organizations"][0]["name"] == org_name
    assert (
        len(result["data"]["me"]["organizations"][0]["groups"])
        == groups_length
    )
    assert len(result["data"]["me"]["permissions"]) == permissions
    assert result["data"]["me"]["phone"] == phone
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == role
    assert len(result["data"]["me"]["tags"]) == tags_length
    assert result["data"]["me"]["tours"] == {
        "newGroup": False,
        "newRoot": False,
    }
    assert result["data"]["me"]["pendingEvents"][0]["id"] == "418900971"
    assert result["data"]["me"]["userEmail"] == email

    is_fluid_email: bool = result["data"]["me"]["userEmail"].endswith(
        "@fluidattacks.com"
    )
    is_fluid_permission_on_list: bool = (
        "can_assign_vulnerabilities_to_fluidattacks_staff"
        in result["data"]["me"]["permissions"]
    )
    assert not is_fluid_email or is_fluid_permission_on_list
    assert result["data"]["me"]["userName"] == "unit test"
    assert result["data"]["me"]["__typename"] == "Me"

    result_ = await get_tag(
        user=email,
        organization_id=organization,
        tag_name=list(
            sorted(result["data"]["me"]["tags"], key=lambda x: x["name"])
        )[-1]["name"],
    )
    assert "errors" not in result_
    assert len(result_["data"]["tag"]["groups"]) == group_tags


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ["email", "length"],
    [
        ["user@gmail.com", 1],
        ["user_manager@gmail.com", 1],
        ["vulnerability_manager@gmail.com", 1],
    ],
)
async def test_get_me_assigned(
    populate: bool, email: str, length: int
) -> None:
    assert populate
    result: dict[str, Any] = await get_vulnerabilities(
        user=email,
    )
    assert "errors" not in result
    assert len(result["data"]["me"]["vulnerabilitiesAssigned"]) == length
    assert len(result["data"]["me"]["reattacks"]["edges"]) == 1
    assert result["data"]["me"]["reattacks"]["edges"][0]["node"] == {
        "lastRequestedReattackDate": "2019-12-31 19:45:12"
    }
    assert (
        len(result["data"]["me"]["findingReattacksConnection"]["edges"]) == 2
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "id"
        ]
        == "475041521"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "status"
        ]
        == "VULNERABLE"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "id"
        ]
        == "3c475384-834c-47b0-ac71-a41a022e401c"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "status"
        ]
        == "VULNERABLE"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "groupName"
        ]
        == "group1"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "groupName"
        ]
        == "group1"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "verificationSummary"
        ]["requested"]
        == 3
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "verificationSummary"
        ]["requested"]
        == 1
    )
    assert (
        len(
            result["data"]["me"]["findingReattacksConnection"]["edges"][0][
                "node"
            ]["vulnerabilitiesToReattackConnection"]["edges"]
        )
        == 1
    )
    assert (
        len(
            result["data"]["me"]["findingReattacksConnection"]["edges"][1][
                "node"
            ]["vulnerabilitiesToReattackConnection"]["edges"]
        )
        == 0
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ["email"],
    [
        ["vulnerability_manager@gmail.com"],
        ["user_manager@gmail.com"],
    ],
)
async def test_get_me_vulnerabilities_assigned_ids(
    populate: bool,
    email: str,
    snapshot: Any,
) -> None:
    """
    Test for GetMeVulnerabilitiesAssignedIds
    in /front/.../navbar/to-do/queries.ts
    """
    assert populate
    result: dict = await get_me_vulnerabilities_assigned_ids(
        user=email,
    )
    json_result = json.dumps(result, indent=2)
    snapshot.assert_match(str(json_result), "snapshot.json")
