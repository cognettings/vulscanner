import boto3
import click
import json
import logging
import os
import re
import requests
from requests.exceptions import (
    ConnectTimeout,
    HTTPError,
    Timeout,
)
from retry import (  # type: ignore
    retry,
)
import subprocess
import sys
from typing import (
    Any,
    cast,
)
import uuid
import yaml  # type: ignore

_FORMAT: str = "[%(levelname)s] %(message)s"
logging.basicConfig(format=_FORMAT)

LOGGER: logging.Logger = logging.getLogger("execute_machine")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False


PATTERNS: list[dict[str, str | list[dict[str, Any]]]] = [
    {
        "name": ".csproj",
        "description": "visual studio c sharp project",
        "type": "file_extension",
    },
    {
        "name": "App.Config",
        "description": "C Sharp module",
        "type": "file_extension",
    },
    {
        "name": ".sln",
        "description": "visual studio c sharp set of projects",
        "type": "file_extension",
    },
    {
        "name": ".vbproj",
        "description": "visual studio visual basic project",
        "type": "file_extension",
    },
    {
        "name": "pom.xml",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": True}
        ],
        "description": "java maven project",
        "type": "specific_file",
    },
    {
        "name": "build.xml",
        "description": "Apache ant build",
        "type": "specific_file",
    },
    {
        "name": "makes.nix",
        "description": "makes root dir",
        "type": "specific_file",
    },
    {
        "name": "main.nix",
        "description": "nix root dir",
        "type": "specific_file",
    },
    {
        "name": "build.gradle",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": True}
        ],
        "description": "java gradel project",
        "type": "specific_file",
    },
    {
        "name": "settings.gradle",
        "description": "java gradel project",
        "type": "specific_file",
    },
    {
        "name": "setup.cfg",
        "description": "python project",
        "type": "specific_file",
    },
    {
        "name": "pyproject.toml",
        "description": "python project",
        "type": "specific_file",
    },
    {
        "name": "requirements.txt",
        "description": "file of dependencies in python projects",
        "type": "specific_file",
    },
    {
        "name": "poetry.lock",
        "description": "python poetry project",
        "type": "specific_file",
    },
    {
        "name": "setup.py",
        "description": "python poetry project",
        "type": "specific_file",
    },
    {
        "name": "package.json",
        "description": "node npm project",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "type": "specific_file",
    },
    {
        "name": "yarn.lock",
        "description": "node yarn project",
        "requires": [
            {"name": "directory", "values": ["src"], "optional": False}
        ],
        "type": "specific_file",
    },
    {
        "name": "main.tf",
        "description": "terraform infra",
        "type": "specific_file",
    },
    {
        "name": "variables.tf",
        "description": (
            "terraform infra, main can not be present, this can be a module"
        ),
        "type": "specific_file",
    },
    {
        "name": "Podfile",
        "description": ("swift project"),
        "type": "specific_file",
    },
]


@retry(
    (TypeError, ConnectionError, ConnectTimeout, Timeout, HTTPError),
    tries=5,
    delay=2,
)
def _request_asm(payload: dict[str, Any], token: str) -> dict[str, Any] | None:
    result: dict[str, Any] | None = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    with requests.session() as session:
        response = session.post(
            "https://app.fluidattacks.com/api",
            data=json.dumps(payload),
            headers=headers,
        )
        try:
            result = response.json()
        except json.JSONDecodeError:
            LOGGER.error(response.text)
            return result
        if response.status_code >= 400:
            if result:
                for error in result.get("errors", []):
                    LOGGER.error(error)
            else:
                LOGGER.error(response.text)
            response.raise_for_status()
    return result


def get_roots(token: str, group_name: str) -> list[dict[str, Any]] | None:
    result: list[dict[str, Any]] | None = None
    query = """
        query MachineGetGroupRoots(
            $groupName: String!
        ) {
            group(groupName: $groupName) {
                roots {
                    ... on GitRoot {
                        gitEnvironmentUrls {
                          url
                          id
                          secrets {
                            value
                            key
                          }
                          urlType
                        }
                        nickname
                        url
                        id
                        gitignore
                    }
                }
            }
        }
    """
    payload = {"query": query, "variables": {"groupName": group_name}}

    response = _request_asm(payload=payload, token=token)
    if response is not None:
        result = response["data"]["group"]["roots"]
    else:
        LOGGER.error("Failed to fetch root info for group %s", group_name)

    return result


def get_group_language(token: str, group_name: str) -> str | None:
    result: str | None = None
    query = """
        query MachineGetGroupLanguage($groupName: String!) {
            group(groupName: $groupName) {
                language
            }
        }
    """
    payload = {"query": query, "variables": {"groupName": group_name}}

    response = _request_asm(payload=payload, token=token)
    if response is not None:
        result = response["data"]["group"]["language"]
    else:
        LOGGER.error("Failed to fetch root info for group %s", group_name)

    return result


def get_repo_head_hash(path: str) -> str:
    with subprocess.Popen(["git", "rev-parse", "HEAD"], cwd=path) as executor:
        _stdout, _ = executor.communicate()
        return _stdout.decode()


def evaluate_requirement(
    requirement: dict[str, Any],
    current_directories: list[str],
    current_files: list[str],
) -> bool:
    if requirement.get("optional", False):
        return True
    if requirement["name"] == "directory":
        return all(
            required_directory in current_directories
            for required_directory in requirement["values"]
        )
    if requirement["name"] == "file":
        return all(
            required_file in current_files
            for required_file in requirement["values"]
        )
    return False


def file_match_expected_patterns(
    file: str,
    current_directories: list[str],
    current_files: list[str],
) -> dict[str, Any] | None:
    for config in PATTERNS:
        if (
            config["type"] == "file_extension"
            and re.match(f"(.?)*{config['name']}$", file) is not None
        ):
            # matches the pattern of a project configuration file
            return config

        if config["type"] == "specific_file" and config["name"] == file:
            # has the name of a configuration file
            if requires := config.get("requires"):
                requires = cast(list[dict[str, Any]], requires)
                if all(
                    evaluate_requirement(
                        req, current_directories, current_files
                    )
                    for req in requires
                ):
                    return config
            else:
                return config

    return None


def is_additional_path(dirs: list[str], files: list[str]) -> bool:
    for file in files:
        match_config = file_match_expected_patterns(file, dirs, files)
        if match_config is not None:
            return True

    return False


def generate_config_files(
    *,
    group_name: str,
    root_nickname: str,
    checks: tuple[str, ...],
    token: str,
    language: str = "EN",
    working_dir: str = ".",
    retry_number: int,
) -> list[dict[str, Any]]:
    additional_paths: list[str] = []
    all_configs: list[dict[str, Any]] = []
    for current_dir, dirs, files in os.walk(working_dir):
        if current_dir == working_dir:
            continue
        if is_additional_path(dirs, files):
            additional_paths.append(current_dir.replace(f"{working_dir}/", ""))
    commit = ""
    git_root = next(
        (
            root
            for root in get_roots(token, group_name) or []
            if root.get("nickname") == root_nickname
        ),
        None,
    )
    if not git_root:
        return []
    all_configs = [
        generate_config(
            group_name=group_name,
            git_root=git_root,
            checks=checks,
            language=language,
            working_dir=working_dir,
            is_main=True,
            commit=commit,
            retry_number=retry_number,
        )
    ]

    return all_configs


def generate_config(  # pylint: disable=too-many-locals
    *,
    group_name: str,
    git_root: dict[str, Any],
    checks: tuple[str, ...],
    commit: str,
    language: str = "EN",
    include: tuple[str, ...] = (),
    exclude: tuple[str, ...] = (),
    working_dir: str = ".",
    is_main: bool = False,
    retry_number: int,
) -> dict[str, Any]:
    namespace = git_root["nickname"]
    execution_id = (
        f"{group_name}"
        f'_{os.environ.get("AWS_BATCH_JOB_ID", uuid.uuid4().hex)}'
        f"_{namespace}"
        f"_{uuid.uuid4().hex[:8]}"
    )

    dast_config: dict[str, Any] | None = None
    if is_main:
        env_urls: set[str] = {
            environment_url["url"]
            for environment_url in git_root["gitEnvironmentUrls"]
            if environment_url["urlType"] == "URL"
        }
        enable_dast_checks = False
        if len(env_urls) > 0:
            enable_dast_checks = True

        secrets = {
            secret["key"]: secret["value"]
            for environment_url in git_root["gitEnvironmentUrls"]
            if environment_url["urlType"] == "CLOUD"
            for secret in environment_url["secrets"]
        }
        dast_config = {
            "aws_credentials": (
                [
                    {
                        "access_key_id": secrets["AWS_ACCESS_KEY_ID"],
                        "secret_access_key": secrets["AWS_SECRET_ACCESS_KEY"],
                    }
                ]
                if (
                    "AWS_ACCESS_KEY_ID" in secrets
                    and "AWS_SECRET_ACCESS_KEY" in secrets
                )
                else []
            ),
            "urls": list(env_urls),
            "http_checks": enable_dast_checks,
            "ssl_checks": enable_dast_checks,
        }
    sast_config = {
        "include": include if include else ["."],
        "exclude": list(
            sorted(
                (
                    "glob(**/.git)",
                    *exclude,
                    *(git_root["gitignore"] if git_root else []),
                )
            )
        ),
        "lib_path": True,
        "lib_root": True,
    }
    sca_config = {
        "include": include if include else ["."],
        "exclude": list(
            sorted(
                (
                    "glob(**/.git)",
                    *exclude,
                    *(git_root["gitignore"] if git_root else []),
                )
            )
        ),
    }
    if retry_number > 1:
        sast_config.update({"recursion_limit": 1000})
    return {
        "apk": {
            "exclude": [],
            "include": ["glob(**/*.apk)"] if is_main else [],
        },
        "checks": list(checks),
        "commit": commit,
        "dast": dast_config,
        "language": language,
        "namespace": namespace,
        "output": {
            "file_path": os.path.abspath(
                f"{working_dir}/execution_results/{execution_id}.sarif"
            ),
            "format": "SARIF",
        },
        "execution_id": execution_id,
        "sast": sast_config,
        "sca": sca_config,
        "working_dir": os.path.abspath(working_dir),
    }


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: Any) -> None:  # pylint: disable=unused-argument
    pass


@cli.command()
@click.option("--group-name", required=True)
@click.option("--root-nickname", required=True)
@click.option("--api-token", required=True)
@click.option("--checks", required=True)
@click.option("--working-dir", required=True, type=click.Path(), default=".")
@click.option("--retry-number", required=True, default=0)
def generate_configs(  # pylint: disable=too-many-arguments
    group_name: str,
    root_nickname: str,
    api_token: str,
    checks: str,
    working_dir: str,
    retry_number: int,
) -> None:
    configs = generate_config_files(
        group_name=group_name,
        root_nickname=root_nickname,
        checks=json.loads(checks),
        language=get_group_language(api_token, group_name) or "EN",
        working_dir=working_dir,
        token=api_token,
        retry_number=retry_number,
    )
    os.makedirs(f"{working_dir}/execution_configs", exist_ok=True)
    os.makedirs(f"{working_dir}/execution_results", exist_ok=True)

    for config in configs:
        with open(
            (
                f"{working_dir}/execution_configs"
                f"/{config['execution_id']}.yaml"
            ),
            "w",
            encoding="utf-8",
        ) as handler:
            yaml.safe_dump(config, handler)


@cli.command()
@click.option(
    "--execution-id",
    required=True,
)
def submit_task(execution_id: str) -> None:
    client = boto3.client("sqs")
    client.send_message(
        QueueUrl=(
            "https://sqs.us-east-1.amazonaws.com/205810638802/"
            "integrates_report"
        ),
        MessageBody=json.dumps(
            {
                "id": execution_id,
                "task": "report",
                "args": [execution_id],
            }
        ),
    )
    sys.exit(0)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
