# pylint: disable=too-many-arguments
from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.toe_inputs.types import (
    ToeInputRequest,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "root_id", "component", "entry_point", "be_present"],
    [
        [
            "admin@fluidattacks.com",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "https://test.com/test",
            "idTest",
            True,
        ],
        [
            "admin@fluidattacks.com",
            "63298a73-9dff-46cf-b42d-9b2f01a56690",
            "https://test.com/test",
            "idTest",
            False,
        ],
    ],
)
async def test_update_toe_input(
    populate: bool,
    email: str,
    root_id: str,
    component: str,
    entry_point: str,
    be_present: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateToeInput"]
    assert result["data"]["updateToeInput"]["success"]
    loaders = get_new_context()
    toe_input = await loaders.toe_input.load(
        ToeInputRequest(
            component=component,
            entry_point=entry_point,
            group_name=group_name,
            root_id=root_id,
        )
    )
    assert toe_input
    assert toe_input.state.be_present == be_present


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "root_id", "component", "entry_point", "be_present"],
    [
        [
            "admin@fluidattacks.com",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1e",
            "https://app.fluidattacks.com:8080/test/fail",
            "-",
            True,
        ],
    ],
)
async def test_update_toe_input_fail_2(
    populate: bool,
    email: str,
    root_id: str,
    component: str,
    entry_point: str,
    be_present: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Toe input has not been found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.mark.parametrize(
    ["email", "root_id", "component", "entry_point", "be_present"],
    [
        [
            "user@gmail.com",
            "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "https://app.fluidattacks.com:8080/test",
            "-",
            True,
        ],
    ],
)
async def test_update_toe_input_fail_3(
    populate: bool,
    email: str,
    root_id: str,
    component: str,
    entry_point: str,
    be_present: bool,
) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        be_present=be_present,
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
