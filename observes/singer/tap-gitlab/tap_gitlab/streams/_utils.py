from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    PureIter,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab._utils.mutable import (
    Mutable,
)
from tap_gitlab.api.http_json_client import (
    Page,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")
_Seg = TypeVar("_Seg")
_State = TypeVar("_State")


def is_empty_list(items: FrozenList[_T]) -> Maybe[FrozenList[_T]]:
    return Maybe.from_optional(items if items else None)


@dataclass(frozen=True)
class GenericStream:
    _start_page: int
    _per_page: int

    def generic_stream(
        self,
        get_page: Callable[[Page], Cmd[_T]],
        is_empty: Callable[[_T], Maybe[_T]],
    ) -> Stream[_T]:
        return (
            infinite_range(self._start_page, 1)
            .map(lambda i: Page.new_page(i, self._per_page).unwrap())
            .map(get_page)
            .transform(lambda x: from_piter(x))
            .map(is_empty)
            .transform(until_empty)
        )

    def generic_page_stream(
        self,
        get_page: Callable[[Page], Cmd[FrozenList[_T]]],
        is_empty: Callable[[FrozenList[_T]], Maybe[FrozenList[_T]]],
    ) -> Stream[_T]:
        return (
            self.generic_stream(
                get_page,
                is_empty,
            )
            .map(lambda x: from_flist(x))
            .transform(lambda x: chain(x))
        )

    @staticmethod
    def is_empty(items: FrozenList[_T]) -> Maybe[FrozenList[_T]]:
        return is_empty_list(items)


@dataclass(frozen=True)
class _LabeledItem(Generic[_T, _Seg]):
    item: _T
    segment: _Seg
    forzed_end: bool
    # True when the item is the last item of a stream
    # because of a forced limit, and not due to the stream end


@dataclass(frozen=True)
class SegmentsStream(Generic[_Seg, _State, _T]):
    """
    - paginates over `get_segment` until an element is empty up to `is_empty`
    - chains all pagination over each segment provided i.e. `segments`
    - appends a state at each end of a segment pagination, calculated by the
    `new_state` function
    - limits total emitted pages to `page_limit`
    - When limit is reached stream stops and emits an interrupted state,
    calculated by the `interrupted_state` function
    """

    _segments: PureIter[_Seg]
    _init: _State
    _page_limit: int
    _per_page: int
    _get_segment: Callable[[_Seg, Page], Cmd[_T]]
    _is_empty: Callable[[_T], Maybe[_T]]
    _new_state: Callable[[_State, _Seg], _State]
    _interrupted_state: Callable[[_State, _Seg, _T], _State]
    _mutable_state: Mutable[_State]  # handles current streamer state
    _streamed_pages: Mutable[int]  # handles total emitted pages counter

    @staticmethod
    def new(
        segments: PureIter[_Seg],
        init: _State,
        page_limit: int,
        per_page: int,
        get_segment: Callable[[_Seg, Page], Cmd[_T]],
        is_empty: Callable[[_T], Maybe[_T]],
        new_state: Callable[[_State, _Seg], _State],
        interrupted_state: Callable[[_State, _Seg, _T], _State],
    ) -> Cmd[SegmentsStream[_Seg, _State, _T]]:
        """
        - segments: that will be streamed
        - init: initial state
        - page_limit: limit max emitted pages
        - per_page: items per page
        - get_segment: item getter as function of the
        segment and the page
        - is_empty: empty page detector/handler
        - new_state: function for calculating the next
        state after a segment has been streamed
        - interrupted_state: function for calculating
        the next state after a segment stream has been
        interrupted because page limit. This is a function
        of the last state, segment and item.
        """
        state = Mutable.new(init)
        streamed_pages = Mutable.new(0)
        return state.bind(
            lambda s: streamed_pages.map(
                lambda sp: SegmentsStream(
                    segments,
                    init,
                    page_limit,
                    per_page,
                    get_segment,
                    is_empty,
                    new_state,
                    interrupted_state,
                    s,
                    sp,
                )
            )
        )

    def _get_labeled(
        self, seg: _Seg, page: Page
    ) -> Cmd[_LabeledItem[_T, _Seg]]:
        """
        Label item with the corresponding segment and end flag.
        End flag triggered when page limit is reached.
        """
        increase = self._streamed_pages.mutate(lambda x: x + 1)
        is_less_than_limit = self._streamed_pages.get().map(
            lambda p: p < self._page_limit
        )
        return increase + is_less_than_limit.bind(
            lambda b: self._get_segment(seg, page).map(
                lambda t: _LabeledItem(t, seg, not b)
            )
        )

    def _paginate_segment(self, seg: _Seg) -> Stream[_LabeledItem[_T, _Seg]]:
        """
        Paginate labeled items until:
        - not empty **up to** _is_empty
        - or page limit reached
        """
        return (
            from_range(range(1, self._page_limit + 1))
            .map(lambda i: Page.new_page(i, self._per_page).unwrap())
            .map(lambda p: self._get_labeled(seg, p))
            .transform(lambda x: from_piter(x))
            .map(lambda i: self._is_empty(i.item).map(lambda _: i))
            .transform(until_empty)
        )

    def _interrupt_state(
        self, last: Coproduct[_LabeledItem[_T, _Seg], _State]
    ) -> Maybe[Cmd[_State]]:
        empty: Maybe[Cmd[_State]] = Maybe.empty()
        return last.map(
            lambda i: Maybe.from_optional(
                self._mutable_state.get().map(
                    lambda s: self._interrupted_state(s, i.segment, i.item)
                )
                if i.forzed_end
                else None
            ),
            lambda _: empty,
        )

    def _append_state(
        self,
    ) -> Stream[Coproduct[_LabeledItem[_T, _Seg], _State]]:
        """
        Append a new state at each segment pagination end.
        The new state is calculated with the `new_state` function; the state
        input is a previous calculated state or the `init` state as default.
        """
        factory: CoproductFactory[
            _LabeledItem[_T, _Seg], _State
        ] = CoproductFactory()
        return self._segments.map(
            lambda seg: _utils.append_to_stream(
                self._paginate_segment(seg).map(lambda x: factory.inl(x)),
                lambda _: Maybe.from_value(
                    self._mutable_state.mutate(
                        lambda prev: self._new_state(prev, seg)
                    )
                    + self._mutable_state.get().map(lambda x: factory.inr(x))
                ),
            )
        ).transform(lambda x: chain(x))

    def stream(self) -> Stream[Coproduct[_T, _State]]:
        # Append interrupted state if last streamed item has the end flag.
        def _append(
            last: Maybe[Coproduct[_LabeledItem[_T, _Seg], _State]]
        ) -> Maybe[Cmd[Coproduct[_LabeledItem[_T, _Seg], _State]]]:
            return last.bind(
                lambda x: self._interrupt_state(x).map(
                    lambda c: c.map(lambda s: Coproduct.inr(s))
                ),
            )

        # stream until forzed_end flag found (inclusive)
        result = _utils.append_to_stream(
            _utils.until_condition(
                self._append_state(),
                lambda u: u.map(lambda i: i.forzed_end, lambda _: False),
            ),
            _append,
        )
        # Clean data stream by un-labeling items
        return result.map(
            lambda u: u.map(
                lambda i: Coproduct.inl(i.item),
                lambda st: Coproduct.inr(st),
            )
        )
