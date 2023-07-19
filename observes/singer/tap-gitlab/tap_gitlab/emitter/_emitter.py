from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
    Stream,
)
from fa_purity.pure_iter.transform import (
    consume as piter_consume,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_purity.union import (
    Coproduct,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from tap_gitlab._utils.mutable import (
    Mutable,
)
from typing import (
    Callable,
    Generic,
    IO,
    TypeVar,
)

_Item = TypeVar("_Item")
_FullState = TypeVar("_FullState")
_SpecificState = TypeVar("_SpecificState")


@dataclass(frozen=True)
class StreamEmitter(Generic[_FullState, _SpecificState, _Item]):
    """
    Generic StreamEmitter

    - _target = file for singer emitions
    - _state_encoder = state to singer state transform
    - _item_encoder = item to singer records transform
    - _extract = get _SpecificState from _FullState
    - _override = override input _FullState with input _SpecificState
    - _stream = stream of items or states for an init _SpecificState as input
    """

    _target: IO[str]
    _state_encoder: Callable[[_FullState], SingerState]
    _item_encoder: Callable[[_Item], Stream[SingerRecord]]
    _extract: Callable[[_FullState], _SpecificState]
    _override: Callable[[_FullState, _SpecificState], _FullState]
    _stream: Callable[
        [_SpecificState], Stream[Coproduct[_Item, _SpecificState]]
    ]

    def emit_schemas(self, schemas: PureIter[SingerSchema]) -> Cmd[None]:
        return schemas.map(lambda s: emitter.emit(self._target, s)).transform(
            lambda x: piter_consume(x)
        )

    def emit(self, init: _FullState) -> Cmd[_FullState]:
        _final_state = Mutable.new(init)
        return _final_state.bind(
            lambda mutable: self._stream(self._extract(init))
            .map(
                lambda u: u.map(
                    lambda i: self._item_encoder(i)
                    .map(lambda x: emitter.emit(self._target, x))
                    .transform(consume),
                    lambda s: emitter.emit(
                        self._target,
                        self._state_encoder(self._override(init, s)),
                    )
                    + mutable.update(self._override(init, s)),
                )
            )
            .transform(lambda x: consume(x))
            + mutable.get()
        )
