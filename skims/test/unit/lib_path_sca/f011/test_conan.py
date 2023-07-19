from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f011.conan import (
    conan_conanfile_txt,
    conan_lock,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_conan_conanfile_txt() -> None:
    conan_dep: re.Pattern[str] = re.compile(
        r"^(?P<product>[\w\-]+)\/\[?(?P<version>[^\],]+)"
    )
    path: str = "skims/test/data/lib/sca/f011/conanfile.txt"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = conan_conanfile_txt.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in range(1, 8):
        if pkg_info := conan_dep.search(content[line_num]):
            pkg_name = pkg_info.group("product")
            version = pkg_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item in pkg_name and version == item):
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_conan_lock() -> None:
    path: str = "skims/test/data/lib/sca/f011/conan.lock"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = conan_lock.__wrapped__(file_contents, path)  # type: ignore
    assertion: bool = True
    packages = (
        ("sound32", "1.0"),
        ("matrix", "1.1"),
        ("libpng", "1.7.0"),
        ("libxml2", "2.10.0"),
    )
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion
