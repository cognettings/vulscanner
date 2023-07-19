from lib.path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD_BLOCKING,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)


@SHIELD_BLOCKING
def unverifiable_files(path: str, raw_content: bytes) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        description_key="src.lib_path.f117.unverifiable_files.description",
        iterator=iter([(0, 0)]),
        path=path,
        method=MethodsEnum.UNVERIFIABLE_FILES,
    )
