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
import re


def excessive_privileges_for_others(  # NOSONAR
    content: str, path: str
) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for index, lines in enumerate(content.splitlines(), 1):
            if "chmod" in lines and not lines.startswith("#"):
                for item in lines.split(" "):
                    if re.match(r"^\d{3}$", item) and not item.endswith("0"):
                        yield index, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f405.excessive_privileges_for_others",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.BASH_EXCESSIVE_PRIVILEGES_FOR_OTHERS,
    )
