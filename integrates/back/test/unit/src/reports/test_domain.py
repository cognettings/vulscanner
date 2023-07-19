from back.test.unit.src.utils import (
    get_module_at_test,
)
import pytest
from reports.domain import (
    get_toe_lines_report,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(MODULE_AT_TEST + "get_group_toe_lines_report", new_callable=AsyncMock)
async def test_get_toe_lines_report(
    mock_get_group_toe_lines_report: AsyncMock,
) -> None:
    group_name = "fluid_group"
    email = "fluid@test.com"

    mock_get_group_toe_lines_report.return_value = "string_tested"

    result = await get_toe_lines_report(group_name=group_name, email=email)

    assert result == mock_get_group_toe_lines_report.return_value
