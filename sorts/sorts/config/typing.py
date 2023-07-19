from typing import (
    NamedTuple,
)


class ConfigCI(NamedTuple):
    enable: bool
    max_risk: int
    platform: str
    required_approvals: int
    reviewers: list[str]


class Config(NamedTuple):
    ci: ConfigCI
