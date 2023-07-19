from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
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


def header_allow_dangerous_methods(content: str, path: str) -> Vulnerabilities:
    danger_methods = {"debug", "trace"}

    def iterator() -> Iterator[tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("add"):
            if (
                isinstance(tag, Tag)
                and tag.name == "add"
                and (tag_value := tag.attrs.get("verb"))
                and any(
                    danger_m in tag_value.lower().split(",")
                    for danger_m in danger_methods
                )
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    desc_key = "f044.resource_has_danger_https_methods_enabled"
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=desc_key,
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_HEADER_ALLOW_DANGER_METHODS,
    )


def header_allow_all_methods(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("add"):
            if (
                isinstance(tag, Tag)
                and tag.name == "add"
                and (tag_value := tag.attrs.get("verb"))
                and tag_value.lower() == "*"
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f044.resource_has_https_methods_enabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_HEADER_ALLOW_ALL_METHODS,
    )
