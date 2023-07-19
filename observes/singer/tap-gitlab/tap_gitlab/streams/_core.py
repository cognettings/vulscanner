from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.jobs import (
    JobStatus,
)
from tap_gitlab.api.merge_requests import (
    Scope as MrScope,
    State as MrState,
)
from typing import (
    Tuple,
)


@dataclass(frozen=True)
class MrStream:
    project: ProjectId
    scope: MrScope
    mr_state: MrState


@dataclass(frozen=True)
class JobStream:
    project: ProjectId
    scopes: Tuple[JobStatus, ...]
