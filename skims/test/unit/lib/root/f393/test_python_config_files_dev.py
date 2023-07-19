from collections.abc import (
    Iterator,
)
from lib.root.f393.python_config_files import (
    conan_conanfile_py_dev,
)
from lib.sca.common import (
    DependencyType,
)
from model.graph import (
    GraphShardMetadataLanguage,
)
from operator import (
    itemgetter,
)
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
from sast.parse import (
    get_shard,
)


@pytest.mark.skims_test_group("unittesting")
def test_conan_conanfile_py_dev(mocker: MockerFixture) -> None:
    path = "skims/test/data/lib_root/f393/conanfile.py"
    shard = get_shard(path, GraphShardMetadataLanguage.PYTHON, os.getcwd())
    if not shard:
        assert False
    methods_mock = mocker.Mock()
    methods_mock.selected_nodes = ["16"]
    mock_translate_deps = mocker.patch(
        "lib.root.f393.python_config_files."
        "translate_dependencies_to_vulnerabilities"
    )
    conan_conanfile_py_dev(shard, methods_mock)
    assertion: bool = True
    packages = (
        ("pkg_a", "4.5.1"),
        ("libtiff", "3.9.0"),
        ("glew", "2.1.0"),
        ("tool_win", "0.1"),
        ("cairo", "~0.17.0"),
    )
    trans_deps_args = mock_translate_deps.call_args.kwargs
    deps_info: Iterator[DependencyType] = trans_deps_args.get("dependencies")
    for product, version in packages:
        try:
            next_dep = next(deps_info)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion
