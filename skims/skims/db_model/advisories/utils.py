from custom_exceptions import (
    _SingleMessageException,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from datetime import (
    datetime,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from dynamodb.types import (
    Item,
)
from s3.model.types import (
    Advisory,
)
from semantic_version import (
    NpmSpec,
)
from semver_match_tools.semver_match import (
    coerce_range,
)
from utils.lists import (
    remove_last_slash,
)
from utils.logs import (
    log_blocking,
)

VALID_RANGES = ("=", "<", ">", ">=", "<=")
CVSS_BASE_METRICS: dict[str, tuple[str, ...]] = {
    "AV": ("N", "A", "L", "P"),
    "AC": ("L", "H"),
    "PR": ("N", "L", "H"),
    "UI": ("N", "R"),
    "S": ("U", "C"),
    "C": ("H", "L", "N"),
    "I": ("H", "L", "N"),
    "A": ("H", "L", "N"),
}


def format_item_to_advisory(item: Item) -> Advisory:
    cve_ids = item.get("associated_advisory")
    if cve_ids is None:
        cve_ids = item["id"]
    return Advisory(
        id=cve_ids,
        package_name=item["package_name"],
        package_manager=item["package_manager"],
        vulnerable_version=item["vulnerable_version"],
        severity=item.get("severity"),
        source=item["source"],
        created_at=item.get("created_at"),
        modified_at=item.get("modified_at"),
        cwe_ids=item.get("cwe_ids"),
    )


def _check_severity(severity: str | None, source: str) -> bool:
    if severity is None:
        if source != PATCH_SRC:
            return True
        return False
    severity_elems = severity.split("/")
    if len(severity_elems) != 9:
        return False
    cvss, ver = severity_elems[0].split(":")
    if (
        cvss != "CVSS"
        or not ver.replace(".", "", 1).isdigit()
        or not ver.startswith("3")
    ):
        return False
    for index, (key, values) in enumerate(CVSS_BASE_METRICS.items(), 1):
        metric, value = severity_elems[index].split(":")
        if metric != key or value not in values:
            return False
    return True


def _check_versions(versions: str) -> bool:
    if not versions:
        return False
    version_list = versions.split(" || ")
    for version_range in version_list:
        range_ver = version_range.split()
        if not all(ver.startswith(VALID_RANGES) for ver in range_ver):
            return False
    try:
        coerced_versions = coerce_range(versions)
        NpmSpec(coerced_versions)
    except ValueError:
        return False

    return True


def format_advisory(
    advisory: Advisory,
    is_update: bool = False,
    checked: bool = False,
) -> Advisory:
    severity = advisory.severity
    vulnerable_version = advisory.vulnerable_version
    source = advisory.source
    if not checked:
        if not _check_versions(vulnerable_version):
            raise InvalidVulnerableVersion()
        if not _check_severity(severity, source):
            if source != PATCH_SRC:
                severity = None
            else:
                raise InvalidSeverity()

    current_date = str(datetime.now())

    return Advisory(
        id=advisory.id,
        package_name=advisory.package_name.lower(),
        package_manager=advisory.package_manager.lower(),
        vulnerable_version=vulnerable_version.lower(),
        severity=remove_last_slash(severity) if severity else None,
        source=source,
        created_at=current_date if (not is_update) else advisory.created_at,
        modified_at=current_date if is_update else None,
        cwe_ids=advisory.cwe_ids,
    )


def print_exc(
    exc: _SingleMessageException,
    action: str,
    advisory: Advisory,
    attr: str = "",
) -> None:
    log_blocking(
        "warning",
        (
            "Advisory PLATFORM#%s#PACKAGE#%s SOURCE#%s#ADVISORY#%s "
            "wasn't %s. %s%s"
        ),
        advisory.package_manager,
        advisory.package_name,
        advisory.source,
        advisory.id,
        action,
        exc.new(),
        attr,
    )
