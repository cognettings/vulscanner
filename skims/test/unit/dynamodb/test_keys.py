from dynamodb.keys import (
    _build_composite_key,
    _validate_key_words,
    build_key,
)
from dynamodb.types import (
    Facet,
    PrimaryKey,
)
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "template, values, expected",
    [
        (
            "PLATFORM#platform#PACKAGE#pkg_name",
            {
                "platform": "gem",
                "pkg_name": "package_name_1",
            },
            "PLATFORM#gem#PACKAGE#package_name_1",
        ),
        (
            "SOURCE#src#ADVISORY#id",
            {
                "id": "CVE-ADVISORY-1",
                "src": "MANUAL",
            },
            "SOURCE#MANUAL#ADVISORY#CVE-ADVISORY-1",
        ),
    ],
)
def test_build_composite_key(
    template: str, values: dict[str, str], expected: str
) -> None:
    assert _build_composite_key(template=template, values=values) == expected


@pytest.mark.skims_test_group("unittesting")
def test_build_key(
    mocker: MockerFixture,
) -> None:
    facet = Facet(
        attrs=("test",),
        pk_alias="PLATFORM#test",
        sk_alias="SOURCE#test",
    )
    values = {"test": "built"}
    expected = PrimaryKey(
        partition_key="PLATFORM#built",
        sort_key="SOURCE#built",
    )
    mock_build_composite_key = mocker.patch(
        "dynamodb.keys._build_composite_key",
        side_effect=lambda template, values: template.replace(
            "test", values["test"]
        ),
    )
    result = build_key(facet=facet, values=values)
    assert mock_build_composite_key.call_count == 2
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "key, is_valid",
    [
        ("test", True),
        ("test#test", False),
        ("test#test#test", False),
    ],
)
def test_validate_key_words(key: str, is_valid: bool) -> None:
    if is_valid:
        _validate_key_words(key=key)
    else:
        with pytest.raises(ValueError):
            _validate_key_words(key=key)
