from __future__ import (
    annotations,
)

from .ids import (
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
    Maybe,
    Result,
    ResultE,
)


class PipelineStatus(Enum):
    created = "created"
    waiting_for_resource = "waiting_for_resource"
    preparing = "preparing"
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
    canceled = "canceled"
    skipped = "skipped"
    manual = "manual"
    scheduled = "scheduled"

    @staticmethod
    def from_raw(raw: str) -> ResultE[PipelineStatus]:
        try:
            return Result.success(PipelineStatus(raw))
        except ValueError as err:
            return Result.failure(Exception(err))


@dataclass(frozen=True)
class Pipeline:
    sha: str
    before_sha: Maybe[str]
    ref: str
    status: PipelineStatus
    source: str
    duration: Maybe[Decimal]
    queued_duration: Maybe[Decimal]
    user: UserId
    created_at: datetime
    updated_at: Maybe[datetime]
    started_at: Maybe[datetime]
    finished_at: Maybe[datetime]
