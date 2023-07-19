from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from mailer.events import (
    send_mail_event_report,
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
        "event_id",
        "event_type",
        "description",
        "root_id",
        "reason",
        "other",
        "is_closed",
    ],
    [
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            None,
            None,
            False,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "PROBLEM_SOLVED",
            None,
            True,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "OTHER",
            "Test",
            True,
        ],
    ],
)
@patch(MODULE_AT_TEST + "send_mails_async", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "Dataloaders.root", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "Dataloaders.stakeholder", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "get_group_stakeholders_emails", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "get_organization_name", new_callable=AsyncMock)
async def test_send_event_report(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_get_organization_name: AsyncMock,  # NOSONAR
    mock_get_group_stakeholders_emails: AsyncMock,
    mock_dataloaders_stakeholder: AsyncMock,
    mock_dataloaders_root: AsyncMock,
    mock_send_mails_async: AsyncMock,
    group_name: str,
    event_id: str,
    event_type: str,
    description: str,
    reason: str,
    root_id: str,
    other: str,
    is_closed: bool,
    mock_data_for_module: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_organization_name,
            "get_organization_name",
            [group_name],
        ),
        (
            mock_get_group_stakeholders_emails,
            "get_group_stakeholders_emails",
            [group_name],
        ),
        (
            mock_dataloaders_stakeholder.load_many,
            "Dataloaders.stakeholder",
            [group_name],
        ),
        (
            mock_dataloaders_root.load,
            "Dataloaders.root",
            [group_name, root_id],
        ),
        (
            mock_send_mails_async,
            "send_mails_async",
            [group_name, root_id, event_type, description, reason, event_id],
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
    await send_mail_event_report(
        loaders=get_new_context(),
        group_name=group_name,
        event_id=event_id,
        event_type=event_type,
        description=description,
        root_id=root_id,
        reason=reason,
        other=other,
        is_closed=is_closed,
        report_date=datetime(2022, 6, 16).date(),
    )
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)
