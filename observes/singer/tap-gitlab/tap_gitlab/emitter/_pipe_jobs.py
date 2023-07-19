from __future__ import (
    annotations,
)

from ._emitter import (
    StreamEmitter,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
    timedelta,
)
from fa_purity import (
    Cmd,
    Maybe,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.stream.transform import (
    chain,
)
import sys
from tap_gitlab.api.core.ids import (
    PipelineId,
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
)
from tap_gitlab.api.jobs import (
    JobObj,
)
from tap_gitlab.intervals import (
    ChainedOpenLeft,
    FragmentedProgressInterval,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    MIN,
)
from tap_gitlab.singer.jobs import (
    schemas as jobs_schemas,
)
from tap_gitlab.singer.jobs.records import (
    job_encode,
)
from tap_gitlab.singer.state import (
    state_to_singer,
)
from tap_gitlab.state import (
    EtlState,
    PipeJobsStreamKey,
    PipelineJobsState,
)
from tap_gitlab.state.default import (
    NOW,
)
from tap_gitlab.streams import (
    pipe_jobs,
)
from typing import (
    IO,
    Tuple,
)


@dataclass(frozen=True)
class PipeJobsEmitter:
    _target: IO[str]
    _project: ProjectId
    _page_limit: int
    _stream_key: PipeJobsStreamKey
    _client: HttpJsonClient

    def _to_full_state(
        self,
        state: EtlState,
        pipe_jobs_state: FragmentedProgressInterval[datetime],
    ) -> EtlState:
        pipe_jobs = {k: v for k, v in state.pipeline_jobs.items()}
        pipe_jobs[self._stream_key] = PipelineJobsState(pipe_jobs_state)
        return EtlState(freeze(pipe_jobs), state.mrs)

    def _extract_state(
        self,
        state: EtlState,
    ) -> FragmentedProgressInterval[datetime]:
        default = FragmentedProgressInterval.new(
            ChainedOpenLeft.from_intervals(
                (
                    IntervalFactory.datetime_default().new_left_open(
                        MIN(), NOW - timedelta(microseconds=1)
                    ),
                )
            ).unwrap(),
            (False,),
        ).unwrap()
        return (
            Maybe.from_optional(state.pipeline_jobs.get(self._stream_key))
            .map(lambda s: s.state)
            .value_or(default)
        )

    def _streamer(
        self,
    ) -> StreamEmitter[
        EtlState,
        FragmentedProgressInterval[datetime],
        Stream[Tuple[PipelineId, JobObj]],
    ]:
        return StreamEmitter(
            sys.stdout,
            state_to_singer,
            lambda s: s.map(
                lambda j: job_encode(self._project, j[0], j[1])
            ).transform(lambda x: chain(x)),
            self._extract_state,
            self._to_full_state,
            lambda s: pipe_jobs.PipeJobStreams(
                self._client, self._project, self._page_limit, s
            ).stream(self._stream_key.status),
        )

    def _append_now(self, state: EtlState) -> EtlState:
        extracted = self._extract_state(state)
        return self._to_full_state(state, extracted.append(NOW).unwrap())

    def emit(self, init: EtlState) -> Cmd[EtlState]:
        streamer = self._streamer()
        return streamer.emit_schemas(
            jobs_schemas.all_schemas()
        ) + streamer.emit(self._append_now(init))
