from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_group_consult(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_group_consult_with_suppress(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_add_group_consult_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_group_consult_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group3"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
