from fa_purity import (
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.json_2 import (
    JsonObj,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
)
from pure_requests.response import (
    handle_status,
    json_decode,
)
from requests import (
    HTTPError,
    JSONDecodeError,
    Response,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def decode_json(
    response: Response,
) -> Result[
    JsonObj, Coproduct[HTTPError, Coproduct[JSONDecodeError, TypeError]]
]:
    def _decode(
        raw: JsonObj | FrozenList[JsonObj],
    ) -> Result[JsonObj, TypeError]:
        if isinstance(raw, tuple):
            err = TypeError("Unexpected list")
            return Result.failure(err)
        return Result.success(raw)

    factory: CoproductFactory[
        HTTPError, Coproduct[JSONDecodeError, TypeError]
    ] = CoproductFactory()
    factory2: CoproductFactory[JSONDecodeError, TypeError] = CoproductFactory()
    return (
        handle_status(response)
        .alt(lambda x: factory.inl(x))
        .bind(
            lambda r: json_decode(r)
            .alt(lambda x: factory.inr(factory2.inl(x)))
            .bind(
                lambda x: _decode(x).alt(
                    lambda x: factory.inr(factory2.inr(x))
                )
            )
        )
    )


def require_index(items: FrozenList[_T], index: int) -> ResultE[_T]:
    try:
        return Result.success(items[index])
    except IndexError as err:
        return Result.failure(Exception(err))
