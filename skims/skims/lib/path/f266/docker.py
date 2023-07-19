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

COMMANDS_REGEX = [
    re.compile(r"(\s+|^RUN).*useradd"),
    re.compile(r"(\s+|^RUN).*adduser"),
    re.compile(r"(\s+|^RUN).*addgroup"),
    re.compile(r"(\s+|^RUN).*usergroup"),
    re.compile(r"(\s+|^RUN).*usermod"),
    re.compile(r"^USER"),
]


def get_container_image(content: str) -> bool:
    for _, line in enumerate(content.splitlines(), start=1):
        if re.match(r"FROM\s+\S+", line):
            return True
    return False


def container_without_user(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        no_line = (0, 0)
        has_user = False
        for _, line in enumerate(content.splitlines(), start=1):
            if any(regex.match(line) for regex in COMMANDS_REGEX):
                has_user = True
        if get_container_image(content) and not has_user:
            yield no_line

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.container_without_user",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WITHOUT_USER,
    )


def container_with_user_root(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if re.match(r"^USER root", line):
                yield (line_number, 0)

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.docker_with_user_root",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WITH_USER_ROOT,
    )
