from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f075.android import (
    android_exported_cp,
    android_uri_permissions,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        content = content_generator()
        soup = BeautifulSoup(content, features="html.parser")
        results = (
            *results,
            android_exported_cp(content, soup, path),
            android_uri_permissions(content, soup, path),
        )

    return results
