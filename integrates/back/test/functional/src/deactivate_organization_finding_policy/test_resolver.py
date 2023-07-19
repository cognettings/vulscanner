from . import (
    get_result,
)
from custom_exceptions import (
    PolicyAlreadyHandled,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id"),
    (
        ("f3f19b09-00e5-4bc7-b9ea-9999c9fe9f87"),
        ("3be367f9-b06c-4f72-ab77-38268045a8ff"),
    ),
)
async def test_deactivate_organization_finding_policy(
    populate: bool, finding_policy_id: str
) -> None:
    assert populate
    result = await get_result(
        email="user_manager@fluidattacks.com",
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" not in result
    assert result["data"]["deactivateOrganizationFindingPolicy"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id"),
    (("dd63f2df-522d-4bfa-ad85-837832c71164"),),
)
async def test_deactivate_organization_finding_policy_fail_1(
    populate: bool, finding_policy_id: str
) -> None:
    assert populate
    result = await get_result(
        email="user_manager@fluidattacks.com",
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(PolicyAlreadyHandled())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_organization_finding_policy")
@pytest.mark.parametrize(
    ("finding_policy_id"),
    (
        ("f3f19b09-00e5-4bc7-b9ea-9999c9fe9f87"),
        ("3be367f9-b06c-4f72-ab77-38268045a8ff"),
    ),
)
@pytest.mark.parametrize(
    ("email"),
    (
        ("user@gmail.com"),
        ("hacker@gmail.com"),
        ("reattacker@gmail.com"),
        ("reviewer@gmail.com"),
        ("vulnerability_manager@fluidattacks.com"),
    ),
)
async def test_deactivate_organization_finding_policy_fail_2(
    populate: bool, finding_policy_id: str, email: str
) -> None:
    assert populate
    result = await get_result(
        email=email,
        organization_name="orgtest",
        finding_policy_id=finding_policy_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
