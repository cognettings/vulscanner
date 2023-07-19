from collections.abc import (
    Iterator,
)
from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
    get_conan_dep_info,
    pkg_deps_to_vulns,
    resolve_conan_lock_deps,
)
from model.core import (
    MethodsEnum,
    Platform,
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_CONANFILE_TXT)
def conan_conanfile_txt(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("[requires]"):
            line_deps = True
        elif line_deps:
            if not line or line.startswith("["):
                break
            pkg_name, pkg_version = get_conan_dep_info(line)
            yield format_pkg_dep(
                pkg_name, pkg_version, line_number, line_number
            )


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.CONAN, MethodsEnum.CONAN_LOCK)
def conan_lock(content: str, path: str) -> Iterator[DependencyType]:
    return resolve_conan_lock_deps(content, "requires")
