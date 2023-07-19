from back.test.unit.src.utils import (
    get_module_at_test,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import datetime
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings.types import (
    SeverityLevelsInfo,
    SeverityLevelSummary,
)
import pytest
from reports.certificate import (
    _set_percentage,
    format_finding,
    resolve_month_name,
)
from reports.types import (
    CertFindingInfo,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "findings_domain.get_severity_levels_info",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "findings_domain.get_total_open_cvssf",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "findings_domain.get_open_vulnerabilities_len",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "findings_domain.get_closed_vulnerabilities_len",
    new_callable=AsyncMock,
)
async def test_format_finding(
    mock_fin_dom_get_closed_vulnerabilities_len: AsyncMock,
    mock_fin_dom_get_open_vulnerabilities_len: AsyncMock,
    mock_fin_dom_get_total_open_cvssf: AsyncMock,
    mock_findings_domain_get_severity_levels_info: AsyncMock,
) -> None:
    level_test = SeverityLevelsInfo(
        critical=SeverityLevelSummary(0, 1, 2),
        high=SeverityLevelSummary(0, 1, 3),
        medium=SeverityLevelSummary(0, 1, 4),
        low=SeverityLevelSummary(0, 1, 5),
    )
    mock_fin_dom_get_closed_vulnerabilities_len.return_value = 10
    mock_fin_dom_get_open_vulnerabilities_len.return_value = 15
    mock_fin_dom_get_total_open_cvssf.return_value = Decimal("128.0")
    mock_findings_domain_get_severity_levels_info.return_value = level_test

    closed_vulnerabilities = (
        mock_fin_dom_get_closed_vulnerabilities_len.return_value
    )
    open_vulnerabilities = (
        mock_fin_dom_get_open_vulnerabilities_len.return_value
    )
    risk_exposure = mock_fin_dom_get_total_open_cvssf.return_value
    severity_levels = (
        mock_findings_domain_get_severity_levels_info.return_value
    )

    loaders: Dataloaders = get_new_context()
    finding = MagicMock(spec=Finding)
    finding.title = "title_tested"

    result = await format_finding(loaders, finding)

    expected_result = CertFindingInfo(
        closed_vulnerabilities=closed_vulnerabilities,
        open_vulnerabilities=open_vulnerabilities,
        risk_exposure=risk_exposure,
        severity_levels=severity_levels,
    )

    assert result == expected_result


def test_set_percentage() -> None:
    assert _set_percentage(10, 10) == "100%"
    assert _set_percentage(10, 5) == "50%"
    assert _set_percentage(6, 5) == "83.3%"
    assert _set_percentage(0, 0) == "N/A"
    assert _set_percentage(0, 5) == "N/A"
    assert _set_percentage(10, 0) == "0%"


def test_resolve_month_name() -> None:
    lang = "en"
    date = datetime.datetime(2020, 11, 5)
    words = {"test": "test_value"}
    assert resolve_month_name(lang, date, words) == "November"

    lang = "es"
    date = datetime.datetime(2020, 11, 5)
    words = {"november": "test_november"}
    assert resolve_month_name(lang, date, words) == "test_november"
