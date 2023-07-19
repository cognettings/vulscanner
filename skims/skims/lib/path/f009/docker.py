from collections.abc import (
    Iterator,
)
from lib.path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from lib.path.f009.utils import (
    is_key_sensitive,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
import re

# Constants
WS = r"\s*"
WSM = r"\s+"
DOCKERFILE_ENV: re.Pattern[str] = re.compile(
    rf"^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>[^$].+?){WS}$",
)


def dockerfile_env_secrets(content: str, path: str) -> Vulnerabilities:
    secret_smells: set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }

    def iterator() -> Iterator[tuple[int, int]]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := DOCKERFILE_ENV.match(line):
                secret: str = match.group("key").lower()
                value: str = match.group("value").strip('"').strip("'")
                is_interpolated: bool = (
                    not (value.startswith("${") and value.endswith("}"))
                    and not value.startswith("#{")
                    and not value.endswith("}#")
                )
                if (
                    value
                    and is_interpolated
                    and (
                        any(smell in secret for smell in secret_smells)
                        or is_key_sensitive(secret)
                    )
                ):
                    column: int = match.start("value")
                    yield line_no, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="f009.dockerfile_env_secrets_exposed",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOCKER_ENV_SECRETS,
    )
