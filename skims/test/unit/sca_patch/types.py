from s3.model.types import (
    Advisory,
)

SCA_PATCH: str = "sca_patch"
ADVISORIES_TEST_DICTS: tuple[dict, dict] = (
    {
        "associated_advisory": "CVE-ADVISORY-1",
        "package_name": "package_name_1",
        "package_manager": "gem",
        "vulnerable_version": ">=2.13.0 <2.15.0",
        "source": "example_source",
        "severity": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
    },
    {
        "associated_advisory": "CVE-ADVISORY-2",
        "package_name": "package_name_2",
        "package_manager": "npm",
        "vulnerable_version": "<2.15.0",
        "source": "MANUAL",
        "severity": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
    },
)
ADVISORIES_TEST_OBJECTS: tuple[Advisory, Advisory] = (
    Advisory(
        id="CVE-ADVISORY-1",
        package_manager="gem",
        package_name="package_name_1",
        source="MANUAL",
        vulnerable_version=">=2.13.0 <2.15.0",
        severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
    ),
    Advisory(
        id="CVE-ADVISORY-2",
        package_manager="npm",
        package_name="package_name_2",
        source="MANUAL",
        vulnerable_version="<2.15.0",
        severity="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
    ),
)
