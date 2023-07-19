from lib.path.common import (
    get_vulnerabilities_blocking,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    ParseResults,
    Regex,
)
import re

SHA_256_PATTERN = r"FROM\s+.*@sha256:[a-fA-F0-9]{43,}(\s+AS\s+\S+)?"
VARIABLE_PATTERN = r"FROM\s+(#\{.+\}#|\$\{.+\}|\$.+)"


def unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    def check_regex(tokens: ParseResults) -> bool:
        for token in tokens:
            if re.match(SHA_256_PATTERN, token) or re.match(
                VARIABLE_PATTERN, token
            ):
                return False
        return True

    grammar = Regex(r"FROM\s+.+")
    grammar.addCondition(check_regex)

    return get_vulnerabilities_blocking(
        content=content,
        description_key="criteria.vulns.380.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.UNPINNED_DOCKER_IMAGE,
    )
