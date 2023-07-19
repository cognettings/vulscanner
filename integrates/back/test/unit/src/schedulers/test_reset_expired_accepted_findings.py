from back.test.unit.src.utils import (
    get_module_at_test,
)
from dataloaders import (
    get_new_context,
)
import pytest
from schedulers.reset_expired_accepted_findings import (
    process_group,
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


@pytest.mark.parametrize(
    ["group_name", "progress"],
    [["lubbock", 0.0]],
)
@patch(MODULE_AT_TEST + "process_finding", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.group_findings",
    new_callable=AsyncMock,
)
async def test_process_group(
    mock_loaders_group_findings: AsyncMock,
    mock_process_finding: AsyncMock,
    group_name: str,
    progress: float,
    mocked_data_for_module: Any,
) -> None:
    # Set up mock's result using mocked_data_for_module fixture
    mock_loaders_group_findings.load.return_value = mocked_data_for_module(
        mock_path="Dataloaders.group_findings",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )

    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    mock_process_finding.side_effect = mocked_data_for_module(
        mock_path="process_finding",
        mock_args=[group_name],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    await process_group(
        loaders=loaders, group_name=group_name, progress=progress
    )
    assert mock_loaders_group_findings.load.called is True
    assert mock_process_finding.called is True
