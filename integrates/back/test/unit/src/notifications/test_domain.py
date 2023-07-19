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
from notifications.domain import (
    _get_recipient_first_name_async,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email", "expected_first_name"],
    [
        ["integratesuser@gmail.com", "Integrates"],
        ["forces.unittesting@fluidattacks.com", "forces.unittesting"],
    ],
)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder",
    new_callable=AsyncMock,
)
async def test_recipient_first_name(
    mock_dataloaders_stakeholder: AsyncMock,
    email: str,
    expected_first_name: str,
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_dataloaders_stakeholder.load.return_value = mock_data_for_module(
        mock_path="Dataloaders.stakeholder",
        mock_args=[email],
        module_at_test=MODULE_AT_TEST,
    )
    loaders: Dataloaders = get_new_context()
    result = await _get_recipient_first_name_async(loaders, email)
    assert result == expected_first_name
    assert mock_dataloaders_stakeholder.load.called is True
