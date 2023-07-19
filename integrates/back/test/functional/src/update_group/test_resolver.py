from . import (
    get_query_group,
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupService,
    GroupStateJustification,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    GroupState,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group")
@pytest.mark.parametrize(
    [
        "email",
        "group_name",
        "group_current_state",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_arm",
        "tier",
    ],
    [
        [
            "admin@gmail.com",
            "unittesting",
            GroupState(
                has_machine=True,
                has_squad=True,
                managed=GroupManaged["MANAGED"],
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2020-05-20T22:00:00+00:00"
                ),
                service=GroupService.WHITE,
                status=GroupStateStatus.ACTIVE,
                tier=GroupTier.OTHER,
                type=GroupSubscriptionType.CONTINUOUS,
            ),
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            True,
            True,
            True,
            GroupTier.SQUAD,
        ],
        [
            "admin@gmail.com",
            "group2",
            GroupState(
                has_machine=False,
                has_squad=True,
                managed=GroupManaged["MANAGED"],
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2020-05-20T22:00:00+00:00"
                ),
                service=GroupService.BLACK,
                status=GroupStateStatus.ACTIVE,
                tier=GroupTier.OTHER,
                type=GroupSubscriptionType.ONESHOT,
            ),
            GroupService.WHITE,
            GroupSubscriptionType.ONESHOT,
            False,
            False,
            False,
            GroupTier.OTHER,
        ],
    ],
)
async def test_update_group(
    # pylint: disable=too-many-arguments
    populate: bool,
    email: str,
    group_name: str,
    group_current_state: GroupState,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
    tier: GroupTier,
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.state.type == group_current_state.type
    assert group.state.has_machine == group_current_state.has_machine
    assert group.state.has_squad == group_current_state.has_squad
    assert group.state.justification is None
    assert group.state.tier == group_current_state.tier
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        service=service,
        subscription=subscription,
        has_machine=has_machine,
        has_squad=has_squad,
        has_arm=has_arm,
        tier=tier,
    )
    loaders.group.clear_all()
    group = await loaders.group.load(group_name)
    if not has_arm:
        assert not group
    else:
        assert group
        assert group.state.type == subscription
        assert group.state.has_machine == has_machine
        assert group.state.has_squad == has_squad
        assert group.state.justification == GroupStateJustification.NONE
        assert group.state.tier == tier
    assert "errors" not in result
    assert "success" in result["data"]["updateGroup"]
    assert result["data"]["updateGroup"]["success"]

    query_result = await get_query_group(email=email, group_name=group_name)
    if bool(group):
        assert group_name in query_result["data"]["group"]["name"]
    else:
        assert "errors" in query_result
        assert (
            query_result["errors"][0]["message"]
            == "Access denied or group not found"
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group")
@pytest.mark.parametrize(
    [
        "email",
        "group_name",
        "group_current_state",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_arm",
        "tier",
    ],
    [
        [
            "admin@gmail.com",
            "group1",
            GroupState(
                has_machine=False,
                has_squad=True,
                managed=GroupManaged["MANAGED"],
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2020-05-20T22:00:00+00:00"
                ),
                service=GroupService.WHITE,
                status=GroupStateStatus.ACTIVE,
                tier=GroupTier.OTHER,
                type=GroupSubscriptionType.CONTINUOUS,
            ),
            GroupService.WHITE,
            GroupSubscriptionType.ONESHOT,
            False,
            False,
            False,
            GroupTier.ONESHOT,
        ],
    ],
)
async def test_update_group_fail_service(
    # pylint: disable=too-many-arguments
    populate: bool,
    email: str,
    group_name: str,
    group_current_state: GroupState,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
    tier: GroupTier,
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.state.type == group_current_state.type
    assert group.state.has_machine == group_current_state.has_machine
    assert group.state.has_squad == group_current_state.has_squad
    assert group.state.justification is None
    assert group.state.tier == group_current_state.tier
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        service=service,
        subscription=subscription,
        has_machine=has_machine,
        has_squad=has_squad,
        has_arm=has_arm,
        tier=tier,
    )

    query_result = await get_query_group(email=email, group_name=group_name)
    if bool(group):
        assert group_name in query_result["data"]["group"]["name"]
    else:
        assert "errors" in query_result
        assert (
            query_result["errors"][0]["message"]
            == "Access denied or group not found"
        )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - OneShot service is no longer provided"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_update_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        service=GroupService.WHITE,
        subscription=GroupSubscriptionType.ONESHOT,
        has_machine=False,
        has_squad=False,
        has_arm=False,
        tier=GroupTier.ONESHOT,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
