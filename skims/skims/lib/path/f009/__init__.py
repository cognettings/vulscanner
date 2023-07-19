from collections.abc import (
    Callable,
)
from lib.path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    filetypes_to_check_credentials,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib.path.f009.aws import (
    aws_credentials,
)
from lib.path.f009.conf_files import (
    jwt_token,
    web_config_db_connection,
    web_config_user_pass,
)
from lib.path.f009.docker import (
    dockerfile_env_secrets,
)
from lib.path.f009.java import (
    java_properties_sensitive_data,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_aws_credentials(content: str, path: str) -> Vulnerabilities:
    return aws_credentials(content=content, path=path)


@SHIELD_BLOCKING
def run_dockerfile_env_secrets(content: str, path: str) -> Vulnerabilities:
    return dockerfile_env_secrets(content=content, path=path)


@SHIELD_BLOCKING
def run_java_properties_sensitive_data(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_sensitive_data(content=content, path=path)


@SHIELD_BLOCKING
def run_web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return web_config_user_pass(content=content, path=path)


@SHIELD_BLOCKING
def run_web_config_db_connection(content: str, path: str) -> Vulnerabilities:
    return web_config_db_connection(content=content, path=path)


@SHIELD_BLOCKING
def run_jwt_token(content: str, path: str) -> Vulnerabilities:
    return jwt_token(content=content, path=path)


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    content = content_generator()
    results: tuple[Vulnerabilities, ...] = ()
    if file_extension in {
        "bashrc",
        "bash_profile",
        "cfg",
        "conf",
        "config",
        "env",
        "groovy",
        "ini",
        "java",
        "jpage",
        "js",
        "json",
        "kt",
        "properties",
        "ps1",
        "py",
        "Renviron",
        "sbt",
        "sh",
        "sql",
        "swift",
        "xml",
        "yaml",
        "yml",
    } or filetypes_to_check_credentials(file_name, file_extension):
        results = (
            *results,
            run_aws_credentials(content, path),
            run_jwt_token(content, path),
        )

    if file_name in NAMES_DOCKERFILE:
        results = (*results, run_dockerfile_env_secrets(content, path))

    elif file_extension in EXTENSIONS_JAVA_PROPERTIES:
        results = (*results, run_java_properties_sensitive_data(content, path))
    elif file_extension in {"config", "httpsF5", "json", "settings"}:
        results = (
            *results,
            run_web_config_user_pass(content, path),
            run_web_config_db_connection(content, path),
        )

    return results
