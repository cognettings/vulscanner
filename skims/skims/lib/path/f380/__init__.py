from collections.abc import (
    Callable,
)
from lib.path.common import (
    EXTENSIONS_BASH,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib.path.f380.bash import (
    image_has_digest,
)
from lib.path.f380.docker import (
    unpinned_docker_image,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    return unpinned_docker_image(content=content, path=path)


@SHIELD_BLOCKING
def run_image_has_digest(content: str, path: str) -> Vulnerabilities:
    return image_has_digest(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    content = content_generator()

    if file_extension in EXTENSIONS_BASH:
        results = (run_image_has_digest(content, path),)

    if file_name in NAMES_DOCKERFILE:
        results = (run_unpinned_docker_image(content, path),)

    return results
