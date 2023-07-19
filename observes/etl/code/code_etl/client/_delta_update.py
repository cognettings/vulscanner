from __future__ import (
    annotations,
)

from code_etl.objs import (
    CommitDataId,
    CommitStamp,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
    ResultE,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class CommitStampDiff:
    """
    Wraps two `CommitStamp` objects that share the same `CommitDataId`
    (up to CommitDataId.ignore_fa_hash_eq)
    """

    _private: _Private
    old: CommitStamp
    new: CommitStamp

    @staticmethod
    def from_stamps(
        old: CommitStamp, new: CommitStamp
    ) -> ResultE[CommitStampDiff]:
        if CommitDataId.ignore_fa_hash_eq(
            old.commit.commit_id, new.commit.commit_id
        ):
            return Result.success(CommitStampDiff(_Private(), old, new))
        error = ValueError(
            "old and new `CommitStamp` objects do not share "
            "the same `CommitDataId` (up to CommitDataId.ignore_fa_hash_eq)"
        )
        return Result.failure(Exception(error))

    def commit_hash(self) -> str:
        return self.old.commit.commit_id.hash.hash

    def is_diff(self) -> bool:
        return self.old != self.new
