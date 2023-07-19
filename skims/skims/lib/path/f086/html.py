from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Iterator,
)
from lib.path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)


def has_not_subresource_integrity(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        r"""
        Check if elements fetched by the provided HTML have `SRI`.

        See: `Documentation <https://developer.mozilla.org/en-US/
        docs/Web/Security/Subresource_Integrity>`_.
        """

        soup = BeautifulSoup(content, features="html.parser")
        for elem_types in ("link", "script"):
            for elem in soup(elem_types):
                if (
                    (ref_ext := elem.get("href") or elem.get("src"))
                    and ref_ext.startswith("http")
                    and (
                        ref_ext.endswith(".js")
                        or elem.get("type") == "text/javascript"
                    )
                    and not elem.get("integrity")
                ):
                    yield elem.sourceline, elem.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f086.sub_resource_integrity.missing_integrity"
        ),
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_HAS_NOT_SUB_RESOURCE_INTEGRITY,
    )
