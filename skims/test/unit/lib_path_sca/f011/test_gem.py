from ..utils import (
    get_file_info_from_path,
)
from collections.abc import (
    Iterator,
)
from lib.sca.common import (
    DependencyType,
)
from lib.sca.f011.gem import (
    gem_gemfile,
    gem_gemfile_lock,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile() -> None:
    gemfile_dep: re.Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    path: str = "skims/test/data/lib/sca/f011/Gemfile"
    file_contents: str = get_file_info_from_path(path)
    gem_gemfile_fun = gem_gemfile.__wrapped__  # type: ignore
    content: list[str] = file_contents.splitlines()
    generator_gem: Iterator[DependencyType] = gem_gemfile_fun(
        file_contents, path
    )
    assertion: bool = True
    lines_prod_deps = [*range(116), 130, 136, 139, *range(148, 182)]
    for line_num in lines_prod_deps:
        if matched := re.search(gemfile_dep, content[line_num]):
            pkg_name: str = matched.group("name")

            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_name == item and line_num + 1 == line
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_lock() -> None:
    gem_lock_dep: re.Pattern[str] = re.compile(
        r"^\s{4}(?P<gem>(?P<name>[\w\-]+)\s?(\(.*\))?)"
    )
    path: str = "skims/test/data/lib/sca/f011/Gemfile.lock"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    gemfile_lock_fun = gem_gemfile_lock.__wrapped__  # type: ignore
    generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
        file_contents, path
    )
    assertion: bool = True

    for line_num in range(22, 219):
        if matched := re.search(gem_lock_dep, content[line_num]):
            pkg_name: str = matched.group("name")
            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            if pkg_name != item or line_num + 1 != line:
                assertion = not assertion
                break

    assert assertion
