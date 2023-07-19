from aiohttp import (
    FormData,
)
from collections.abc import (
    Callable,
)
import json
import pytest
from typing import (
    Any,
)


@pytest.fixture(name="mock_post_request")
def fixture_mock_post_request() -> Callable:
    class MockPostResponse:
        def __init__(
            self, url: str, data: str | FormData, headers: str
        ) -> None:
            self.ok = False  # pylint: disable=invalid-name
            self.url = url
            self.data = data
            self._info: dict | None = None
            self.headers = headers

        async def json(self) -> dict:
            self.ok = True
            if isinstance(self.data, FormData):
                path = self.data().__dict__["_value"].decode("utf-8")
                if "error" in path:
                    json.loads("this_cause_a_JSONDecodeError")
                return dict(url=self.url, path=path)

            self._info = json.loads(self.data)
            if self._info and self._info["code"] == "error":
                json.loads("this_cause_a_JSONDecodeError")
            return dict(
                code=self._info["code"] if self._info else None,
                url=self.url,
                headers=self.headers,
                access_token="testing",
            )

        def __enter__(self) -> None:
            raise TypeError("Use async with instead")

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: Any,
        ) -> None:
            # __exit__ should exist in pair with __enter__ but never executed
            pass

        async def __aenter__(self) -> "MockPostResponse":
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: Any,
        ) -> None:
            # here release all locked resources since this is
            #  a mock I will keep as simple as possible
            pass

    return MockPostResponse


@pytest.fixture
def mock_session(mock_post_request: Callable) -> Callable:
    "This fixture mocks the interaction with oauth providers"

    class MockClientSession:
        def __init__(self, headers: dict | None = None) -> None:
            self.headers = json.dumps(headers) if headers else None

        def post(  # pylint: disable=unused-argument
            self,
            url: str,
            *,
            data: Any = None,
            **kwargs: Any,
        ) -> Callable:
            return mock_post_request(url, data, headers=self.headers)

        def __enter__(self) -> None:
            raise TypeError("Use async with instead")

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: Any,
        ) -> None:
            # __exit__ should exist in pair with __enter__ but never executed
            pass

        async def __aenter__(self) -> "MockClientSession":
            return self

        async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: Any,
        ) -> None:
            # here release all locked resources since this is
            #  a mock I will keep as simple as possible
            pass

    return MockClientSession
