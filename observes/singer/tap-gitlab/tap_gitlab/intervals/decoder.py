from ._chained import (
    ChainedOpenLeft,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
    ResultE,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
    Unfolder,
)
from fa_purity.result.transform import (
    all_ok,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    IntervalPoint,
    MAX,
    MIN,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_P = TypeVar("_P")


@dataclass(frozen=True)
class IntervalDecoder(
    Generic[_P],
):
    factory: IntervalFactory[_P]
    decode_point: Callable[[JsonValue], ResultE[_P]]

    def decode_ipoint(self, raw: JsonObj) -> ResultE[IntervalPoint[_P]]:
        def _to_interval(item: IntervalPoint[_P]) -> IntervalPoint[_P]:
            return item

        def _min_max(item: str) -> ResultE[IntervalPoint[_P]]:
            if item == "MIN":
                return Result.success(_to_interval(MIN()))
            elif item == "MAX":
                return Result.success(_to_interval(MAX()))
            return Result.failure(Exception("Not MIN nor MAX"))

        def _decode(item: JsonValue) -> ResultE[IntervalPoint[_P]]:
            return (
                Unfolder.to_primitive(item)
                .bind(JsonPrimitiveUnfolder.to_str)
                .bind(_min_max)
                .lash(lambda _: self.decode_point(item).map(_to_interval))
            )

        _type = decode.require_restricted_str(raw, "type", ("IntervalPoint",))
        _point = (
            decode.require_key(raw, "obj")
            .bind(Unfolder.to_json)
            .bind(lambda j: decode.require_key(j, "point"))
            .bind(lambda x: _decode(x))
        )
        return _type.bind(lambda _: _point)

    def decode_chained_ol(self, raw: JsonObj) -> ResultE[ChainedOpenLeft[_P]]:
        _type = decode.require_restricted_str(
            raw,
            "type",
            (
                "ChainedOpenLeft",
                "FragmentedInterval",
            ),
        )
        _endpoints = (
            decode.require_key(raw, "obj")
            .bind(Unfolder.to_json)
            .bind(
                lambda j: decode.require_key(j, "endpoints")
                .bind(Unfolder.to_list)
                .bind(
                    lambda items: all_ok(
                        tuple(
                            Unfolder.to_json(i).bind(self.decode_ipoint)
                            for i in items
                        )
                    )
                )
            )
        )
        return _type.bind(
            lambda _: _endpoints.bind(
                lambda e: ChainedOpenLeft.new(self.factory.greater, e)
            )
        )

    def decode_f_progress(
        self, raw: JsonObj
    ) -> ResultE[FragmentedProgressInterval[_P]]:
        _type = decode.require_restricted_str(
            raw, "type", ("FragmentedProgressInterval",)
        )
        _interval = (
            decode.require_key(raw, "obj")
            .bind(Unfolder.to_json)
            .bind(
                lambda j: decode.require_key(j, "f_interval")
                .bind(Unfolder.to_json)
                .bind(self.decode_chained_ol)
            )
        )
        _completeness = (
            decode.require_key(raw, "obj")
            .bind(Unfolder.to_json)
            .bind(
                lambda j: decode.require_key(j, "completeness").bind(
                    lambda v: Unfolder.to_list_of(
                        v,
                        lambda x: Unfolder.to_primitive(x).bind(
                            JsonPrimitiveUnfolder.to_bool
                        ),
                    )
                )
            )
        )

        return _type.bind(
            lambda _: _interval.bind(
                lambda i: _completeness.bind(
                    lambda c: FragmentedProgressInterval.new(i, c)
                )
            )
        )
