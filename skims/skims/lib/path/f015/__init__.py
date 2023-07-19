from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f015.conf_files import (
    basic_auth_method,
    jmx_header_basic,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_jmx_header_basic(
    content: str,
    path: str,
) -> Vulnerabilities:
    return jmx_header_basic(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def run_basic_auth_method(content: str, path: str) -> Vulnerabilities:
    return basic_auth_method(content=content, path=path)


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
            run_jmx_header_basic(content, path),
            run_basic_auth_method(content, path),
        )

    return results
