from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Callable,
)
from lib.path.common import (
    SHIELD_BLOCKING,
)
from lib.path.f055.android import (
    android_backups_enabled,
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
    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        content = content_generator()
        soup = BeautifulSoup(content, features="html.parser")
        return (android_backups_enabled(content, soup, path),)

    return ()
