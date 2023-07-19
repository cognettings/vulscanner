from . import (
    _requests,
    _retry,
)
from ._requests import (
    ConnectionError,
    HandledErrors,
    HTTPError,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Result,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.result import (
    ResultFactory,
)
from fa_purity.union import (
    Coproduct,
    CoproductFactory,
    UnionFactory,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


@dataclass(frozen=True)
class Credentials:
    account: str
    api_key: str

    def __str__(self) -> str:
        return "masked api_key"


class UnexpectedServerResponse(Exception):
    pass


@dataclass(frozen=True)
class RawClient:
    _auth: Credentials
    _max_retries: int = 10
    _api_url: str = "https://api.checklyhq.com"

    def _full_endpoint(self, endpoint: str) -> str:
        return self._api_url + endpoint

    @property
    def _headers(self) -> JsonObj:
        headers = {
            "X-Checkly-Account": JsonValue(self._auth.account),
            "Authorization": JsonValue(f"Bearer {self._auth.api_key}"),
        }
        return freeze(headers)

    def _handler(
        self,
        item: Result[JsonObj | FrozenList[JsonObj], HandledErrors],
    ) -> (
        Result[
            JsonObj | FrozenList[JsonObj],
            Coproduct[HTTPError, ConnectionError],
        ]
        | NoReturn
    ):
        factory: CoproductFactory[
            HTTPError, ConnectionError
        ] = CoproductFactory()

        def _http_err(error: HTTPError) -> HTTPError | NoReturn:
            err_code: int = error.response.status_code  # type: ignore[misc]
            if err_code in (429,) or err_code in range(500, 600):
                return error
            raise error

        return item.alt(
            lambda e: e.map(
                lambda h: factory.inl(_http_err(h)),
                lambda u: u.map(
                    raise_exception,
                    lambda c: factory.inr(c),
                ),
            )
        )

    def _server_error_handler(
        self,
        retry: int,
        result: Result[_T, Coproduct[HTTPError, ConnectionError]],
    ) -> Result[_T | None, Coproduct[HTTPError, ConnectionError]]:
        _union: UnionFactory[_T, None] = UnionFactory()
        factory: CoproductFactory[
            HTTPError, ConnectionError
        ] = CoproductFactory()
        factory2: ResultFactory[
            _T | None, Coproduct[HTTPError, ConnectionError]
        ] = ResultFactory()

        def _handler(
            error: HTTPError,
        ) -> Result[_T | None, Coproduct[HTTPError, ConnectionError]]:
            err_code: int = error.response.status_code  # type: ignore[misc]
            threshold = round(self._max_retries * 0.4)
            if retry >= threshold and err_code in range(500, 600):
                return factory2.success(None)
            return Result.failure(factory.inl(error))

        return result.map(_union.inl).lash(
            lambda u: u.map(
                _handler, lambda c: factory2.failure(factory.inr(c))
            )
        )

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj] | None]:
        _union: UnionFactory[
            JsonObj | FrozenList[JsonObj], None
        ] = UnionFactory()
        target = self._full_endpoint(endpoint)
        log = Cmd.from_cmd(
            lambda: LOG.info("API call (get): %s\nparams = %s", target, params)
        )
        handled = (
            _requests.get(target, self._headers, params)
            .map(self._handler)
            .map(lambda r: r.map(_union.inl))
        )

        def _retry_cmd(
            retry: int,
            result: Result[
                JsonObj | FrozenList[JsonObj] | None,
                Coproduct[HTTPError, ConnectionError],
            ],
        ) -> Cmd[
            Result[
                JsonObj | FrozenList[JsonObj] | None,
                Coproduct[HTTPError, ConnectionError],
            ]
        ]:
            retry_msg = Cmd.from_cmd(
                lambda: LOG.info("retry #%2s waiting...", retry)
            )
            delay = _retry.sleep_cmd(retry ^ 2)
            _delay = _retry.cmd_if_fail(result, retry_msg + delay)
            factory: ResultFactory[
                JsonObj | FrozenList[JsonObj] | None,
                Coproduct[HTTPError, ConnectionError],
            ] = ResultFactory()

            if endpoint.startswith("/v1/check-results"):
                return (
                    self._server_error_handler(retry, result)
                    .map(lambda x: Cmd.from_cmd(lambda: factory.success(x)))
                    .value_or(_delay)
                )
            return _delay

        return log + _retry.retry_cmd(
            handled, lambda i, r: _retry_cmd(i, r), self._max_retries
        ).map(lambda r: r.alt(raise_exception).unwrap())

    def get_list(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        empty: FrozenList[JsonObj] = tuple()
        return (
            self.get(endpoint, params)
            .map(lambda x: empty if x is None else x)
            .map(
                lambda x: Maybe.from_optional(
                    x if isinstance(x, tuple) else None
                )
                .to_result()
                .alt(
                    lambda _: Exception(f"Expected a FrozenList got {type(x)}")
                )
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )

    def get_item(self, endpoint: str, params: JsonObj) -> Cmd[JsonObj]:
        empty: JsonObj = FrozenDict({})
        return (
            self.get(endpoint, params)
            .map(lambda x: empty if x is None else x)
            .map(
                lambda x: Maybe.from_optional(
                    x if not isinstance(x, tuple) else None
                )
                .to_result()
                .alt(lambda _: Exception(f"Expected a JsonObj got {type(x)}"))
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )
