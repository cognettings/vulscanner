from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    FrozenDict,
    ResultE,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
from fa_purity.json.value.core import (
    JsonValue,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_singer_io.singer import (
    SingerRecord,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class PlainRecord:
    _private: _Private = field(repr=False, hash=False, compare=False)
    stream: str
    record: FrozenDict[str, Primitive]

    @staticmethod
    def from_singer(record: SingerRecord) -> ResultE[PlainRecord]:
        items = (
            Unfolder(JsonValue(record.record))
            .to_unfolder_dict()
            .map(lambda d: tuple(d.items()))
            .map(
                lambda t: tuple(
                    pure_map(
                        lambda p: p[1]
                        .to_any_primitive()
                        .map(lambda x: (p[0], x)),
                        t,
                    )
                )
            )
            .alt(Exception)
            .bind(lambda x: all_ok(x))
            .map(lambda x: FrozenDict(dict(x)))
        )
        return items.map(lambda d: PlainRecord(_Private(), record.stream, d))

    @staticmethod
    def new(stream: str, record: FrozenDict[str, Primitive]) -> PlainRecord:
        return PlainRecord(_Private(), stream, record)
