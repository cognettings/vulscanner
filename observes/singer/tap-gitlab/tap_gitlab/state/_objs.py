from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity.json_2.value import (
    JsonValue,
)
from tap_gitlab.api.core.job import (
    JobStatus,
)
from tap_gitlab.api.core.pipeline import (
    PipelineStatus,
)
from tap_gitlab.api.jobs import (
    JobsFilter,
)
from tap_gitlab.api.pipelines import (
    PipelineFilter,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from tap_gitlab.streams import (
    MrStream,
)
from typing import (
    Dict,
    FrozenSet,
    Generic,
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class EncodedObj:
    obj_type: str
    encoded: JsonValue


@dataclass(frozen=True)
class PageId(Generic[_T]):
    page: _T
    per_page: int


@dataclass(frozen=True)
class MrStreamState:
    state: FragmentedProgressInterval[datetime]


@dataclass(frozen=True)
class PipelineJobsState:
    state: FragmentedProgressInterval[datetime]


@dataclass(frozen=True)
class MrStateMap:
    items: Dict[MrStream, MrStreamState]


@dataclass(frozen=True)
class PipeJobsStreamKey:
    status: PipelineStatus
    jobs_status: FrozenSet[JobStatus]


@dataclass(frozen=True)
class EtlState:
    # all in the context of a single gitlab project
    pipeline_jobs: FrozenDict[PipeJobsStreamKey, PipelineJobsState]
    mrs: MrStateMap
