from . import (
    findings as findings_utils,
)
import collections
from collections.abc import (
    KeysView,
)
from custom_exceptions import (
    InvalidFilter,
)
from db_model.findings.types import (
    Finding,
)
import re
from typing import (
    Any,
)


def camel_case_list_dict(elements: list[dict]) -> list[dict]:
    """Convert a the keys of a list of dicts to camelcase."""
    return [
        {snakecase_to_camelcase(k): element[k] for k in element}
        for element in elements
    ]


def camelcase_to_snakecase(str_value: str) -> str:
    """Convert a camelcase string to snakecase."""
    my_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str_value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", my_str).lower()


def filter_findings(
    findings: list[Finding], filters: dict[str, Any]
) -> list[Finding]:
    """Return filtered findings according to filters."""

    def satisfies_filter(finding: Finding) -> bool:
        filter_finding_value = {
            "verified": findings_utils.is_verified(
                finding.unreliable_indicators.unreliable_verification_summary
            ),
        }
        hits = 0
        for attr, value in filters.items():
            try:
                result = filter_finding_value[attr]
            except KeyError as ex:
                raise InvalidFilter(attr) from ex
            if str(result) == str(value):
                hits += 1
        return hits == len(filters)

    return [finding for finding in findings if satisfies_filter(finding)]


def list_to_dict(
    keys: list[object], values: list[object]
) -> dict[object, object]:
    """Merge two lists into a {key: value} dictionary"""
    dct: dict[object, object] = collections.OrderedDict()
    index = 0

    if len(keys) < len(values):
        diff = len(values) - len(keys)
        for i in range(diff):
            del i
            keys.append("")
    elif len(keys) > len(values):
        diff = len(keys) - len(values)
        for i in range(diff):
            del i
            values.append("")
    else:
        # Each key has a value associated, so there's no need to empty-fill
        pass

    for item in values:
        if keys[index] == "":
            dct[index] = item
        else:
            dct[keys[index]] = item
        index += 1
    return dct


def snakecase_to_camelcase(str_value: str) -> str:
    """Convert a snakecase string to camelcase."""
    return re.sub("_.", lambda x: x.group()[1].upper(), str_value)


def replace_all(text: str, dic: dict[str, str]) -> str:
    for i, j in list(dic.items()):
        text = text.replace(i, j)
    return text


# Standardization helper utils


def clean_up_kwargs(
    kwargs: dict, keys_to_remove: tuple = ("group_name", "project_name")
) -> dict:
    """Removes the specified keys to avoid **args duplication in helper methods
    that receive dicts"""
    for key in keys_to_remove:
        kwargs.pop(key, None)
    return kwargs


def duplicate_dict_keys(
    dictionary: dict,
    first_key: str,
    second_key: str,
) -> dict:
    """Checks which of these keys exist in the dict and copies its value on
    the other key, if none exist, raises an error"""
    keys: KeysView = dictionary.keys()
    if first_key in keys and second_key not in keys:
        dictionary[second_key] = dictionary.get(first_key)
    elif second_key in keys and first_key not in keys:
        dictionary[first_key] = dictionary.get(second_key)
    return dictionary


def get_key_or_fallback(
    kwargs: dict,
    current_key: str = "group_name",
    old_key: str = "project_name",
    fallback: str | None = None,
) -> Any:
    """Tries to get current_key's value from kwargs, with a (lazy) old_key as a
    second option. If none of the keys can be found it returns a fallback value
    if specified, returns None otherwise"""
    return kwargs.get(current_key, kwargs.get(old_key, fallback))


def get_present_key(
    kwargs: dict,
    current_key: str = "group_name",
    old_key: str = "project_name",
) -> str:
    """Checks if either current_key or old_key exist in kwargs and returns the
    first of these keys, raises a KeyError otherwise"""
    if current_key in kwargs.keys():
        return current_key
    if old_key in kwargs.keys():
        return old_key
    raise KeyError(
        f"Couldn't find either {current_key} or {old_key} keys in the dict"
    )


def map_roles(
    role: str,
) -> str:
    """Maps old roles to their new equivalents"""
    if role.lower() == "customer":
        return "user"
    if role.lower() == "customeradmin":
        return "user_manager"
    return role


def is_sequence(specific: str) -> bool:
    """Validate if a specific field has secuence value."""
    return "," in specific


def escape_csv_field(raw_text: str) -> str:
    partially_escaped_str: str = raw_text.strip().replace('"', '""')
    return f"'{partially_escaped_str}"


def get_advisories(where: str) -> str | None:
    result = re.search(r"(?P<name>(\(.*\))?(\s+\[.*\]))", where)
    if result:
        return result.group("name")
    return None


def get_missing_dependency(where: str) -> str:
    try:
        str_info = where.split(" ", maxsplit=1)[1]
    except IndexError:
        return ""
    if match := re.match(r"\(missing dependency: (?P<name>(.+))\)$", str_info):
        match_dict = match.groupdict()
        return match_dict["name"]

    return ""


def get_apk_details(where: str) -> str:
    try:
        str_info = where.split(" ", maxsplit=1)[1]
    except IndexError:
        return ""
    if match := re.match(r"\(Details: (?P<details>(.+))\)$", str_info):
        match_dict = match.groupdict()
        return match_dict["details"]

    return ""


def ignore_advisories(where: str | None) -> str:
    if where is not None:
        where = re.sub(r"(\s+\(.*\))?(\s+\[.*\])?", "", where)
    return str(where)
