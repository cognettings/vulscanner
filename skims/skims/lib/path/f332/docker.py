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


def container_with_disabled_ssl(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for idx, line in enumerate(content.splitlines(), start=1):
            if re.search(
                r"\s+\-Dcom.sun.management.jmxremote.ssl=false\s?", line
            ):
                yield (idx, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f332.container_disabled_ssl",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_DISABLED_SSL,
    )
