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


def android_debugging_enabled(
    content: str, soup: BeautifulSoup, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for tag in soup.find_all("application"):
            is_debuggable = get_tag_attr_value(
                tag,
                key="android:debuggable",
                default="false",
            ).lower()

            if is_debuggable == "true":
                yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f058.app_manifest_debugging_enabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PATH_APK_DEBUGGING_ENABLED,
    )
