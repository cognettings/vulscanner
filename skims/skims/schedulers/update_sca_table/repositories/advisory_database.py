import glob
import json
from s3.model.types import (
    Advisory,
)
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)

URL_ADVISORY_DATABASE: str = "https://github.com/github/advisory-database.git"
PLATFORMS = {
    "maven": "maven",
    "nuget": "nuget",
    "npm": "npm",
    "pypi": "pip",
    "rubygems": "gem",
    "go": "go",
    "packagist": "composer",
    "pub": "pub",
}


def append_advisories(  # pylint: disable=too-many-arguments
    advisories: list[Advisory],
    current_advisories: dict[str, dict[str, str]],
    vuln_id: str,
    severity: str | None,
    cwe_ids: list[str] | None,
    withdrawn: str | None = None,
) -> None:
    for key_pkg, sub_dict in current_advisories.items():
        advisories.append(
            Advisory(
                id=vuln_id,
                package_manager=PLATFORMS[sub_dict["platform"]],
                package_name=key_pkg,
                severity=severity,
                source=URL_ADVISORY_DATABASE,
                vulnerable_version=sub_dict["version"]
                if withdrawn is None
                else "<0",
                cwe_ids=cwe_ids,
            )
        )


def get_limit(events: list[dict[str, str]], pkg_obj: dict) -> str:
    if len(events) > 1:
        if (fixed := events[1].get("fixed")) is not None:
            return f" <{fixed}"
        if (l_affected := events[1].get("last_affected")) is not None:
            return f" <={l_affected}"
    if (db_specific := pkg_obj.get("database_specific")) and (
        l_version := db_specific.get("last_known_affected_version_range")
    ):
        return f" {l_version.replace(' ', '')}"
    return ""


def get_final_range(final_range: str, str_range: str) -> str:
    if final_range == "":
        return str_range
    return " || ".join((final_range, str_range))


def get_vulnerabilities_ranges(
    # pylint: disable= too-many-arguments, too-many-locals
    affected: list[dict],
    vuln_id: str,
    advisories: list[Advisory],
    severity: str | None,
    cwe_ids: list[str] | None,
    withdrawn: str | None = None,
) -> None:
    current_advisories: dict[str, dict[str, str]] = {}
    for pkg_obj in affected:
        package: dict[str, Any] = pkg_obj.get("package") or {}
        ecosystem: str = str(package.get("ecosystem"))
        if (platform := ecosystem.lower()) not in PLATFORMS:
            continue
        pkg_name: str = str(package.get("name")).lower()
        ranges: list[dict[str, Any]] = pkg_obj.get("ranges") or []
        final_range = ""
        versions: list[str] = pkg_obj.get("versions") or []
        formatted_versions = ["=" + ver for ver in versions]
        if formatted_versions:
            final_range = " || ".join(formatted_versions)
        for range_ver in ranges:
            events: list[dict[str, str]] = range_ver.get("events") or []
            str_range: str
            introduced = f">={events[0].get('introduced')}"
            limit = get_limit(events, pkg_obj)
            str_range = f"{introduced}{limit}".lower()
            final_range = get_final_range(final_range, str_range)
        if pkg_name not in current_advisories:
            current_advisories.update(
                {pkg_name: {"version": final_range, "platform": platform}}
            )
        else:
            cur_range = current_advisories[pkg_name]["version"]
            current_advisories.update(
                {
                    pkg_name: {
                        "version": " || ".join((cur_range, final_range)),
                        "platform": platform,
                    }
                }
            )
    append_advisories(
        advisories,
        current_advisories,
        vuln_id,
        severity,
        cwe_ids,
        withdrawn,
    )


def get_advisory_database(
    advisories: list[Advisory], tmp_dirname: str
) -> None:
    filenames = sorted(
        glob.glob(
            f"{tmp_dirname}/advisories/github-reviewed/**/*.json",
            recursive=True,
        )
    )
    print("processing advisory-database")
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as stream:
            try:
                from_json: dict = json.load(stream)
                withdrawn = from_json.get("withdrawn")
                vuln_id = str(from_json.get("id"))
                affected = from_json.get("affected") or []
                severity: list[dict[str, str]] = (
                    from_json.get("severity") or []
                )
                database_specific = from_json.get("database_specific")
                if database_specific:
                    cwe_ids = database_specific.get("cwe_ids")
                severity_val: str | None = None
                if len(severity) > 0:
                    severity_val = severity[0].get("score")

                get_vulnerabilities_ranges(
                    affected,
                    vuln_id,
                    advisories,
                    severity_val,
                    cwe_ids,
                    withdrawn,
                )
            except json.JSONDecodeError as exc:
                log_blocking("error", "%s", exc)
