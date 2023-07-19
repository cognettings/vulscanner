from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
from fa_purity import (
    Result,
    ResultE,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
)


class StatefullStreams(Enum):
    MRS_CLOSED = "MRS_CLOSED"
    MRS_MERGED = "MRS_MERGED"
    PIPE_JOBS_SUCCESS = "PIPE_JOBS_SUCCESS"
    PIPE_JOBS_FAILED = "PIPE_JOBS_FAILED"
    PIPE_JOBS_CANCELED = "PIPE_JOBS_CANCELED"
    PIPE_JOBS_SKIPPED = "PIPE_JOBS_SKIPPED"
    PIPE_JOBS_MANUAL = "PIPE_JOBS_MANUAL"

    @staticmethod
    def from_raw(raw: str) -> ResultE[StatefullStreams]:
        try:
            return Result.success(StatefullStreams(raw.upper()))
        except ValueError as err:
            return Result.failure(Exception(err))


class StatelessStreams(Enum):
    ISSUES = "ISSUES"
    MEMBERS = "MEMBERS"

    @staticmethod
    def from_raw(raw: str) -> ResultE[StatelessStreams]:
        try:
            return Result.success(StatelessStreams(raw.upper()))
        except ValueError as err:
            return Result.failure(Exception(err))


class SupportedStreams(Enum):
    ISSUES = "ISSUES"
    MEMBERS = "MEMBERS"
    MRS_CLOSED = "MRS_CLOSED"
    MRS_MERGED = "MRS_MERGED"
    PIPE_JOBS_SUCCESS = "PIPE_JOBS_SUCCESS"
    PIPE_JOBS_FAILED = "PIPE_JOBS_FAILED"
    PIPE_JOBS_CANCELED = "PIPE_JOBS_CANCELED"
    PIPE_JOBS_SKIPPED = "PIPE_JOBS_SKIPPED"
    PIPE_JOBS_MANUAL = "PIPE_JOBS_MANUAL"

    @staticmethod
    def from_raw(raw: str) -> ResultE[SupportedStreams]:
        try:
            return Result.success(SupportedStreams(raw.upper()))
        except ValueError as err:
            return Result.failure(Exception(err))

    def classify(self) -> Coproduct[StatefullStreams, StatelessStreams]:
        factory: CoproductFactory[
            StatefullStreams, StatelessStreams
        ] = CoproductFactory()
        return (
            StatefullStreams.from_raw(self.value)
            .map(lambda sl: factory.inl(sl))
            .lash(
                lambda _: StatelessStreams.from_raw(self.value).map(
                    lambda sl: factory.inr(sl)
                )
            )
            .unwrap()
        )
