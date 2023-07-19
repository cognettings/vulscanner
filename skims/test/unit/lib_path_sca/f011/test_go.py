from ..utils import (
    get_file_info_from_path,
)
from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
)
from lib.sca.f011.go import (
    add_require,
    go_mod,
    GO_REQ_MOD_DEP,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_go_add_require() -> None:
    req_dict: dict[str, DependencyType] = {}
    dep_line: str = "require gorm.io/gorm v1.24.0"
    line_number: int = 24
    if matched := re.search(GO_REQ_MOD_DEP, dep_line):
        add_require(matched, req_dict, line_number)
    exp_dict = {
        "gorm.io/gorm": format_pkg_dep(
            "gorm.io/gorm", "1.24.0", line_number, line_number
        )
    }
    assert exp_dict == req_dict


@pytest.mark.skims_test_group("unittesting")
def test_go_mod() -> None:
    path: str = "skims/test/data/lib/sca/f011/go.mod"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = go_mod.__wrapped__(file_contents, path)  # type: ignore
    assertion: bool = True
    for line_num in [*range(5, 28), *range(31, 85), 91, 94, 95]:
        if line_num in (91, 94, 95):
            dep_splitted_info = content[line_num].split("=> ")[1].split()
        else:
            dep_splitted_info = content[line_num].strip().split()
        pkg_name: str = dep_splitted_info[0]
        version: str = dep_splitted_info[1][1:]

        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            line, item = itemgetter("line", "item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = (
            pkg_item in pkg_name and version == item and line_num + 1 == line
        )
        if not equal_props:
            assertion = not assertion
            break

    assert assertion
