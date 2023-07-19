from __future__ import (
    annotations,
)

from ._utils import (
    GenericStream,
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
    FrozenList,
    Maybe,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_purity.stream.transform import (
    chain as stream_chain,
)
from fa_purity.union import (
    Coproduct,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.api.core.ids import (
    PipelineRelativeId,
    ProjectId,
)
from tap_gitlab.api.core.job import (
    JobStatus,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
    Page,
)
from tap_gitlab.api.jobs import (
    JobObj,
    JobsClient,
    JobsFilter,
    JobStatus,
)
from tap_gitlab.api.pipelines import (
    OrderBy,
    PipelineClient,
    PipelineFilter,
    PipelineId,
    PipelineStatus,
    Sort,
)
from tap_gitlab.intervals.interval import (
    MIN,
    OpenLeftInterval,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
    ProgressInterval,
)
from tap_gitlab.streams._utils import (
    SegmentsStream,
)
from typing import (
    FrozenSet,
    Tuple,
)


class InvalidPage(Exception):
    pass


@dataclass(frozen=True)
class _Item:
    last_datetime: Maybe[datetime]
    jobs: Stream[Tuple[PipelineId, JobObj]]


def _new_state(
    prev: FragmentedProgressInterval[datetime],
    seg: ProgressInterval[OpenLeftInterval[datetime]],
) -> FragmentedProgressInterval[datetime]:
    return prev.change_completeness(seg.interval, True)


def _is_empty(item: _Item) -> Maybe[_Item]:
    return item.last_datetime.map(lambda _: item)


@dataclass(frozen=True)
class _PipeJobStream:
    _client: HttpJsonClient
    proj: ProjectId
    _per_page: int
    _status: Maybe[PipelineStatus]
    _scope: Maybe[FrozenSet[JobStatus]]
    _include_retried: bool

    def _updated_between_client(
        self, after: datetime | None, before: datetime
    ) -> PipelineClient:
        _filter = PipelineFilter(
            self._status,
            Maybe.from_optional(after),
            Maybe.from_value(before),
            Maybe.from_value(OrderBy.updated_at),
            Maybe.from_value(Sort.desc),
        )
        return PipelineClient(
            self._client, self.proj, Maybe.from_value(_filter)
        )

    def _jobs_client(self) -> JobsClient:
        _filter = JobsFilter(self._scope, True)
        return JobsClient(self._client, self.proj, Maybe.from_value(_filter))

    def _paginate_jobs(
        self, pipe_id: PipelineId
    ) -> Stream[Tuple[PipelineId, JobObj]]:
        result: Stream[JobObj] = GenericStream(
            1, self._per_page
        ).generic_page_stream(
            lambda p: self._jobs_client().pipeline_jobs_page(pipe_id, p),
            GenericStream.is_empty,
        )
        return result.map(lambda j: (pipe_id, j))

    def get_segment(
        self,
        interval: ProgressInterval[OpenLeftInterval[datetime]],
        page: Page,
    ) -> Cmd[_Item]:
        client = self._updated_between_client(
            None
            if isinstance(interval.interval.lower, MIN)
            else interval.interval.lower,
            interval.interval.upper,
        )

        def last_pipeline_update_at(
            pipelines: FrozenList[Tuple[PipelineId, PipelineRelativeId]]
        ) -> Cmd[Maybe[datetime]]:
            none: Cmd[Maybe[datetime]] = Cmd.from_cmd(lambda: Maybe.empty())
            return (
                decode.require_index(pipelines, -1)
                .map(
                    lambda t: client.get_updated_at(t[0]).map(
                        lambda d: Maybe.from_value(d)
                    )
                )
                .value_or(none)
            )

        return client.pipelines_ids_page(page).bind(
            lambda ids: last_pipeline_update_at(ids).map(
                lambda k: _Item(
                    k,
                    from_flist(ids)
                    .map(lambda t: t[0])
                    .map(lambda i: self._paginate_jobs(i))
                    .transform(stream_chain),
                )
            )
        )

    def _interrupted_state(
        self,
        prev: FragmentedProgressInterval[datetime],
        seg: ProgressInterval[OpenLeftInterval[datetime]],
        item: _Item,
    ) -> FragmentedProgressInterval[datetime]:
        lower = item.last_datetime.unwrap()
        lower_seg = ProgressInterval(
            OpenLeftInterval.new(
                seg.interval.greater,
                seg.interval.lower,
                lower - timedelta(microseconds=1),
            ).unwrap(),
            False,
        )
        upper_seg = ProgressInterval(
            OpenLeftInterval.new(
                seg.interval.greater,
                lower - timedelta(microseconds=1),
                seg.interval.upper,
            ).unwrap(),
            True,
        )
        intervals = (
            from_flist(prev.progress_intervals)
            .map(lambda p: (lower_seg, upper_seg) if p == seg else (p,))
            .map(lambda x: from_flist(x))
            .transform(lambda x: chain(x))
        )
        return FragmentedProgressInterval.from_progress_intervals(
            intervals.to_list()
        ).unwrap()

    def stream_fragmented(
        self,
        fragments: FragmentedProgressInterval[datetime],
        page_limit: int,
    ) -> Stream[Coproduct[_Item, FragmentedProgressInterval[datetime]]]:
        _segments = from_flist(fragments.progress_intervals).filter(
            lambda i: not i.completed
        )
        segments = from_flist(tuple(reversed(_segments.to_list())))
        # reversed to ensure that newest data goes first
        new_stream: Cmd[
            SegmentsStream[
                ProgressInterval[OpenLeftInterval[datetime]],
                FragmentedProgressInterval[datetime],
                _Item,
            ]
        ] = SegmentsStream.new(
            segments,
            fragments,
            page_limit,
            self._per_page,
            self.get_segment,
            _is_empty,
            _new_state,
            self._interrupted_state,
        )
        return _utils.squash_cmd_stream(new_stream.map(lambda s: s.stream()))


@dataclass(frozen=True)
class PipeJobStreams:
    client: HttpJsonClient
    proj: ProjectId
    page_limit: int
    state: FragmentedProgressInterval[datetime]

    def stream(
        self, status: PipelineStatus
    ) -> Stream[
        Coproduct[
            Stream[Tuple[PipelineId, JobObj]],
            FragmentedProgressInterval[datetime],
        ]
    ]:
        terminated_states = frozenset(
            [
                JobStatus.failed,
                JobStatus.success,
                JobStatus.canceled,
                JobStatus.skipped,
                JobStatus.manual,
            ]
        )
        return (
            _PipeJobStream(
                self.client,
                self.proj,
                100,
                Maybe.from_value(status),
                Maybe.from_value(terminated_states),
                True,
            )
            .stream_fragmented(self.state, self.page_limit)
            .map(
                lambda c: c.map(
                    lambda i: Coproduct.inl(i.jobs),
                    lambda s: Coproduct.inr(s),
                )
            )
        )
