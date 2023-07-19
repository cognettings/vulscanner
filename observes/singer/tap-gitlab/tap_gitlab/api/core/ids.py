from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from tap_gitlab import (
    _utils,
)
from urllib.parse import (
    quote,
    unquote,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class CommitHash:
    hash_str: str


@dataclass(frozen=True)
class EpicId:
    global_id: int
    internal_id: int


@dataclass(frozen=True)
class IssueId:
    global_id: int
    internal_id: int


@dataclass(frozen=True)
class JobId:
    job_id: int


@dataclass(frozen=True)
class MilestoneId:
    global_id: int
    internal_id: int


@dataclass(frozen=True)
class ProjectId:
    _private: _Private = field(repr=False, hash=False, compare=False)
    _proj_id: str | int

    @staticmethod
    def from_name(name: str) -> ProjectId:
        return ProjectId(_Private(), quote(name, safe=""))

    @staticmethod
    def from_id(proj_id: int) -> ProjectId:
        return ProjectId(_Private(), proj_id)

    @classmethod
    def from_raw_str(cls, proj: str) -> ProjectId:
        _proj = _utils.str_to_int(proj).value_or(proj)
        if isinstance(_proj, int):
            return cls.from_id(_proj)
        return cls.from_name(_proj)

    @property
    def str_val(self) -> str:
        if isinstance(self._proj_id, str):
            return self._proj_id
        return _utils.int_to_str(self._proj_id)

    @property
    def raw(self) -> str | int:
        if isinstance(self._proj_id, str):
            return unquote(self._proj_id)
        return self._proj_id


@dataclass(frozen=True)
class PipelineId:
    global_id: int


@dataclass(frozen=True)
class PipelineRelativeId:
    project: ProjectId
    internal_id: int


@dataclass(frozen=True)
class RunnerId:
    runner_id: int


@dataclass(frozen=True)
class UserId:
    user_id: int
