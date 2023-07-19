from fa_purity import (
    Result,
    ResultE,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.json_2.value import (
    JsonObj,
    JsonValue,
    Unfolder,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def require_key(raw: JsonObj, key: str) -> ResultE[JsonValue]:
    try:
        return Result.success(raw[key])
    except KeyError as err:
        return Result.failure(Exception(err))


def require_restricted_str(
    raw: JsonObj, key: str, restrictions: FrozenList[str]
) -> ResultE[str]:
    def _validate(item: str) -> ResultE[str]:
        if item in restrictions:
            return Result.success(item)
        err = Exception(
            f"Expected restricted str i.e. {item} not in {restrictions}"
        )
        return Result.failure(err)

    return (
        require_key(raw, key)
        .bind(
            lambda v: Unfolder.to_primitive(v).bind(
                JsonPrimitiveUnfolder.to_str
            )
        )
        .bind(_validate)
    )


def decode_required_nested_keys(
    raw: JsonObj,
    keys: FrozenList[str],
    decoder: Callable[[JsonValue], ResultE[_T]],
) -> ResultE[_T]:
    previous = JsonValue.from_json(raw)
    try:
        for k in keys:
            result = Unfolder.to_json(previous)
            if result.map(lambda _: True).value_or(False):
                previous = result.unwrap()[k]
            else:
                return (
                    result.map(JsonValue.from_json)
                    .bind(decoder)
                    .alt(
                        lambda e: Exception(
                            f"nested keys {keys} decode fail at {k} i.e. {e}"
                        )
                    )
                )
        return decoder(previous)
    except KeyError as err:
        return Result.failure(Exception(err))


def require_index(raw: FrozenList[_T], index: int) -> ResultE[_T]:
    try:
        return Result.success(raw[index])
    except IndexError as err:
        return Result.failure(Exception(err))


def decode_required_key(
    raw: JsonObj, key: str, decoder: Callable[[JsonValue], ResultE[_T]]
) -> ResultE[_T]:
    return (
        require_key(raw, key)
        .bind(decoder)
        .alt(lambda e: Exception(f"Error at key {key} i.e. {e}"))
    )
