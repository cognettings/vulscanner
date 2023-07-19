from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_update_organization_stakeholder(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
    )
    assert "errors" not in result
    assert result["data"]["updateOrganizationStakeholder"]["success"]
    assert (
        result["data"]["updateOrganizationStakeholder"]["modifiedStakeholder"][
            "email"
        ]
        == email
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_organization_stakeholder")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_update_organization_stakeholder_fail(
    populate: bool, email: str
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    user_role: str = "USER"
    result: dict[str, Any] = await get_result(
        user=email,
        org=org_id,
        email=email,
        role=user_role,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
