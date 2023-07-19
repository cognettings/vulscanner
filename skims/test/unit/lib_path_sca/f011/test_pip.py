from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f011.pip import (
    pip_requirements_txt,
)
from operator import (
    itemgetter,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_pip_requirements_txt() -> None:
    path: str = "skims/test/data/lib/sca/f011/requirements.txt"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = pip_requirements_txt.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num, line in enumerate(content, 1):
        pkg_name, version = line.split("==")

        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            line_dep, item = itemgetter("line", "item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = (
            pkg_item in pkg_name and version == item and line_num == line_dep
        )
        if not equal_props:
            assertion = not assertion
            break

    assert assertion
