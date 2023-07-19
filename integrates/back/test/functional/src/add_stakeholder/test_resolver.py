from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_stakeholder")
async def test_admin(populate: bool) -> None:
    assert populate
    email = "new_user_test@gmail.com"
    role = "USER"
    result: dict[str, Any] = await get_result(email=email, role=role)
    assert "errors" not in result
    assert "addStakeholder" in result["data"]
    assert "success" in result["data"]["addStakeholder"]
    assert result["data"]["addStakeholder"]["success"]
    loaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.email == email


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_stakeholder")
@pytest.mark.parametrize(
    ("email", "role"),
    (
        (
            "customer_manager@gmail.com",
            "CUSTOMER_MANAGER",
        ),
    ),
)
async def test_add_stakeholder_fail(
    populate: bool, email: str, role: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(email=email, role=role)
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Invalid role or not enough permissions to grant role: "
        "customer_manager"
    )
