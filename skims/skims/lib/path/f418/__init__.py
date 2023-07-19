from collections.abc import (
    Callable,
)
from lib.path.common import (
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib.path.f418.docker import (
    docker_using_add_command,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_docker_using_add_command(
    content: str,
    path: str,
) -> Vulnerabilities:
    return docker_using_add_command(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
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
            run_docker_using_add_command(content, path),
        )
    return results
