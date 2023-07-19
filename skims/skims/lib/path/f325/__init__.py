from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f325.dotnetconfig import (
    excessive_auth_privileges,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_excessive_auth_privileges(content: str, path: str) -> Vulnerabilities:
    return excessive_auth_privileges(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "config":
        results = (
            *results,
            run_excessive_auth_privileges(content_generator(), path),
        )

    return results
