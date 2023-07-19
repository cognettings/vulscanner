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
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Maybe,
    Stream,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_purity.union import (
    Coproduct,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
    Page,
)
from tap_gitlab.api.merge_requests import (
    MrFilter,
    MrsClient,
    OrderBy,
    Scope,
    Sort,
    State,
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


class InvalidPage(Exception):
    pass


@dataclass(frozen=True)
class MrsPage:
    data: FrozenList[JsonObj]

    @property
    def min_updated_at(self) -> datetime:
        return isoparse(
            Unfolder(self.data[-1]["updated_at"]).to_primitive(str).unwrap()
        )

    @property
    def max_updated_at(self) -> datetime:
        return isoparse(
            Unfolder(self.data[0]["updated_at"]).to_primitive(str).unwrap()
        )


StreamOut = Cmd[
    Stream[
        Coproduct[
            MrsPage,
            FragmentedProgressInterval[datetime],
        ]
    ]
]


@dataclass(frozen=True)
class _MrStreams:
    _client: HttpJsonClient
    proj: ProjectId
    _per_page: int
    _scope: Maybe[Scope]
    _state: Maybe[State]

    def _updated_between_client(
        self, after: datetime | None, before: datetime
    ) -> MrsClient:
        _filter = MrFilter(
            Maybe.from_optional(after),
            Maybe.from_value(before),
            self._scope,
            self._state,
            Maybe.from_value(OrderBy.updated_at),
            Maybe.from_value(Sort.descendant),
        )
        return MrsClient(self._client, self.proj, Maybe.from_value(_filter))

    def stream_fragmented(
        self,
        fragments: FragmentedProgressInterval[datetime],
        page_limit: int,
    ) -> StreamOut:
        def get_segment(
            interval: ProgressInterval[OpenLeftInterval[datetime]], page: Page
        ) -> Cmd[MrsPage]:
            client = self._updated_between_client(
                None
                if isinstance(interval.interval.lower, MIN)
                else interval.interval.lower,
                interval.interval.upper,
            )
            return client.mrs_page(page).map(MrsPage)

        def _new_state(
            prev: FragmentedProgressInterval[datetime],
            seg: ProgressInterval[OpenLeftInterval[datetime]],
        ) -> FragmentedProgressInterval[datetime]:
            return prev.change_completeness(seg.interval, True)

        def _interrupted_state(
            prev: FragmentedProgressInterval[datetime],
            seg: ProgressInterval[OpenLeftInterval[datetime]],
            item: MrsPage,
        ) -> FragmentedProgressInterval[datetime]:
            lower = item.min_updated_at
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

        segments = from_flist(fragments.progress_intervals).filter(
            lambda i: not i.completed
        )

        new_stream: Cmd[
            SegmentsStream[
                ProgressInterval[OpenLeftInterval[datetime]],
                FragmentedProgressInterval[datetime],
                MrsPage,
            ]
        ] = SegmentsStream.new(
            segments,
            fragments,
            page_limit,
            self._per_page,
            get_segment,
            lambda mp: GenericStream.is_empty(mp.data).map(lambda _: mp),
            _new_state,
            _interrupted_state,
        )
        return new_stream.map(lambda s: s.stream())


def closed_mrs(
    client: HttpJsonClient,
    proj: ProjectId,
    page_limit: int,
    state: FragmentedProgressInterval[datetime],
) -> StreamOut:
    return _MrStreams(
        client,
        proj,
        100,
        Maybe.from_value(Scope.all),
        Maybe.from_value(State.closed),
    ).stream_fragmented(state, page_limit)


def merged_mrs(
    client: HttpJsonClient,
    proj: ProjectId,
    page_limit: int,
    state: FragmentedProgressInterval[datetime],
) -> StreamOut:
    return _MrStreams(
        client,
        proj,
        100,
        Maybe.from_value(Scope.all),
        Maybe.from_value(State.merged),
    ).stream_fragmented(state, page_limit)
