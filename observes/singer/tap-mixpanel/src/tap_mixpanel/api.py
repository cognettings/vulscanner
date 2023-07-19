from contextlib import (
    contextmanager,
)
from functools import (
    partial,
)
from ratelimiter import (
    RateLimiter,
)
import requests  # type: ignore
from requests.exceptions import (  # type: ignore
    HTTPError,
)
import tempfile
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    IO,
    Iterator,
    NamedTuple,
    Tuple,
    TypeVar,
)

_T = TypeVar("_T")
JSON = Dict[str, Any]
API_BASE_URL = "https://data.mixpanel.com/api/2.0"
rate_limiter = RateLimiter(max_calls=40, period=3600)


class Credentials(NamedTuple):
    api_secret: str
    token: str

    @classmethod
    def from_json(cls, creds: JSON) -> "Credentials":
        return Credentials(
            api_secret=creds["API_secret"], token=creds["token"]
        )


def _export(auth: Tuple[str, str], params: JSON) -> Iterator[Any]:
    with rate_limiter:
        result = requests.get(
            f"{API_BASE_URL}/export/",
            auth=auth,
            params=params,
            stream=True,
            timeout=60,
        )
        result.raise_for_status()
        return result.iter_lines(decode_unicode=True)


def handler(cmd: Callable[[], _T]) -> _T:
    max_retries = 10
    retries = 0
    while retries <= max_retries:
        try:
            return cmd()
        except HTTPError as err:
            status_code = err.response.status_code
            if status_code in range(500, 600) or status_code in (
                400,
                429,
            ):
                retries = retries + 1
            else:
                raise err
    raise Exception("Max retries reached")


def _load_data(
    creds: Credentials, event: str, date_range: Tuple[str, str]
) -> Iterator[IO[str]]:
    params = {
        "from_date": date_range[0],
        "to_date": date_range[1],
        "event": f'["{event}"]',
    }
    auth = (creds.api_secret, creds.token)
    result = handler(lambda: _export(auth, params))
    with tempfile.NamedTemporaryFile("w+") as tmp:
        for item in result:
            tmp.write(item)
            tmp.write("\n")
        yield tmp


class ApiClient(NamedTuple):
    load_data: Callable[[str, Tuple[str, str]], Iterator[IO[str]]]
    data_handler: Callable[[str, Tuple[str, str]], ContextManager[IO[str]]]

    @classmethod
    def from_creds(cls, creds: Credentials) -> "ApiClient":
        @contextmanager
        def data_handler(
            event: str, date_range: Tuple[str, str]
        ) -> Iterator[IO[str]]:
            return _load_data(creds, event, date_range)

        return ApiClient(
            load_data=partial(_load_data, creds), data_handler=data_handler
        )
