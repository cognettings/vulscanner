from . import (
    _core,
)
from datetime import (
    datetime,
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
from tap_gitlab.intervals.encoder import (
    IntervalEncoder,
)
from tap_gitlab.state._objs import (
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.streams import (
    StreamEncoder,
)

_prim = JsonPrimitiveFactory.from_raw
_prim_val = JsonValue.from_primitive
_json = JsonValue.from_json


def encode_mr_stm_state(state: MrStreamState) -> JsonObj:
    encoded_obj = freeze(
        {
            "state": _json(_core.i_encoder.encode_f_progress(state.state)),
        }
    )
    return freeze(
        {
            "type": _prim_val(_prim("MrStreamState")),
            "obj": _json(encoded_obj),
        }
    )


def encode_mrstate_map(state: MrStateMap) -> JsonObj:
    encoded_obj = freeze(
        {
            "items": JsonValue.from_list(
                tuple(
                    JsonValue.from_list(
                        (
                            _json(_core.stm_encoder.encode_mr_stream(stm)),
                            _json(encode_mr_stm_state(item)),
                        )
                    )
                    for stm, item in state.items.items()
                )
            ),
        }
    )
    return freeze(
        {"type": _prim_val(_prim("MrStateMap")), "obj": _json(encoded_obj)}
    )
