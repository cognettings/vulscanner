from authz import (
    get_group_level_actions_by_role,
    get_organization_level_actions_by_role,
    get_user_level_actions_by_role,
)
from authz.boundary import (
    get_group_level_actions,
    get_organization_level_actions,
    get_user_level_actions,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

# Constants

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]

TABLE_NAME = "integrates_vms"


@pytest.mark.parametrize(
    ["email", "role"],
    [
        ["continuoushacking@gmail.com", "hacker"],
        ["integratesuser2@gmail.com", "user"],
        ["integrateshacker@fluidattacks.com", "hacker"],
    ],
)
@patch(MODULE_AT_TEST + "get_user_level_enforcer", new_callable=AsyncMock)
async def test_get_user_level_actions(
    mock_get_user_level_enforcer: AsyncMock,
    email: str,
    role: str,
    side_effect_get_user_level_enforcer: Callable[[Dataloaders, str], bool],
) -> None:
    # Set up mock's side_effect using side_effect_get_user_level_enforcer
    # fixture
    mock_get_user_level_enforcer.side_effect = (
        side_effect_get_user_level_enforcer
    )

    loaders: Dataloaders = get_new_context()

    assert await get_user_level_actions(
        loaders, email
    ) == get_user_level_actions_by_role(role)
    assert mock_get_user_level_enforcer.called is True


@pytest.mark.parametrize(
    ["email", "group", "role"],
    [
        ["continuoushacking@gmail.com", "UnItTeStInG", "user_manager"],
        ["continuoushacking@gmail.com", "unittesting", "user_manager"],
        ["continuoushacking@gmail.com", "oneshottest", "user_manager"],
        ["integrateshacker@fluidattacks.com", "unittesting", "hacker"],
        ["integrateshacker@fluidattacks.com", "oneshottest", "reattacker"],
        ["integratesuser@gmail.com", "unittesting", "user_manager"],
        ["integratesuser@gmail.com", "oneshottest", "user"],
    ],
)
@patch(MODULE_AT_TEST + "get_group_level_enforcer", new_callable=AsyncMock)
async def test_get_group_level_actions(
    mock_get_group_level_enforcer: AsyncMock,
    email: str,
    group: str,
    role: str,
    side_effect_get_group_level_enforcer: Callable[[str, str], bool],
) -> None:
    # Set up mock's side_effect using side_effect_get_group_level_enforcer
    # fixture
    mock_get_group_level_enforcer.side_effect = (
        side_effect_get_group_level_enforcer
    )

    loaders: Dataloaders = get_new_context()
    group_level_actions = await get_group_level_actions(loaders, email, group)
    expected_actions = get_group_level_actions_by_role(role)
    assert group_level_actions == expected_actions
    assert mock_get_group_level_enforcer.called is True


@pytest.mark.parametrize(
    ["email", "organization_id", "organization_level_role"],
    [
        [
            "org_testgroupmanager1@gmail.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "customer_manager",
        ],
        [
            "unittest2@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "customer_manager",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_organization_level_enforcer", new_callable=AsyncMock
)
async def test_get_organization_level(
    mock_get_organization_level_enforcer: AsyncMock,
    email: str,
    organization_id: str,
    organization_level_role: str,
    side_effect_get_organization_level_enforcer: Callable[[str, str], bool],
) -> None:
    # Set up mock's side_effect using side_effect_get_group_level_enforcer
    # fixture
    mock_get_organization_level_enforcer.side_effect = (
        side_effect_get_organization_level_enforcer
    )

    loaders: Dataloaders = get_new_context()
    organization_level_actions = await get_organization_level_actions(
        loaders, email, organization_id
    )

    expected_actions = get_organization_level_actions_by_role(
        organization_level_role
    )
    assert organization_level_actions == expected_actions
    assert mock_get_organization_level_enforcer.called is True
