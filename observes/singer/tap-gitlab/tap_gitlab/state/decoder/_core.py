from datetime import (
    datetime,
)
from dateutil import (
    parser,
)
from fa_purity import (
    FrozenDict,
    Result,
    ResultE,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.json_2.value import (
    JsonValue,
    Unfolder,
)
from tap_gitlab._utils import (
    decode,
)
from tap_gitlab.intervals.decoder import (
    IntervalDecoder,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
)
from tap_gitlab.state._objs import (
    EncodedObj,
)
from tap_gitlab.streams import (
    StreamDecoder,
)
from typing import (
    Tuple,
)


def decode_obj(item: JsonValue) -> ResultE[EncodedObj]:
    return Unfolder.to_json(item).bind(
        lambda j: decode.require_key(j, "type")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
        .bind(
            lambda t: decode.require_key(j, "obj").map(
                lambda o: EncodedObj(t, o)
            )
        )
    )


def decode_dict(
    item: EncodedObj,
) -> ResultE[FrozenDict[JsonValue, JsonValue]]:
    def _encoded_pair(
        value: JsonValue,
    ) -> ResultE[Tuple[JsonValue, JsonValue]]:
        return Unfolder.to_list(value).bind(
            lambda i: decode.require_index(i, 0).bind(
                lambda v1: decode.require_index(i, 1).map(lambda v2: (v1, v2))
            )
        )

    if item.obj_type == "FrozenDict":
        return Unfolder.to_list_of(item.encoded, _encoded_pair).map(
            lambda pairs: FrozenDict({p[0]: p[1] for p in pairs})
        )
    return Result.failure(
        Exception(f"Expected type `FrozenDict` but got `{item.obj_type}`")
    )


def decode_datetime(raw: JsonValue) -> ResultE[datetime]:
    def _decode(encoded: str) -> ResultE[datetime]:
        try:
            return Result.success(parser.parse(encoded))
        except parser.ParserError as err:
            return Result.failure(Exception(err))

    return Unfolder.to_json(raw).bind(
        lambda j: decode.require_key(j, "datetime")
        .bind(Unfolder.to_primitive)
        .bind(JsonPrimitiveUnfolder.to_str)
        .bind(_decode)
    )


i_decoder: IntervalDecoder[datetime] = IntervalDecoder(
    IntervalFactory.datetime_default(),
    decode_datetime,
)
s_decoder = StreamDecoder()
