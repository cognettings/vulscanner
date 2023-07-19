from custom_exceptions import (
    _SingleMessageException,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from db_model.advisories.utils import (
    _check_severity,
    _check_versions,
    format_advisory,
    format_item_to_advisory,
    print_exc,
)
from dynamodb.types import (
    Item,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "item, expected_advisory",
    [
        (
            {
                "associated_advisory": "ADV-001",
                "package_name": "package1",
                "package_manager": "npm",
                "vulnerable_version": "1.0.0",
                "severity": "high",
                "source": "SOURCE",
                "created_at": "2021-01-01",
                "modified_at": "2021-02-01",
                "cwe_ids": ["CWE-123", "CWE-456"],
            },
            Advisory(
                id="ADV-001",
                package_name="package1",
                package_manager="npm",
                vulnerable_version="1.0.0",
                severity="high",
                source="SOURCE",
                created_at="2021-01-01",
                modified_at="2021-02-01",
                cwe_ids=["CWE-123", "CWE-456"],
            ),
        ),
        (
            {
                "associated_advisory": "ADV-002",
                "package_name": "package2",
                "package_manager": "npm",
                "vulnerable_version": "2.0.0",
                "severity": "low",
                "source": "MANUAL",
            },
            Advisory(
                id="ADV-002",
                package_name="package2",
                package_manager="npm",
                vulnerable_version="2.0.0",
                severity="low",
                source="MANUAL",
            ),
        ),
    ],
)
def test_format_item_to_advisory(
    item: Item,
    expected_advisory: Advisory,
) -> None:
    result = format_item_to_advisory(item)
    assert result == expected_advisory


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "severity, source, expected_result",
    [
        (None, "SOURCE", True),
        (None, PATCH_SRC, False),
        ("CVSS:2.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N", "SOURCE", False),
        ("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N", "SOURCE", True),
        ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N", "SOURCE", False),
        ("CVSS:3.1/AV:N/AC:L/BAD:N/UI:N/S:C/C:L/I:N/A:N", "SOURCE", False),
    ],
)
def test_check_severity(
    severity: str | None,
    source: str,
    expected_result: bool,
) -> None:
    result = _check_severity(severity, source)
    assert result == expected_result


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "versions, expected",
    [
        ("=1.0.0", True),
        (">=0 <1.2.14", True),
        (">=2.3.0-rc1 <2.7.7", True),
        (">=0 <2.7.9.3 || >=2.8.0 <2.8.11.1 || >=2.9.0 <2.9.5", True),
        ("<=1.0.0 || >=2.0.0", True),
        ("=2.0.0 || >=1.2wer.4 <1.3.5", False),
        ("invalid || =2.0.0", False),
        ("<=1.0.0we", False),
        ("", False),
        ("=1.2.3-alpha.1+build.20230524", True),
    ],
)
def test_check_versions(
    versions: str,
    expected: bool,
) -> None:
    result = _check_versions(versions)
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "exc, action, advisory, attr",
    [
        (
            InvalidSeverity,
            "processed",
            Advisory(
                package_manager="npm",
                package_name="package1",
                source="source",
                id="ADV-001",
                vulnerable_version="1.0.0",
            ),
            "attr1",
        ),
        (
            InvalidVulnerableVersion,
            "found",
            Advisory(
                package_manager="pip",
                package_name="package2",
                source="source",
                id="ADV-002",
                vulnerable_version="1.0.0",
            ),
            "attr2",
        ),
    ],
)
def test_print_exc(
    mocker: MockerFixture,
    exc: InvalidSeverity | InvalidVulnerableVersion,
    action: str,
    advisory: Advisory,
    attr: str,
) -> None:
    log_message = (
        "Advisory PLATFORM#%s#PACKAGE#%s SOURCE#%s#ADVISORY#%s "
        "wasn't %s. %s%s"
    )
    mock_log_blocking = mocker.patch("db_model.advisories.utils.log_blocking")
    print_exc(exc, action, advisory, attr)
    log_args = mock_log_blocking.call_args.args
    assert log_args == (
        "warning",
        log_message,
        advisory.package_manager,
        advisory.package_name,
        advisory.source,
        advisory.id,
        action,
        mocker.ANY,
        attr,
    )
    assert isinstance(log_args[7], _SingleMessageException)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "advisory, is_update, checked, expected_result",
    [
        (
            Advisory(
                id="ADV-001",
                package_name="Package1",
                package_manager="NPM",
                vulnerable_version="1.0.0-RC",
                severity="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N",
                source="source",
                created_at="2021-01-01",
                modified_at=None,
                cwe_ids=["CWE-123", "CWE-456"],
            ),
            True,
            True,
            Advisory(
                id="ADV-001",
                package_name="package1",
                package_manager="npm",
                vulnerable_version="1.0.0-rc",
                severity="valid_severity",
                source="source",
                created_at="2021-01-01",
                modified_at="<current_date>",
                cwe_ids=["CWE-123", "CWE-456"],
            ),
        ),
        (
            Advisory(
                id="ADV-002",
                package_name="package2",
                package_manager="npm",
                vulnerable_version="2.0.0",
                severity="invalid",
                source=PATCH_SRC,
                created_at="2022-01-01",
                modified_at="2022-02-01",
                cwe_ids=["CWE-789"],
            ),
            False,
            False,
            None,
        ),
        (
            Advisory(
                id="ADV-002",
                package_name="package2",
                package_manager="npm",
                vulnerable_version="invalid",
                severity="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N",
                source=PATCH_SRC,
                created_at="2022-01-01",
                modified_at="2022-02-01",
                cwe_ids=["CWE-789"],
            ),
            False,
            False,
            None,
        ),
        (
            Advisory(
                id="ADV-002",
                package_name="package2",
                package_manager="npm",
                vulnerable_version="2.0.0",
                severity="invalid",
                source="source",
                created_at=None,
                modified_at=None,
                cwe_ids=["CWE-789"],
            ),
            False,
            False,
            Advisory(
                id="ADV-002",
                package_name="package2",
                package_manager="npm",
                vulnerable_version="2.0.0",
                severity=None,
                source="source",
                created_at="<current_date>",
                modified_at=None,
                cwe_ids=["CWE-789"],
            ),
        ),
    ],
)
def test_format_advisory(
    mocker: MockerFixture,
    advisory: Advisory,
    is_update: bool,
    checked: bool,
    expected_result: Advisory | None,
) -> None:
    def _check_valid(attr: str | None) -> bool:
        return attr != "invalid"

    mock_check_versions = mocker.patch(
        "db_model.advisories.utils._check_versions",
        return_value=_check_valid(advisory.vulnerable_version),
    )
    mock_check_severity = mocker.patch(
        "db_model.advisories.utils._check_severity",
        return_value=_check_valid(advisory.severity),
    )
    mock_datetime = mocker.patch(
        "db_model.advisories.utils.datetime",
    )
    mock_datetime.now.return_value = "<current_date>"
    mocker.patch(
        "db_model.advisories.utils.remove_last_slash",
        return_value="valid_severity",
    )
    try:
        result = format_advisory(advisory, is_update, checked)
    except (InvalidVulnerableVersion, InvalidSeverity):
        result = None
    if not checked:
        assert mock_check_versions.call_count == 1
        if mock_check_versions.return_value:
            assert mock_check_severity.call_count == 1
    assert mock_datetime.now.call_count == int(bool(result))
    assert result == expected_result
