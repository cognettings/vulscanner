from collections.abc import (
    Callable,
)
from lib.path.common import (
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib.path.f332.docker import (
    container_with_disabled_ssl,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_container_disabled_ssl(content: str, path: str) -> Vulnerabilities:
    return container_with_disabled_ssl(content=content, path=path)


def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    content = content_generator()

    if file_name in NAMES_DOCKERFILE:
        results = (
            *results,
            run_container_disabled_ssl(content, path),
        )

    return results
