import re
from typing import (
    Any,
)


def get_sca_info(what: str) -> dict[str, Any] | None:
    try:
        str_info = what.split(" ", maxsplit=1)[1]
    except IndexError:
        return None
    if match := re.match(
        r"\((?P<name>(\S+)) v(?P<version>(.+))\) \[(?P<cve>(.+))\]", str_info
    ):
        match_dict = match.groupdict()
        return dict(
            dependency_name=match_dict["name"],
            dependency_version=match_dict["version"],
            cve=match_dict["cve"].split(", "),
        )
    return None


def get_missing_dependency(what: str) -> dict[str, Any] | None:
    try:
        str_info = what.split(" ", maxsplit=1)[1]
    except IndexError:
        return None
    if match := re.match(r"\(missing dependency: (?P<name>(.+))\)$", str_info):
        match_dict = match.groupdict()
        return dict(
            dependency_name=match_dict["name"],
        )

    return None


def get_apk_details(what: str) -> dict[str, Any] | None:
    try:
        str_info = what.split(" ", maxsplit=1)[1]
    except IndexError:
        return None
    if match := re.match(r"\(Details: (?P<details>(.+))\)$", str_info):
        match_dict = match.groupdict()
        return dict(
            details=match_dict["details"],
        )

    return None


def format_what(vulnerability: Any) -> str:
    what = re.sub(
        r"\s(\(.*?\))((\s)(\[.*?\]))?", "", vulnerability.what  # NOSONAR
    )
    while what.endswith("/"):
        what = what.rstrip("/")
    return what
