from . import (
    get_root_way1,
    get_root_way2,
    get_root_way3,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_root(populate: bool, email: str) -> None:
    """Test for GetRoot in /front/.../GroupFindingsView/queries.ts"""
    assert populate
    group_name: str = "group1"
    result: dict = await get_root_way1(user=email, group=group_name)
    group = result["data"]["group"]
    roots = group["roots"]
    root_0 = roots[0]
    assert group["name"] == group_name
    assert root_0["id"] == "63298a73-9dff-46cf-b42d-9b2f01a56690"
    assert root_0["nickname"] == ""
    assert root_0["state"] == "ACTIVE"
    assert root_0["__typename"] == "GitRoot"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_root_way2(populate: bool, email: str) -> None:
    """Test for GetRoot in /front/.../GroupScopeView/queries.ts"""
    assert populate
    group_name: str = "group1"
    result: dict = await get_root_way2(user=email, group=group_name)
    group = result["data"]["group"]
    roots = group["roots"]
    root_0 = roots[0]
    cloning_status = root_0["cloningStatus"]
    assert group["name"] == group_name
    assert root_0["branch"] == "master"
    assert root_0["credentials"] is None
    assert root_0["environment"] == "production"
    assert root_0["gitEnvironmentUrls"] == []
    assert root_0["includesHealthCheck"] is True
    assert root_0["url"] == "https://gitlab.com/fluidattacks/universe"
    assert root_0["useVpn"] is False
    assert root_0["createdAt"] == "2020-11-19T13:37:10+00:00"
    assert root_0["createdBy"] == "admin@gmail.com"
    assert root_0["lastEditedAt"] == "2020-11-19T13:37:10+00:00"
    assert root_0["lastEditedBy"] == "admin@gmail.com"
    assert root_0["id"] == "63298a73-9dff-46cf-b42d-9b2f01a56690"
    assert root_0["nickname"] == ""
    assert root_0["state"] == "ACTIVE"
    assert root_0["__typename"] == "GitRoot"
    assert cloning_status["message"] == "root creation"
    assert cloning_status["status"] == "UNKNOWN"
    assert cloning_status["__typename"] == "GitRootCloningStatus"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_root_way3(populate: bool, email: str) -> None:
    """Query for GetRoot in /front/.../GroupScopeView/queries.ts"""
    assert populate
    group_name: str = "group1"
    result: dict = await get_root_way3(user=email, group=group_name)
    group = result["data"]["group"]
    roots = group["roots"]
    root_0 = roots[0]
    assert group["name"] == "group1"
    assert root_0["nickname"] == ""
    assert root_0["state"] == "ACTIVE"
    assert root_0["__typename"] == "GitRoot"
