from . import (
    _core,
    _mr,
    _pipe_jobs,
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
from tap_gitlab.state._objs import (
    EtlState,
)

_prim = JsonPrimitiveFactory.from_raw
_prim_val = JsonValue.from_primitive
_json = JsonValue.from_json


def encode_etl_state(state: EtlState) -> JsonObj:
    encoded_obj = freeze(
        {
            "mrs": _json(_mr.encode_mrstate_map(state.mrs)),
            "pipe_jobs": _json(
                _core.encode_obj(_pipe_jobs.encode(state.pipeline_jobs))
            ),
        }
    )
    return freeze(
        {
            "type": _prim_val(_prim("EtlState")),
            "obj": _json(encoded_obj),
        }
    )
