from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f393.composer import (
    composer_json_dev,
    composer_lock_dev,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_composer_json_dev() -> None:
    patt_dep_info: re.Pattern[str] = re.compile(
        r'"(?P<pkg_name>.*?)": "(?P<version>.*?)"'
    )
    path: str = "skims/test/data/lib/sca/f393/composer.json"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in range(41, 46):
        if dep_info := patt_dep_info.search(content[line_num]):
            pkg_name: str = dep_info.group("pkg_name")
            version: str = dep_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_item == pkg_name and version == item_ver
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_composer_lock_dev() -> None:
    patt_info: re.Pattern[str] = re.compile(r'".*?": "(?P<info>.*?)"')
    path: str = "skims/test/data/lib/sca/f393/composer.lock"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_lock_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in (365, 440, 510):
        if (pkg_name_match := patt_info.search(content[line_num])) and (
            version_match := patt_info.search(content[line_num + 1])
        ):
            pkg_name = pkg_name_match.group("info")
            version = version_match.group("info")
            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item == pkg_name and version == item_ver):
                assertion = not assertion
                break
        else:
            assertion = not assertion
            break

    assert assertion
