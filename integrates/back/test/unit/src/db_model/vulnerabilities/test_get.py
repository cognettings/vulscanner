from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.get import (
    FindingVulnerabilitiesLoader,
    FindingVulnerabilitiesNonDeletedLoader,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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
    ["finding_ids", "expected_vulns"],
    [[["436992569", "422286126", "560175507"], [28, 2, 0]]],
)
@patch(MODULE_AT_TEST + "_get_finding_vulnerabilities", new_callable=AsyncMock)
async def test_finding_vulnerabilities_loader(
    mock__get_finding_vulnerabilities: AsyncMock,
    mocked_data_for_module: Callable,
    finding_ids: list[str],
    expected_vulns: list[int],
) -> None:
    mock__get_finding_vulnerabilities.side_effect = mocked_data_for_module(
        mock_path="_get_finding_vulnerabilities",
        mock_args=[finding_ids],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context().finding_vulnerabilities_all
    assert isinstance(loaders, FindingVulnerabilitiesLoader)
    vulnerabilities = await loaders.load_many(finding_ids)

    for vulns, total_vulns in zip(vulnerabilities, expected_vulns):
        assert len(vulns) == total_vulns
    assert mock__get_finding_vulnerabilities.call_count == 3


@pytest.mark.parametrize(
    ["finding_ids"],
    [[["436992569", "422286126", "560175507"]]],
)
@patch(
    MODULE_AT_TEST + "FindingVulnerabilitiesLoader.load_many",
    new_callable=AsyncMock,
)
async def test_finding_vulnerabilities_non_deleted_loader(
    mock_finding_vulnerabilities_non_deleted_loader: AsyncMock,
    mocked_data_for_module: Callable,
    finding_ids: list[str],
) -> None:
    mock_finding_vulnerabilities_non_deleted_loader.return_value = (
        mocked_data_for_module(
            mock_path="FindingVulnerabilitiesLoader.load_many",
            mock_args=[finding_ids],
            module_at_test=MODULE_AT_TEST,
        )
    )
    loaders = get_new_context().finding_vulnerabilities
    assert isinstance(loaders, FindingVulnerabilitiesNonDeletedLoader)
    vulnerabilities = await loaders.load_many_chained(finding_ids)

    assert vulnerabilities
    assert isinstance(vulnerabilities, list)
    assert len(vulnerabilities) == 30
    assert isinstance(vulnerabilities[0], Vulnerability)
    assert mock_finding_vulnerabilities_non_deleted_loader.called is True
