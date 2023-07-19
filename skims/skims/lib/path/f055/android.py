from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Iterator,
)
from lib.path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from lib.path.utilities.xml import (
    get_tag_attr_value,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)


def android_backups_enabled(
    content: str, soup: BeautifulSoup, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for tag in soup.find_all("application"):
            allow_backup = get_tag_attr_value(
                tag,
                key="android:allowBackup",
                default="not-set",
            ).lower()

            if allow_backup in {"true", "not-set"}:
                yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f055.app_backups_miss_configured",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PATH_APK_BACKUPS_ENABLED,
    )
