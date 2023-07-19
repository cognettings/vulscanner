from collections.abc import (
    Iterator,
)
from lib.root.f011.python_config_files import (
    conan_conanfile_py,
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
def test_conan_conanfile_py(mocker: MockerFixture) -> None:
    path = "skims/test/data/lib_root/f011/conanfile.py"
    shard = get_shard(path, GraphShardMetadataLanguage.PYTHON, os.getcwd())
    if not shard:
        assert False
    methods_mock = mocker.Mock()
    methods_mock.selected_nodes = ["16"]
    mock_translate_deps = mocker.patch(
        "lib.root.f011.python_config_files."
        "translate_dependencies_to_vulnerabilities"
    )
    conan_conanfile_py(shard, methods_mock)
    assertion: bool = True
    packages = (
        ("libde265", "1.0.8"),
        ("opencv", "2.4.13.7"),
        ("poco", "1.10.1"),
        ("opencv", "2.2"),
        ("assimp", "~5.1.0"),
        ("closecv", "4.2"),
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
