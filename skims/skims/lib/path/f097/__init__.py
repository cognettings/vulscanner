from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f097.html import (
    has_reverse_tabnabbing,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_has_reverse_tabnabbing(content: str, path: str) -> Vulnerabilities:
    return has_reverse_tabnabbing(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (
            *results,
            run_has_reverse_tabnabbing(content_generator(), path),
        )

    return results
