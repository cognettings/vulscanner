from config.typing import (
    Config,
    ConfigCI,
)
import json
from jsonschema import (
    validate,
)
from typing import (
    Any,
)

SCHEMA: dict[str, Any] = {
    "additionalProperties": False,
    "properties": {
        "ci": {
            "additionalProperties": False,
            "properties": {
                "enable": {
                    "type": "boolean",
                },
                "max_risk": {
                    "minimum": 0,
                    "type": "integer",
                },
                "platform": {
                    "enum": [
                        "gitlab",
                    ],
                    "type": "string",
                },
                "required_approvals": {
                    "minimum": 0,
                    "type": "integer",
                },
                "reviewers": {
                    "minItems": 1,
                    "type": "array",
                },
            },
            "required": [
                "enable",
                "max_risk",
                "platform",
                "required_approvals",
                "reviewers",
            ],
            "type": "object",
        },
    },
    "required": [
        "ci",
    ],
    "type": "object",
}


def load(*, path: str) -> Config:
    data: dict[str, Any] = json.loads(path)

    validate(instance=data, schema=SCHEMA)

    return Config(
        ci=ConfigCI(
            enable=data["ci"]["enable"],
            max_risk=data["ci"]["max_risk"],
            platform=data["ci"]["platform"],
            required_approvals=data["ci"]["required_approvals"],
            reviewers=data["ci"]["reviewers"],
        ),
    )
