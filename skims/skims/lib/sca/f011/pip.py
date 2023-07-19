from collections.abc import (
    Iterator,
)
from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core import (
    MethodsEnum,
    Platform,
)
import requirements


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.PIP, MethodsEnum.PIP_REQUIREMENTS_TXT)
def pip_requirements_txt(content: str, path: str) -> Iterator[DependencyType]:
    for line_number, line in enumerate(content.splitlines(), 1):
        if line:
            for parse_dependency in requirements.parse(line):
                product = parse_dependency.name
                if len(parse_dependency.specs) == 1:
                    version = parse_dependency.specs[0][1]
                else:
                    continue

                yield format_pkg_dep(
                    product, version, line_number, line_number  # type: ignore
                )
