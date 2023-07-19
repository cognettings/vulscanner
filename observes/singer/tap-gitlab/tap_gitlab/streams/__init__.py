from ._core import (
    JobStream,
    MrStream,
)
from ._decoder import (
    StreamDecoder,
)
from ._encoder import (
    StreamEncoder,
)
from ._jobs import (
    JobStreams,
)
from ._pipelines import (
    PipelineStreams,
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


def default_mr_streams(proj: ProjectId) -> Tuple[MrStream, ...]:
    return (
        MrStream(proj, MrScope.all, MrState.closed),
        MrStream(proj, MrScope.all, MrState.merged),
    )


def default_job_stream(proj: ProjectId) -> JobStream:
    scopes = (
        JobStatus.failed,
        JobStatus.success,
        JobStatus.canceled,
        JobStatus.skipped,
        JobStatus.manual,
    )
    return JobStream(proj, scopes)


__all__ = [
    "JobStream",
    "JobStreams",
    "MrStream",
    "PipelineStreams",
    "StreamDecoder",
    "StreamEncoder",
]
