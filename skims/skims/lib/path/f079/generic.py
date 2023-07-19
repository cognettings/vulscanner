from lib.path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)


def non_upgradeable_deps(path: str, raw_content: bytes) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        description_key="src.lib_path.f079.non_upgradeable_deps.description",
        iterator=iter([(1, 0)]),
        path=path,
        method=MethodsEnum.NON_UPGRADEABLE_DEPS,
    )
