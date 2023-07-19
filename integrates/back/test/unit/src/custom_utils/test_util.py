from custom_utils import (
    datetime as datetime_utils,
    files as files_utils,
    utils,
)
from custom_utils.utils import (
    is_sequence,
)
from datetime import (
    datetime,
)
from organizations import (
    utils as orgs_utils,
)
import os
import pytest
import pytz
import re
from settings import (
    TIME_ZONE,
)
from typing import (
    Dict,
    List,
    Union,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_get_current_date() -> None:
    tzn = pytz.timezone(TIME_ZONE)
    today = datetime.now(tz=tzn)
    date = today.strftime("%Y-%m-%d %H:%M")
    test_data = datetime_utils.get_now_as_str()[:-3]
    assert isinstance(test_data, str)
    assert test_data == date


def test_assert_file_mime() -> None:
    path = os.path.dirname(__file__)
    filename = os.path.join(path, "mock/test-vulns.yaml")
    non_included_filename = os.path.join(path, "mock/test.7z")
    allowed_mimes = ["text/plain"]
    assert files_utils.assert_file_mime(filename, allowed_mimes)
    assert not files_utils.assert_file_mime(
        non_included_filename, allowed_mimes
    )


@pytest.mark.parametrize(
    ["inputs", "expected_output"],
    [
        [
            ["replaced", {"a": "a", "b": "b", "c": "c"}],
            "replaced",
        ],
        [
            ["replaced", {"r": "d", "p": "sp", "de": "di"}],
            "displaced",
        ],
    ],
)
def test_replace_all(
    inputs: List[Union[str, Dict[str, str]]], expected_output: str
) -> None:
    assert utils.replace_all(*inputs) == expected_output  # type: ignore


@pytest.mark.parametrize(
    ["keys", "values", "expected_result"],
    [
        [
            ["item", "item2", "item3"],
            ["hi", "this is a", "item"],
            {"item": "hi", "item2": "this is a", "item3": "item"},
        ],
        [
            ["item", "item2"],
            ["hi", "this is a", "item"],
            {"item": "hi", "item2": "this is a", 2: "item"},
        ],
        [
            ["item", "item2", "item3"],
            ["hi", "this is a"],
            {"item": "hi", "item2": "this is a", "item3": ""},
        ],
    ],
)
def test_list_to_dict(
    keys: List[object],
    values: List[object],
    expected_result: Dict[object, object],
) -> None:
    assert utils.list_to_dict(keys, values) == expected_result


def test_is_sequence() -> None:
    secuence_value = "20,21,22"
    no_secuence_values = ["20-30", "20"]
    assert is_sequence(secuence_value)
    for no_secuence_value in no_secuence_values:
        assert not is_sequence(no_secuence_value)


@pytest.mark.parametrize(
    ["test_case", "expected_output"],
    [
        ["thisIsATest", "this_is_a_test"],
        ["thi2%s0ter_Cas3", "thi2%s0ter__cas3"],
    ],
)
def test_camelcase_to_snakecase(test_case: str, expected_output: str) -> None:
    assert utils.camelcase_to_snakecase(test_case) == expected_output


@pytest.mark.parametrize(
    ["date"], [["2019-03-30 00:00:00"], ["2019/03/30 00:00:00"]]
)
def test_is_valid_format(date: str) -> None:
    date_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    if date_regex.match(date):
        assert datetime_utils.is_valid_format(date)
    else:
        assert not datetime_utils.is_valid_format(date)


@pytest.mark.parametrize(
    ["key", "expected_key"], [["VGVzdCBTU0g=", "VGVzdCBTU0gK"]]
)
def test_format_credential_key(key: str, expected_key: str) -> None:
    assert orgs_utils.format_credentials_ssh_key(ssh_key=key) == expected_key
    assert (
        orgs_utils.format_credentials_ssh_key(ssh_key=expected_key)
        == expected_key
    )
