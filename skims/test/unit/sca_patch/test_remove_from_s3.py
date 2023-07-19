from .types import (
    ADVISORIES_TEST_OBJECTS,
)
import pytest
from s3.model.types import (
    Advisory,
)
from sca_patch import (
    remove_from_s3,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "adv, expected",
    [
        (
            ADVISORIES_TEST_OBJECTS[0],
            {
                "gem": {
                    "package_name_1": {
                        "CVE-ADVISORY-3": "1.1.0",
                    }
                },
                "npm": {
                    "package_name_2": {
                        "CVE-ADVISORY-2": "<2.15.0",
                    }
                },
            },
        ),
        (
            ADVISORIES_TEST_OBJECTS[1],
            {
                "gem": {
                    "package_name_1": {
                        "CVE-ADVISORY-1": ">=2.13.0 <2.15.0",
                        "CVE-ADVISORY-3": "1.1.0",
                    }
                },
                "npm": {},
            },
        ),
    ],
)
def test_remove_from_s3(adv: Advisory, expected: dict[str, dict]) -> None:
    s3_advisories: dict = {
        "gem": {
            "package_name_1": {
                "CVE-ADVISORY-1": ">=2.13.0 <2.15.0",
                "CVE-ADVISORY-3": "1.1.0",
            }
        },
        "npm": {
            "package_name_2": {
                "CVE-ADVISORY-2": "<2.15.0",
            }
        },
    }

    remove_from_s3(adv, s3_advisories)
    assert s3_advisories == expected
