from back.test.unit.src.utils import (
    get_module_at_test,
)
from datetime import (
    datetime,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderState,
    StakeholderTours,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers.remove_inactive_stakeholders import (
    process_stakeholder,
    remove_inactive_stakeholders,
)
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


@freeze_time("2021-04-01T00:00:00+00:00")
@pytest.mark.parametrize(
    ["stakeholder"],
    [
        [
            Stakeholder(
                email="unittest@fluidattacks.com",
                enrolled=True,
                first_name="Miguel",
                is_concurrent_session=False,
                is_registered=True,
                last_login_date=datetime.fromisoformat(
                    "2020-12-31T18:40:37+00:00"
                ),
                last_name="de Orellana",
                legal_remember=True,
                phone=None,
                registration_date=datetime.fromisoformat(
                    "2019-02-28T16:54:12+00:00"
                ),
                role="admin",
                session_key=None,
                session_token=None,
                state=StakeholderState(
                    modified_by=None,
                    modified_date=None,
                    notifications_preferences=NotificationsPreferences(
                        available=[],
                        email=[],
                        sms=[],
                        parameters=NotificationsParameters(
                            min_severity=Decimal("3.0")
                        ),
                    ),
                ),
                tours=StakeholderTours(
                    new_group=False,
                    new_root=False,
                    new_risk_exposure=False,
                    welcome=False,
                ),
            )
        ],
    ],
)
@patch(MODULE_AT_TEST + "stakeholders_domain.remove", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_organizations_access",
    new_callable=AsyncMock,
)
async def test_process_stakeholder(
    mock_dataloaders_stakeholder_organizations_access: AsyncMock,
    mock_stakeholders_domain_remove: AsyncMock,
    stakeholder: Stakeholder,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dataloaders_stakeholder_organizations_access.load,
            "Dataloaders.stakeholder_organizations_access",
            [stakeholder.email],
        ),
        (
            mock_stakeholders_domain_remove,
            "stakeholders_domain.remove",
            [stakeholder.email],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    await process_stakeholder(stakeholder)
    mock_dataloaders_stakeholder_organizations_access.load.assert_called_with(
        stakeholder.email
    )
    mock_stakeholders_domain_remove.assert_called_with(stakeholder.email)


@patch(MODULE_AT_TEST + "process_stakeholder", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "stakeholders_model.get_all_stakeholders",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "process_organization", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "orgs_model.get_all_organizations", new_callable=AsyncMock
)
async def test_remove_inactive_stakeholders_(
    mock_orgs_model_get_all_organizations: AsyncMock,
    mock_process_organization: AsyncMock,
    mock_stakeholders_model_get_all_stakeholders: AsyncMock,
    mock_process_stakeholder: AsyncMock,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_orgs_model_get_all_organizations,
            "orgs_model.get_all_organizations",
            [],
        ),
        (
            mock_stakeholders_model_get_all_stakeholders,
            "stakeholders_model.get_all_stakeholders",
            [],
        ),
    ]
    mocks_setup_list_se: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_process_organization,
            "process_organization",
            [],
        ),
        (
            mock_process_stakeholder,
            "process_stakeholder",
            [],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    for item in mocks_setup_list_se:
        mock, path, arguments = item
        mock.side_effect = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    await remove_inactive_stakeholders()
    assert mock_orgs_model_get_all_organizations.called is True
    assert mock_stakeholders_model_get_all_stakeholders.called is True
    assert mock_process_organization.call_count == 11
    assert mock_process_stakeholder.call_count == 7
