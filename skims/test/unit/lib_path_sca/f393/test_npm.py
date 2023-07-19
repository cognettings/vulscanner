from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f393.npm import (
    npm_package_json as npm_package_json_dev,
    npm_pkg_lock_json as npm_pkg_lock_json_dev,
    npm_yarn_lock_dev,
)
from operator import (
    itemgetter,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_json_dev() -> None:
    path = "skims/test/data/lib/sca/f393/package.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = ("xmldom", "0.4.0")
    try:
        next_dep = next(generator_dep)
        product = itemgetter("item")(next_dep[0])
        version = itemgetter("item")(next_dep[1])
    except StopIteration:
        assertion = not assertion
    if not (product == pkg_info[0] and version == pkg_info[1]):
        assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_yarn_lock_dev() -> None:
    path: str = "skims/test/data/lib/sca/f393/yarn.lock"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_yarn_lock_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = ("xmldom", "0.4.0")
    try:
        next_dep = next(generator_dep)
        pkg_item = itemgetter("item")(next_dep[0])
        item_ver = itemgetter("item")(next_dep[1])
    except StopIteration:
        assertion = not assertion
    if not (pkg_item == pkg_info[0] and pkg_info[1] == item_ver):
        assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_pkg_lock_json_dev() -> None:
    path: str = "skims/test/data/lib/sca/f393/package-lock.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_pkg_lock_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (("@babel/dev", "7.11.0.4"), ("hoek", "5.0.0.3"))
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
