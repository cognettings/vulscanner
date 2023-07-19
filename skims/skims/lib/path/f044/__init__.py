from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f044.conf_files import (
    header_allow_all_methods,
    header_allow_dangerous_methods,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_allow_danger_methods(content: str, path: str) -> Vulnerabilities:
    return header_allow_dangerous_methods(content=content, path=path)


@SHIELD_BLOCKING
def run_header_allow_all_methods(content: str, path: str) -> Vulnerabilities:
    return header_allow_all_methods(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in ("config", "xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_header_allow_all_methods(content, path),
            run_allow_danger_methods(content, path),
        )
    return results
