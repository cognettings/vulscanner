from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class VulnerabilityKindEnum(Enum):
    INPUTS: str = "inputs"
    LINES: str = "lines"
    PORTS: str = "ports"


class Vulnerability(NamedTuple):
    current_state: str
    kind: VulnerabilityKindEnum
    title: str
    where: str


class ToeLines(NamedTuple):
    attacked_lines: int
    filename: str
    loc: int
    root_nickname: str
    sorts_risk_level: str
    sorts_risk_level_date: str
