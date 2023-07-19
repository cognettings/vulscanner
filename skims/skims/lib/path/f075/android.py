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


def android_exported_cp(
    content: str, soup: BeautifulSoup, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for tag in soup.find_all("provider"):
            exported = get_tag_attr_value(
                tag,
                key="android:exported",
                default="false",
            ).lower()

            if exported == "true":
                yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f075.android_manifest_exported_enabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PATH_APK_EXPORTED_CP,
    )


def android_uri_permissions(
    content: str, soup: BeautifulSoup, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for tag in soup.find_all("provider"):
            grant_uri_permissions = get_tag_attr_value(
                tag,
                key="android:grantUriPermissions",
                default="false",
            ).lower()

            if grant_uri_permissions == "true":
                yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f075.android_manifest_UriPermissions_enabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.PATH_APK_EXPORTED_CP,
    )
