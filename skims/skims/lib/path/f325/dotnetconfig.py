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


def excessive_auth_privileges(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Check if authorization to users is configured with excessive privileges
        https://docs.microsoft.com/en-us/iis/configuration/
        system.webserver/security/authorization/add
        """
        soup = BeautifulSoup(content, features="html.parser")

        for custom_headers in soup("authorization"):
            for tag in custom_headers.contents:
                if (
                    isinstance(tag, Tag)
                    and tag.name == "add"
                    and tag.attrs.get("accesstype") == "Allow"
                    and tag.attrs.get("users") == "*"
                ):
                    yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f325.json_principal_wildcard",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_EXCESSIVE_AUTH_PRIVILEGES,
    )
