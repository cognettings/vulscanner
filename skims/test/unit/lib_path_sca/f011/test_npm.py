from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f011.npm import (
    npm_package_json,
    npm_package_lock_json,
    npm_yarn_lock,
)
from operator import (
    itemgetter,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_json() -> None:
    path: str = "skims/test/data/lib/sca/f011/package.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_json.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("@angular/core", "^13.3.3"),
        ("cloudron-sysadmin", "1.0.0"),
        ("script-manager", "0.8.6"),
        ("slug", "0.9.0"),
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


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_lock_json() -> None:
    path: str = "skims/test/data/lib/sca/f011/package-lock.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_lock_json.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("@babel/prod", "7.11.0.8"),
        ("hoek", "5.0.0.7"),
        ("hoek", "5.0.0.6"),
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


@pytest.mark.skims_test_group("unittesting")
def test_npm_yarn_lock() -> None:
    path: str = "skims/test/data/lib/sca/f011/yarn.lock"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_yarn_lock.__wrapped__(  # type: ignore
        file_contents, path
    )
    dependencies = list(generator_dep)
    assertion: bool = True
    packages = {
        "asn1": "0.2.6",
        "jsbn": "0.1.1",
        "uuid": "3.3.2",
    }
    for num in (2, 30, 58):
        next_dep = dependencies[num]
        pkg_item = itemgetter("item")(next_dep[0])
        item_ver = itemgetter("item")(next_dep[1])
        if not (pkg_item in packages and item_ver == packages[pkg_item]):
            assertion = not assertion

    assert assertion
