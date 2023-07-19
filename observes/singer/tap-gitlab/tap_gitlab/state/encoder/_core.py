from datetime import (
    datetime,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
    JsonPrimitiveFactory,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
)
from tap_gitlab.intervals.encoder import (
    IntervalEncoder,
)
from tap_gitlab.state._objs import (
    EncodedObj,
)
from tap_gitlab.streams import (
    StreamEncoder,
)
from typing import (
    Callable,
    TypeVar,
)

_prim = JsonPrimitiveFactory.from_raw
_prim_val = JsonValue.from_primitive
_K = TypeVar("_K")
_V = TypeVar("_V")


def encode_obj(item: EncodedObj) -> JsonObj:
    return freeze(
        {
            "type": _prim_val(_prim(item.obj_type)),
            "obj": item.encoded,
        }
    )


def encode_dict(
    item: FrozenDict[_K, _V],
    encode_key: Callable[[_K], JsonValue],
    encode_value: Callable[[_V], JsonValue],
) -> EncodedObj:
    """
    Generic key type `FrozenDict[_K, _V]` encoder.
    This overcomes the limitation of `JsonObj` for string only keys.
    """
    encoded_obj = tuple(
        JsonValue.from_list((encode_key(k), encode_value(v)))
        for k, v in item.items()
    )
    return EncodedObj("FrozenDict", JsonValue.from_list(encoded_obj))


def encode_datetime(time: datetime) -> JsonObj:
    return freeze(
        {
            "datetime": JsonValue.from_primitive(
                JsonPrimitive.from_str(time.isoformat())
            )
        }
    )


i_encoder: IntervalEncoder[datetime] = IntervalEncoder.new(encode_datetime)
stm_encoder = StreamEncoder()
