from collections.abc import (
    Iterator,
)
from lib.sca.common import (
    DependencyType,
)
from lib.sca.f393.gem import (
    gem_gemfile_dev,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_dev() -> None:
    path: str = "skims/test/data/lib/sca/f393/Gemfile"
    gemfile_dep: re.Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    gem_gemfile_fun = gem_gemfile_dev.__wrapped__  # type: ignore
    content: list[str] = file_contents.splitlines()
    generator_gem: Iterator[DependencyType] = gem_gemfile_fun(
        file_contents, path
    )
    assertion: bool = True
    lines_prod_deps = [*range(117, 127), 131, 132, *range(142, 145)]
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
