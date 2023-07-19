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
from mailer.common import (
    get_recipient_first_name,
    get_recipients,
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


@pytest.mark.parametrize(
    ["email", "is_access_granted", "expected_output"],
    [
        ["nonexistinguser@fluidattacks.com", False, None],
        ["integratesmanager@gmail.com", False, "Integrates"],
        ["nonexistinguser@fluidattacks.com", True, "nonexistinguser"],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder",
    new_callable=AsyncMock,
)
async def test_get_recipient_first_name(
    mock_dataloaders_stakeholder: AsyncMock,
    email: str,
    is_access_granted: bool,
    expected_output: str | None,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_dataloaders_stakeholder.load.return_value = mock_data_for_module(
        mock_path="Dataloaders.stakeholder",
        mock_args=[email],
        module_at_test=MODULE_AT_TEST,
    )
    loaders: Dataloaders = get_new_context()
    assert (
        await get_recipient_first_name(loaders, email, is_access_granted)
        == expected_output
    )
    assert mock_dataloaders_stakeholder.load.called is True


@pytest.mark.parametrize(
    [
        "email_to",
        "email_cc",
        "first_name",
        "is_access_granted",
        "expected_result",
    ],
    [
        [
            "integratesmanager@gmail.com",
            ["nonexisting@nonexisting.com"],
            "Integrates",
            False,
            [
                {
                    "email": "integratesmanager@gmail.com",
                    "name": "Integrates",
                    "type": "to",
                }
            ],
        ],
        [
            "integratesmanager@gmail.com",
            ["unittest@fluidattacks.com"],
            "Integrates",
            False,
            [
                {
                    "email": "integratesmanager@gmail.com",
                    "name": "Integrates",
                    "type": "to",
                },
                {
                    "email": "unittest@fluidattacks.com",
                    "name": "Miguel",
                    "type": "cc",
                },
            ],
        ],
        [
            "integratesmanager@gmail.com",
            None,
            "Integrates",
            False,
            [
                {
                    "email": "integratesmanager@gmail.com",
                    "name": "Integrates",
                    "type": "to",
                }
            ],
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_recipient_first_name",
    new_callable=AsyncMock,
)
async def test_get_recipients(
    # pylint: disable=too-many-arguments
    mock_get_recipient_first_name: AsyncMock,
    email_to: str,
    email_cc: list[str] | None,
    first_name: str,
    is_access_granted: bool,
    expected_result: list[dict[str, Any]],
    mock_data_for_module: Callable,
) -> None:
    if email_cc:
        # Set up mock's result using mock_data_for_module fixture
        for email in email_cc:
            mock_get_recipient_first_name.return_value = mock_data_for_module(
                mock_path="get_recipient_first_name",
                mock_args=[email],
                module_at_test=MODULE_AT_TEST,
            )
    loaders: Dataloaders = get_new_context()
    assert (
        await get_recipients(
            loaders=loaders,
            email_to=email_to,
            email_cc=email_cc,
            first_name=first_name,
            is_access_granted=is_access_granted,
        )
        == expected_result
    )
    if email_cc:
        assert mock_get_recipient_first_name.called is True
