from .types import (
    ADVISORIES_TEST_DICTS,
    ADVISORIES_TEST_OBJECTS,
)
from custom_exceptions import (
    InvalidPatchItem,
)
import pytest
from s3.model.types import (
    Advisory,
)
from sca_patch import (
    ADD,
    check_item,
    REMOVE,
    UPDATE,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "item,action,expected",
    [
        (
            ADVISORIES_TEST_DICTS[0],
            ADD,
            ADVISORIES_TEST_OBJECTS[0],
        ),
        (
            ADVISORIES_TEST_DICTS[1],
            REMOVE,
            ADVISORIES_TEST_OBJECTS[1],
        ),
    ],
)
def test_check_item(item: dict, action: str, expected: Advisory) -> None:
    result: Advisory = check_item(item, action)
    assert result == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "item,action",
    [
        (
            {
                "associated_advisory": "CVE-ADVISORY-1",
                "package_manager": "gem",
                "vulnerable_version": ">=2.13.0 <2.15.0",
                "source": "MANUAL",
                "severity": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
            },
            ADD,
        ),
        (
            {
                "associated_advisory": "CVE-ADVISORY-1",
                "package_name": "package_name_1",
                "package_manager": "gem",
                "vulnerable_version": ">=2.13.0 <2.15.0",
                "severity": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
            },
            REMOVE,
        ),
        (
            {
                "associated_advisory": "CVE-ADVISORY-1",
                "package_name": "package_name_1",
                "package_manager": "gem",
                "source": "MANUAL",
            },
            UPDATE,
        ),
    ],
)
def test_check_item_error(item: dict, action: str) -> None:
    with pytest.raises(InvalidPatchItem):
        check_item(item, action)
