from ._core import (
    JobStream,
    MrStream,
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
    UnfoldedFactory,
)

_prim = JsonPrimitiveFactory.from_raw
_json = JsonValue.from_json
_prim_val = JsonValue.from_primitive


@dataclass(frozen=True)
class StreamEncoder:
    @staticmethod
    def encode_mr_stream(obj: MrStream) -> JsonObj:
        encoded_obj = UnfoldedFactory.from_dict(
            {
                "project": obj.project.raw,
                "scope": obj.scope.value,
                "mr_state": obj.mr_state.value,
            }
        )
        return freeze(
            {
                "type": _prim_val(_prim("MrStream")),
                "obj": _json(encoded_obj),
            }
        )

    @staticmethod
    def encode_job_stream(obj: JobStream) -> JsonObj:
        encoded_obj = freeze(
            {
                "project": _prim_val(_prim(obj.project.raw)),
                "scopes": JsonValue.from_list(
                    tuple(
                        _prim_val(_prim(scope.value)) for scope in obj.scopes
                    )
                ),
            }
        )
        return freeze(
            {
                "type": _prim_val(_prim("JobStream")),
                "obj": _json(encoded_obj),
            }
        )
