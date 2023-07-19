from __future__ import (
    annotations,
)

from ._page import (
    InvalidPage,
    Page,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Result,
)
from fa_purity.json import (
    JsonObj as LegacyJsonObj,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitiveFactory,
    JsonValue,
    LegacyAdapter,
    Unfolder,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from pure_requests import (
    basic,
    response,
    retry as _retry,
)
from requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    HTTPError,
    JSONDecodeError,
    RequestException,
)
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Credentials:
    api_key: str

    def __repr__(self) -> str:
        return "Credentials([masked])"

    def __str__(self) -> str:
        return "Credentials([masked])"


_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


class UnexpectedType(Exception):
    def __init__(self, obj: _T, expected: str) -> None:
        super().__init__(
            f"Expected `{expected}` but got `{type(obj).__name__}`"
        )


def _retry_cmd(retry: int, item: Result[_S, _F]) -> Cmd[Result[_S, _F]]:
    log = Cmd.from_cmd(lambda: LOG.info("retry #%2s waiting...", retry))
    return _retry.cmd_if_fail(item, log + _retry.sleep_cmd(retry ^ 2))


def _http_error_handler(error: HTTPError) -> HTTPError | NoReturn:
    err_code: int = error.response.status_code  # type: ignore[misc]
    handled = (
        409,
        429,
    )
    if err_code in range(500, 600) or err_code in handled:
        return error
    raise error


def _handled_errors(error: RequestException) -> RequestException | NoReturn:
    """wrap handled errors, raise unhandled errors"""
    if isinstance(error, HTTPError):  # type: ignore[misc]
        return _http_error_handler(error)
    if isinstance(error, ChunkedEncodingError):  # type: ignore[misc]
        return error
    if isinstance(error, ConnectionError):  # type: ignore[misc]
        return error
    raise error


def _cast_http(err: HTTPError) -> RequestException:
    return err


def _cast_json(err: JSONDecodeError) -> RequestException:
    return err


@dataclass(frozen=True)
class HttpJsonClient:
    _creds: Credentials
    _max_retries: int

    def _full_endpoint(self, endpoint: str) -> str:
        return "https://gitlab.com/api/v4" + endpoint

    @staticmethod
    def new(creds: Credentials) -> HttpJsonClient:
        return HttpJsonClient(
            creds,
            150,
        )

    @property
    def _headers(self) -> JsonObj:
        return FrozenDict(
            {
                "Private-Token": JsonValue.from_primitive(
                    JsonPrimitiveFactory.from_raw(self._creds.api_key)
                )
            }
        )

    def get(
        self, relative_endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        _full = self._full_endpoint(relative_endpoint)
        log = Cmd.from_cmd(
            lambda: LOG.info(
                "API call (get): %s\nparams = %s",
                _full,
                Unfolder.dumps(params),
            )
        )

        handled = log + basic.get(_full, self._headers, params).map(
            lambda r: r.bind(
                lambda r1: response.handle_status(r1).alt(_cast_http)
            )
            .bind(lambda r2: response.json_decode(r2).alt(_cast_json))
            .alt(_handled_errors)
        )
        return _retry.retry_cmd(
            handled,
            _retry_cmd,
            self._max_retries,
        ).map(lambda r: r.alt(raise_exception).unwrap())

    def get_list(
        self, relative_endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        def assert_flist(
            item: JsonObj | FrozenList[JsonObj],
        ) -> FrozenList[JsonObj]:
            if isinstance(item, tuple):
                return item
            raise TypeError("Expected a FrozenList")

        return self.get(relative_endpoint, params).map(assert_flist)

    def get_item(
        self, relative_endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj]:
        def assert_json(item: JsonObj | FrozenList[JsonObj]) -> JsonObj:
            if not isinstance(item, tuple):
                return item
            raise TypeError("Expected a FrozenList")

        return self.get(relative_endpoint, params).map(assert_json)

    def legacy_get_list(
        self, relative_endpoint: str, params: LegacyJsonObj
    ) -> Cmd[FrozenList[LegacyJsonObj]]:
        return self.get_list(
            relative_endpoint, LegacyAdapter.json(params)
        ).map(
            lambda items: tuple(LegacyAdapter.to_legacy_json(i) for i in items)
        )

    def legacy_get_item(
        self, relative_endpoint: str, params: LegacyJsonObj
    ) -> Cmd[LegacyJsonObj]:
        return self.get_item(
            relative_endpoint, LegacyAdapter.json(params)
        ).map(LegacyAdapter.to_legacy_json)

    def post(self, relative_endpoint: str) -> Cmd[None]:
        _full = self._full_endpoint(relative_endpoint)
        log = Cmd.from_cmd(lambda: LOG.info("API call (post): %s", _full))
        handled = log + basic.post(
            self._full_endpoint(relative_endpoint),
            self._headers,
            FrozenDict({}),
        ).map(
            lambda c: c.bind(
                lambda r: response.handle_status(r).alt(_cast_http)
            )
            .map(lambda _: None)
            .alt(_handled_errors)
        )
        result: Cmd[Result[None, _retry.MaxRetriesReached]] = _retry.retry_cmd(
            handled,
            _retry_cmd,
            self._max_retries,
        )
        return result.map(lambda r: r.alt(raise_exception).unwrap())


__all__ = [
    "Page",
    "InvalidPage",
]
