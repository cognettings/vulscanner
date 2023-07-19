from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Notification,
)
from mailer.utils import (
    get_available_notifications,
    get_group_emails_by_notification,
    get_org_groups,
    get_organization_country,
    get_organization_name,
    get_stakeholder_roles,
)
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "email",
        "expected",
    ],
    [
        [
            "customer_manager@fluidattacks.com",
            [
                Notification.EVENT_REPORT,
                Notification.FILE_UPDATE,
                Notification.GROUP_INFORMATION,
                Notification.NEW_COMMENT,
                Notification.PORTFOLIO_UPDATE,
                Notification.ROOT_UPDATE,
                Notification.SERVICE_UPDATE,
                Notification.UNSUBSCRIPTION_ALERT,
                Notification.UPDATED_TREATMENT,
                Notification.VULNERABILITY_REPORT,
            ],
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_stakeholder_roles",
    new_callable=AsyncMock,
)
async def test_get_available_notifications(
    mock_get_stakeholder_roles: AsyncMock,
    email: str,
    expected: list[Notification],
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_get_stakeholder_roles.return_value = mock_data_for_module(
        mock_path="get_stakeholder_roles",
        mock_args=[email],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    available_notifications = await get_available_notifications(loaders, email)
    assert available_notifications == expected
    assert mock_get_stakeholder_roles.called is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
        "notification",
    ],
    [
        [
            "unittesting",
            "user_unsubscribed",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_stakeholders_email_by_preferences",
    new_callable=AsyncMock,
)
async def test_get_group_emails_by_notification(
    mock_get_stakeholders_email_by_preferences: AsyncMock,
    group_name: str,
    notification: str,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_get_stakeholders_email_by_preferences.return_value = (
        mock_data_for_module(
            mock_path="get_stakeholders_email_by_preferences",
            mock_args=[group_name, notification],
            module_at_test=MODULE_AT_TEST,
        )
    )
    loaders = get_new_context()
    group_emails = await get_group_emails_by_notification(
        loaders=loaders, group_name=group_name, notification=notification
    )
    assert len(group_emails) == 5
    assert mock_get_stakeholders_email_by_preferences.called is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "org_id",
    ],
    [
        [
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.organization_groups",
    new_callable=AsyncMock,
)
async def test_get_org_groups(
    mock_dataloaders_organization_groups: AsyncMock,
    org_id: str,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_dataloaders_organization_groups.load.return_value = (
        mock_data_for_module(
            mock_path="Dataloaders.organization_groups",
            mock_args=[org_id],
            module_at_test=MODULE_AT_TEST,
        )
    )
    loaders = get_new_context()
    org_groups = await get_org_groups(loaders, org_id)
    assert len(org_groups) == 3
    assert mock_dataloaders_organization_groups.load.called is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["group_name", "expected"],
    [
        [
            "unittesting",
            "Colombia",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.organization",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.group",
    new_callable=AsyncMock,
)
async def test_get_organization_country(
    mock_dataloaders_group: AsyncMock,
    mock_dataloaders_organization: AsyncMock,
    group_name: str,
    expected: str,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dataloaders_group.load,
            "Dataloaders.group",
            [group_name],
        ),
        (
            mock_dataloaders_organization.load,
            "Dataloaders.organization",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    org_country = await get_organization_country(loaders, group_name)
    assert org_country == expected
    assert mock_dataloaders_group.load.called is True
    assert mock_dataloaders_organization.load.called is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["group_name", "expected"],
    [
        [
            "unittesting",
            "okada",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.organization",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.group",
    new_callable=AsyncMock,
)
async def test_get_organization_name(
    mock_dataloaders_group: AsyncMock,
    mock_dataloaders_organization: AsyncMock,
    group_name: str,
    expected: str,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dataloaders_group.load,
            "Dataloaders.group",
            [group_name],
        ),
        (
            mock_dataloaders_organization.load,
            "Dataloaders.organization",
            [group_name],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    org_name = await get_organization_name(loaders, group_name)
    assert org_name == expected
    assert mock_dataloaders_group.load.called is True
    assert mock_dataloaders_organization.load.called is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "expected"],
    [
        [
            "customer_manager@fluidattacks.com",
            dict(group={"customer_manager"}, org={"customer_manager"}),
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "authz.get_group_level_role",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "get_org_groups",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "authz.get_organization_level_role",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_organizations_access",
    new_callable=AsyncMock,
)
async def test_get_stakeholder_roles(  # pylint: disable=too-many-arguments
    mock_dataloaders_stakeholder_organizations_access: AsyncMock,
    mock_authz_get_organization_level_role: AsyncMock,
    mock_get_org_groups: AsyncMock,
    mock_authz_get_group_level_role: AsyncMock,
    email: str,
    expected: dict[str, set[str]],
    mock_data_for_module: Callable,
) -> None:
    mock_dataloaders_stakeholder_organizations_access.load.return_value = (
        mock_data_for_module(
            mock_path="Dataloaders.stakeholder_organizations_access",
            mock_args=[email],
            module_at_test=MODULE_AT_TEST,
        )
    )
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_authz_get_organization_level_role,
            "authz.get_organization_level_role",
            [email],
        ),
        (
            mock_get_org_groups,
            "get_org_groups",
            [email],
        ),
        (
            mock_authz_get_group_level_role,
            "authz.get_group_level_role",
            [email],
        ),
    ]

    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.side_effect = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()
    stakeholder_roles = await get_stakeholder_roles(loaders, email)
    assert stakeholder_roles == expected
    assert (
        mock_dataloaders_stakeholder_organizations_access.load.called is True
    )
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)
