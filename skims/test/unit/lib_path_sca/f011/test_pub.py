from ..utils import (
    get_file_info_from_path,
)
from collections.abc import (
    Iterator,
)
from lib.sca.common import (
    DependencyType,
)
from lib.sca.f011.pub import (
    pub_pubspec_yaml,
)
from operator import (
    itemgetter,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_pub_pubspec_yaml() -> None:
    path: str = "skims/test/data/lib/sca/f011/pubspec.yaml"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    gemfile_lock_fun = pub_pubspec_yaml.__wrapped__  # type: ignore
    generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
        file_contents, path
    )
    assertion: bool = True

    for line_num in range(13, 27):
        pkg_name, version = content[line_num].lstrip().split(": ")
        current_dep = next(generator_gem)
        try:
            item = itemgetter("item")(current_dep[0])
            item_version = itemgetter("item")(current_dep[1])
        except StopIteration:
            assertion = not assertion
            break

        if pkg_name != item or version != item_version:
            assertion = not assertion
            break

    assert assertion
