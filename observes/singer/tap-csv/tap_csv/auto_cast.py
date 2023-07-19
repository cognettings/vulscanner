from fa_purity import (
    PureIter,
    Result,
    ResultE,
)
from fa_purity.json_2 import (
    JsonPrimitive,
    JsonValue,
)
from fa_purity.pure_iter.factory import (
    from_list,
)
from typing import (
    Callable,
)


def _int_cast(raw: str) -> ResultE[JsonValue]:
    try:
        value = int(raw)
        if int(raw) > pow(10, 12):
            return Result.success(
                JsonValue.from_primitive(JsonPrimitive.from_str(raw))
            )
        return Result.success(
            JsonValue.from_primitive(JsonPrimitive.from_int(value))
        )
    except ValueError as err:
        return Result.failure(Exception(err))


def _float_cast(raw: str) -> ResultE[JsonValue]:
    try:
        if (
            (raw.lower() != "nan" or raw == "NaN")
            and float(raw) != float("inf")
            and float(raw) < pow(10, 12)
        ):
            return Result.success(
                JsonValue.from_primitive(JsonPrimitive.from_float(float(raw)))
            )
        return Result.failure(Exception("invalid float"))
    except ValueError as err:
        return Result.failure(Exception(err))


def _bool_cast(raw: str) -> ResultE[JsonValue]:
    if raw.lower() == "false" or raw.lower() == "true":
        return Result.success(
            JsonValue.from_primitive(
                JsonPrimitive.from_bool(raw.lower() == "true")
            )
        )
    return Result.failure(Exception("not a bool"))


def auto_cast(data: str) -> JsonValue:
    test_casts: PureIter[Callable[[str], ResultE[JsonValue]]] = from_list(
        [
            _int_cast,
            _float_cast,
            _bool_cast,
            lambda x: Result.success(
                JsonValue.from_primitive(JsonPrimitive.from_str(x))
            ),
        ]
    )
    item = test_casts.map(lambda f: f(data)).find_first(
        lambda r: r.map(lambda _: True).value_or(False)
    )
    return item.unwrap().unwrap()
