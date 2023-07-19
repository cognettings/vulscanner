from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f079.generic import (
    non_upgradeable_deps,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_non_upgradeable_deps(path: str, raw_content: bytes) -> Vulnerabilities:
    return non_upgradeable_deps(path=path, raw_content=raw_content)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], bytes],
    unique_nu_paths: set[str],
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if path in unique_nu_paths:
        results = (
            *results,
            run_non_upgradeable_deps(path, raw_content_generator()),
        )

    return results
