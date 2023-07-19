from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Result,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
from fa_purity.json.factory import (
    from_any,
    json_list,
)
from fa_purity.json.transform import (
    to_raw,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
    UnionFactory,
)
import requests
from requests import (
    Response,
)
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    JSONDecodeError,
)
from typing import (
    NoReturn,
    TypeVar,
)

HandledErrors = Coproduct[
    HTTPError, Coproduct[JSONDecodeError, ConnectionError]
]
_T = TypeVar("_T")


def _unhandled_get(
    endpoint: str, headers: JsonObj, params: JsonObj
) -> Cmd[Response | NoReturn]:
    def _action() -> Response:
        return requests.get(
            endpoint,
            headers=to_raw(headers),  # type: ignore[misc]
            params=to_raw(params),  # type: ignore[misc]
        )

    return Cmd.from_cmd(_action)


def _handle_status(response: Response) -> Result[Response, HTTPError]:
    try:
        response.raise_for_status()
        return Result.success(response)
    except HTTPError as err:  # type: ignore[misc]
        return Result.failure(err)


def _json_decode(
    response: Response,
) -> Result[JsonObj | FrozenList[JsonObj], JSONDecodeError]:
    try:
        _union: UnionFactory[JsonObj, FrozenList[JsonObj]] = UnionFactory()
        raw = response.json()  # type: ignore[misc]
        result = json_list(raw).map(_union.inr).lash(lambda _: from_any(raw).map(_union.inl))  # type: ignore[misc]
        return Result.success(result.unwrap())
    except JSONDecodeError as err:  # type: ignore[misc]
        return Result.failure(err)


def _handle_connection_error(
    action: Cmd[_T],
) -> Cmd[Result[_T, ConnectionError]]:
    def _action(unwrapper: CmdUnwrapper) -> Result[_T, ConnectionError]:
        try:
            return Result.success(unwrapper.act(action))
        except ConnectionError as err:  # type: ignore[misc]
            return Result.failure(err)

    return Cmd.new_cmd(_action)


def get(
    endpoint: str, headers: JsonObj, params: JsonObj
) -> Cmd[Result[JsonObj | FrozenList[JsonObj], HandledErrors]]:
    factory: CoproductFactory[
        HTTPError, Coproduct[JSONDecodeError, ConnectionError]
    ] = CoproductFactory()
    factory2: CoproductFactory[
        JSONDecodeError, ConnectionError
    ] = CoproductFactory()
    return _handle_connection_error(
        _unhandled_get(endpoint, headers, params)
    ).map(
        lambda r: r.alt(lambda e: factory.inr(factory2.inr(e)))
        .bind(lambda res: _handle_status(res).alt(factory.inl))
        .bind(
            lambda res: _json_decode(res).alt(
                lambda e: factory.inr(factory2.inl(e))
            )
        )
    )


__all__ = [
    "ConnectionError",
    "HTTPError",
    "JSONDecodeError",
]
