from db_model.roots.types import (
    RootEnvironmentCloud,
    RootEnvironmentUrl,
    RootEnvironmentUrlType,
)
from decimal import (
    Decimal,
)
import pytest
from reports.pdf import (
    _format_url,
    get_severity,
)


def test_format_url() -> None:
    # first if called
    root_url = RootEnvironmentUrl(
        id="33445", url_type=RootEnvironmentUrlType.URL, url="http://test.com"
    )
    expected_url = "http://test.com"
    assert _format_url(root_url) == expected_url

    # no if called
    root_url2 = RootEnvironmentUrl(id="64563", url="http://test2.com")
    expected_url = "http://test2.com"
    assert _format_url(root_url2) == expected_url

    # second and third if called
    root_url3 = RootEnvironmentUrl(
        id="6453563",
        url_type=RootEnvironmentUrlType.CLOUD,
        url="http://test3.com",
        cloud_name=RootEnvironmentCloud.GCP,
    )
    expected_url = "CLOUD: GCP: http://test3.com"
    assert _format_url(root_url3) == expected_url


@pytest.mark.parametrize(
    ["metric", "metric_value", "expected_result"],
    [
        ["access_vector", "0.395", "Local"],
        ["attack_vector", "0.62", "Red adyacente"],
        ["confidentiality_impact", "0.66", "Completo"],
        ["integrity_impact", "0.0", "Ninguno"],
        ["availability_impact", "0.275", "Parcial"],
        ["authentication", "0.704", "Ninguna"],
        ["exploitability", "1.0", "Alta"],
        ["confidence_level", "0.9", "No confirmado"],
        ["resolution_level", "0.9", "Temporal"],
        ["access_complexity", "0.71", "Bajo"],
    ],
)
def test_get_severity(
    metric: str,
    metric_value: str,
    expected_result: str,
) -> None:
    result = get_severity(metric, Decimal(metric_value))
    assert result == expected_result
