from purity.v2.json.errors import (
    invalid_type,
)
from purity.v2.json.errors.invalid_type import (
    InvalidType,
)
from purity.v2.json.primitive.core import (
    NotNonePrimTvar,
    PrimitiveTVar,
)
from purity.v2.result import (
    Result,
)
from typing import (
    Any,
    Optional,
    Type,
)


def to_primitive(
    raw: Any, prim_type: Type[PrimitiveTVar]
) -> Result[PrimitiveTVar, InvalidType]:
    if isinstance(raw, prim_type):
        return Result.success(raw)
    return Result.failure(
        invalid_type.new("to_primitive", str(prim_type), raw)
    )


def to_opt_primitive(
    raw: Any, prim_type: Type[NotNonePrimTvar]
) -> Result[Optional[NotNonePrimTvar], InvalidType]:
    if raw is None or isinstance(raw, prim_type):
        return Result.success(raw)
    return Result.failure(
        invalid_type.new("to_opt_primitive", f"{prim_type} | None", raw)
    )
