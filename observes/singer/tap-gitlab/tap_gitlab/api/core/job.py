from __future__ import (
    annotations,
)

from .ids import (
    CommitHash,
    JobId,
    RunnerId,
    UserId,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenList,
    Maybe,
    Result,
    ResultE,
)


@dataclass(frozen=True)
class JobDates:
    created_at: datetime
    started_at: Maybe[datetime]
    finished_at: Maybe[datetime]


@dataclass(frozen=True)
class JobConf:
    allow_failure: bool
    tag_list: FrozenList[str]
    ref_branch: str
    stage: str


class JobStatus(Enum):
    created = "created"
    pending = "pending"
    running = "running"
    failed = "failed"
    success = "success"
    canceled = "canceled"
    skipped = "skipped"
    waiting_for_resource = "waiting_for_resource"
    manual = "manual"

    @staticmethod
    def from_raw(raw: str) -> ResultE[JobStatus]:
        try:
            return Result.success(JobStatus(raw))
        except ValueError as err:
            return Result.failure(Exception(err))


@dataclass(frozen=True)
class JobResultStatus:
    status: str
    failure_reason: Maybe[str]
    duration: Maybe[Decimal]
    queued_duration: Maybe[Decimal]


@dataclass(frozen=True)
class Job:
    name: str
    user_id: UserId
    runner_id: Maybe[RunnerId]
    coverage: Maybe[float]
    commit: CommitHash
    dates: JobDates
    conf: JobConf
    result: JobResultStatus


__all__ = [
    "JobId",
]
