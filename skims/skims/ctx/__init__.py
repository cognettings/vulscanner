import os
from os import (
    environ,
    makedirs,
)
from os.path import (
    expanduser,
)
from typing import (
    Any,
)

# Constants
SKIMS_CONFIG: Any
STATE_FOLDER: str = expanduser("~/.skims")
STATE_FOLDER_DEBUG: str = os.path.join(STATE_FOLDER, "debug")
NAMESPACES_FOLDER: str = os.path.join(STATE_FOLDER, "namespaces")


def _get_artifact(env_var: str) -> str:
    if value := environ.get(env_var):
        return value
    raise ValueError(f"Expected environment variable: {env_var}")


# Side effects
CIPHER_SUITES_PATH: str = _get_artifact("SKIMS_CIPHER_SUITES_PATH")
CRITERIA_REQUIREMENTS: str = _get_artifact("SKIMS_CRITERIA_REQUIREMENTS")
CRITERIA_VULNERABILITIES: str = _get_artifact("SKIMS_CRITERIA_VULNERABILITIES")
LEGAL = _get_artifact("SKIMS_LEGAL")
STATIC = _get_artifact("SKIMS_STATIC")
TREE_SITTER_PARSERS = _get_artifact("SKIMS_TREE_SITTER_PARSERS")

DB_MODEL_PATH = _get_artifact("SKIMS_DB_MODEL_PATH")
# not secrets but must be environment vars
AWS_REGION_NAME = "us-east-1"


makedirs(STATE_FOLDER, mode=0o700, exist_ok=True)
makedirs(STATE_FOLDER_DEBUG, mode=0o700, exist_ok=True)
makedirs(NAMESPACES_FOLDER, mode=0o700, exist_ok=True)
