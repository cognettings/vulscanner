from db_model.advisories.get import (
    _get_advisories,
    _get_all_advisories,
    AdvisoriesLoader,
)
from dynamodb.types import (
    PrimaryKey,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from typing import (
    NamedTuple,
)


@pytest.fixture(name="mock_scan_response")
def fixture_scan_response() -> list[dict]:
    return [
        {"title": "Advisory 1"},
        {"title": "Advisory 2"},
        {"title": "Advisory 3"},
    ]


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_get_advisories(mocker: MockerFixture) -> None:
    platform = "npm"
    pkg_name = "gatsby"
    items = (
        {
            "package_name": pkg_name,
            "package_manager": platform,
            "associated_advisory": "CVE-ADVISORY",
            "vulnerable_version": "VERSION",
            "source": "SOURCE",
        },
    )
    mock_build_key = mocker.patch(
        "db_model.advisories.get.keys.build_key",
        return_value=PrimaryKey(
            partition_key=f"PLATFORM#{platform}#PACKAGE#{pkg_name}",
            sort_key="SOURCE#src#ADVISORY#id",
        ),
    )
    mock_query = mocker.patch(
        "db_model.advisories.get.operations.query",
        return_value=mocker.Mock(items=items),
    )
    mock_format_item_to_advisory = mocker.patch(
        "db_model.advisories.get.format_item_to_advisory",
        return_value=Advisory(
            id="CVE-ADVISORY",
            package_name=pkg_name,
            package_manager=platform,
            vulnerable_version="VERSION",
            source="SOURCE",
        ),
    )
    await _get_advisories(platform=platform, package_name=pkg_name)
    assert mock_build_key.call_count == 1
    assert mock_query.call_count == 1
    assert mock_format_item_to_advisory.call_count == len(items)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_get_all_advisories(
    mocker: MockerFixture,
    mock_scan_response: list[dict],
) -> None:
    class AdvisoryTest(NamedTuple):
        title: str

    mock_scan = mocker.patch(
        "db_model.advisories.get.operations.scan",
        return_value=mock_scan_response,
    )
    mock_format_item_to_advisory = mocker.patch(
        "db_model.advisories.get.format_item_to_advisory",
        side_effect=lambda item: AdvisoryTest(item["title"]),
    )
    result = await _get_all_advisories()
    assert mock_scan.call_count == 1
    assert mock_format_item_to_advisory.call_count == 3
    assert len(result) == len(mock_scan_response)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_load_fn(
    mocker: MockerFixture,
) -> None:
    mock_get_advisories = mocker.patch(
        "db_model.advisories.get._get_advisories",
    )
    ad_keys = (
        ("gem", "rails"),
        ("npm", "gatsby"),
    )
    result = await AdvisoriesLoader().batch_load_fn(ad_keys)
    assert mock_get_advisories.call_args_list == [
        ({"platform": "gem", "package_name": "rails"},),
        ({"platform": "npm", "package_name": "gatsby"},),
    ]
    assert len(result) == len(ad_keys)
