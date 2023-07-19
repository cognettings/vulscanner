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
)
from fa_purity import (
    Cmd,
    Maybe,
    ResultE,
    Stream,
)
from fa_purity.union import (
    Coproduct,
)
import sys
from tap_gitlab import (
    _utils,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
)
from tap_gitlab.api.merge_requests import (
    Scope as MrScope,
    State as MrState,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from tap_gitlab.singer.mrs.records import (
    mr_record,
)
from tap_gitlab.singer.state import (
    state_to_singer,
)
from tap_gitlab.state import (
    EtlState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.state.default import (
    NOW,
)
from tap_gitlab.streams import (
    mrs as mr_streams,
    MrStream,
)
from tap_gitlab.streams.mrs import (
    MrsPage,
)
from typing import (
    Callable,
    IO,
)


def _extract_mr_stream_state(
    state: EtlState, stream: MrStream
) -> Maybe[FragmentedProgressInterval[datetime]]:
    return Maybe.from_optional(state.mrs.items.get(stream)).map(
        lambda s: s.state
    )


def _mr_stream_state_to_full(
    stream: MrStream,
    state: EtlState,
    mr_state: FragmentedProgressInterval[datetime],
) -> EtlState:
    mrs = {k: v for k, v in state.mrs.items.items()}
    mrs[stream] = MrStreamState(mr_state)
    return EtlState(state.pipeline_jobs, MrStateMap(mrs))


def _append_now_mr_state(
    state: EtlState, stream: MrStream
) -> ResultE[EtlState]:
    mrs = (
        Maybe.from_optional(state.mrs.items.get(stream))
        .to_result()
        .alt(lambda _: Exception(KeyError(stream)))
    )
    return mrs.map(
        lambda m: _mr_stream_state_to_full(
            stream, state, m.state.append(NOW).unwrap()
        )
    )


@dataclass(frozen=True)
class MrsEmitter:
    _target: IO[str]
    _project: ProjectId
    _page_limit: int

    def _base_emitter(
        self,
        _extract: Callable[[EtlState], FragmentedProgressInterval[datetime]],
        _override: Callable[
            [EtlState, FragmentedProgressInterval[datetime]], EtlState
        ],
        _stream: Callable[
            [FragmentedProgressInterval[datetime]],
            Stream[Coproduct[MrsPage, FragmentedProgressInterval[datetime]]],
        ],
    ) -> StreamEmitter[
        EtlState,
        FragmentedProgressInterval[datetime],
        MrsPage,
    ]:
        return StreamEmitter(
            sys.stdout,
            state_to_singer,
            lambda p: _utils.to_stream(mr_record(p)),
            _extract,
            _override,
            _stream,
        )

    def closed_stream_emitter(
        self,
        client: HttpJsonClient,
        init: EtlState,
    ) -> Cmd[EtlState]:
        mr_stream = MrStream(self._project, MrScope.all, MrState.closed)

        def _stream(
            state: FragmentedProgressInterval[datetime],
        ) -> Stream[Coproduct[MrsPage, FragmentedProgressInterval[datetime]]]:
            return _utils.squash_cmd_stream(
                mr_streams.closed_mrs(
                    client, self._project, self._page_limit, state
                )
            )

        emitter = self._base_emitter(
            lambda s: _extract_mr_stream_state(
                s, mr_stream
            ).unwrap(),  # Use default value
            lambda f, s: _mr_stream_state_to_full(mr_stream, f, s),
            _stream,
        )
        return emitter.emit(_append_now_mr_state(init, mr_stream).unwrap())

    def merged_stream_emitter(
        self,
        client: HttpJsonClient,
        init: EtlState,
    ) -> Cmd[EtlState]:
        mr_stream = MrStream(self._project, MrScope.all, MrState.merged)

        def _stream(
            state: FragmentedProgressInterval[datetime],
        ) -> Stream[Coproduct[MrsPage, FragmentedProgressInterval[datetime]]]:
            return _utils.squash_cmd_stream(
                mr_streams.merged_mrs(
                    client, self._project, self._page_limit, state
                )
            )

        emitter = self._base_emitter(
            lambda s: _extract_mr_stream_state(
                s, mr_stream
            ).unwrap(),  # Use default value
            lambda f, s: _mr_stream_state_to_full(mr_stream, f, s),
            _stream,
        )
        return emitter.emit(_append_now_mr_state(init, mr_stream).unwrap())
