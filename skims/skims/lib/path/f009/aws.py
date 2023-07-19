from lib.path.common import (
    get_vulnerabilities_blocking,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    Regex,
)


def aws_credentials(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        description_key="f009.aws_credentials_exposed",
        grammar=Regex(r"AKIA[A-Z0-9]{16}"),
        path=path,
        method=MethodsEnum.AWS_CREDENTIALS,
    )
