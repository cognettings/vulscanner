from __future__ import (
    annotations,
)

from ._chained import (
    ChainedOpenLeft,
)
from dataclasses import (
    dataclass,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveFactory,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
)
from tap_gitlab.intervals.interval import (
    IntervalPoint,
    MAX,
    MIN,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from typing import (
    Callable,
    Dict,
    Generic,
    TypeVar,
)

_P = TypeVar("_P")
_prim = JsonPrimitiveFactory.from_raw
_prim_val = JsonValue.from_primitive
_json = JsonValue.from_json


@dataclass(frozen=True)
class IntervalEncoder(
    Generic[_P],
):
    _encode_point: Callable[[_P], JsonObj]

    @staticmethod
    def new(
        encode_point: Callable[[_P], JsonObj],
    ) -> IntervalEncoder[_P]:
        return IntervalEncoder(encode_point)

    def encode_point(self, point: _P) -> JsonObj:
        return self._encode_point(point)

    def encode_ipoint(self, point: IntervalPoint[_P]) -> JsonObj:
        encoded = (
            _prim_val(_prim(str(point)))
            if isinstance(point, (MAX, MIN))
            else _json(self.encode_point(point))
        )
        encoded_obj = freeze({"point": encoded})
        raw: Dict[str, JsonValue] = {
            "type": _prim_val(_prim("IntervalPoint")),
            "obj": _json(encoded_obj),
        }
        return freeze(raw)

    def encode_chained_ol(self, interval: ChainedOpenLeft[_P]) -> JsonObj:
        encoded_obj = freeze(
            {
                "endpoints": JsonValue.from_list(
                    tuple(
                        _json(self.encode_ipoint(point))
                        for point in interval.endpoints
                    )
                )
            }
        )
        return freeze(
            {
                "type": _prim_val(_prim("ChainedOpenLeft")),
                "obj": _json(encoded_obj),
            }
        )

    def encode_f_progress(
        self, interval: FragmentedProgressInterval[_P]
    ) -> JsonObj:
        encoded_obj = freeze(
            {
                "f_interval": _json(
                    self.encode_chained_ol(interval.f_interval)
                ),
                "completeness": JsonValue.from_list(
                    tuple(_prim_val(_prim(c)) for c in interval.completeness)
                ),
            }
        )
        return freeze(
            {
                "type": _prim_val(_prim("FragmentedProgressInterval")),
                "obj": _json(encoded_obj),
            }
        )
