import pytest
from s3.model.types import (
    Advisory,
)
from schedulers.update_sca_table import (
    fix_advisory,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "parameter,expected",
    [
        (
            Advisory(
                id="CVE-ADVISORY-1",
                package_manager="gem",
                package_name="package_name_1",
                severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                source="https://github.com/github/advisory-database.git",
                vulnerable_version=">=0 || >=2.4.0 <2.12.2",
            ),
            Advisory(
                id="CVE-ADVISORY-1",
                package_manager="gem",
                package_name="package_name_1",
                severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                source="https://github.com/github/advisory-database.git",
                vulnerable_version=">=2.4.0 <2.12.2",
            ),
        ),
        (
            Advisory(
                id="CVE-ADVISORY-2",
                package_manager="go",
                package_name="package_name_2",
                severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                source="MANUAL",
                vulnerable_version=">=0 <2.4.0 || >2.5.4 <=2.6.3",
            ),
            Advisory(
                id="CVE-ADVISORY-2",
                package_manager="go",
                package_name="package_name_2",
                severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                source="MANUAL",
                vulnerable_version=">=0 <2.4.0 || >2.5.4 <=2.6.3",
            ),
        ),
    ],
)
def test_fix_advisory(parameter: Advisory, expected: Advisory) -> None:
    formated_range: Advisory = fix_advisory(parameter)
    assert formated_range == expected
