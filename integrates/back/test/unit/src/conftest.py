import asyncio
from collections.abc import (
    Callable,
    Generator,
)
import json
import logging
import pytest
from settings import (
    JWT_COOKIE_NAME,
    LOGGING,
)
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

logging.config.dictConfig(LOGGING)


@pytest.fixture(autouse=True)
def disable_logging() -> None:
    """Disable logging in all tests."""
    logging.disable(logging.INFO)


@pytest.yield_fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def resolve_mock_data() -> Any:
    def _resolve_mock_data(
        mock_data: dict[str, dict[str, Any]],
        mock_path: str,
        mock_args: list[Any],
        module_at_test: str,
    ) -> Callable[[dict[str, dict[str, Any]], str, list[Any], str], Any]:
        args_as_str = json.dumps(mock_args, default=str)
        mock_path = module_at_test + mock_path
        return mock_data[mock_path][args_as_str]

    return _resolve_mock_data


@pytest.fixture(name="get_mocked_data")
def fixture_get_mocked_data() -> Callable:
    def _get_mocked_data(
        mocked_data: dict[str, dict[str, Any]],
        mocked_functionality_path: str,
        mock_key: str,
        module_at_test: str,
    ) -> Any:
        return mocked_data[module_at_test + mocked_functionality_path][
            mock_key
        ]

    return _get_mocked_data


@pytest.fixture
def set_mock(
    get_mocked_data: Callable,
) -> Callable:
    def _set_mock(
        # pylint: disable=too-many-arguments
        mock: MagicMock | AsyncMock,
        mocked_functionality_path: str,
        mock_key: str,
        module_at_test: str,
        mocked_data: dict[str, dict[str, Any]],
        side_effect: bool = False,
    ) -> None:
        data = get_mocked_data(
            mocked_data=mocked_data,
            mocked_functionality_path=mocked_functionality_path,
            mock_key=mock_key,
            module_at_test=module_at_test,
        )
        config = {"side_effect" if side_effect else "return_value": data}
        mock.configure_mock(**config)

    return _set_mock


@pytest.fixture
def request_fixture() -> Callable[[str], MagicMock]:
    def _request(subject: str = "unittest") -> MagicMock:
        token: str = "token"
        session: dict[str, str] = dict(
            username=subject, session_key="f2Mu6UsPXT8"
        )
        cookies: dict[str, str] = {JWT_COOKIE_NAME: token}
        headers: dict[str, str] = {}
        request = MagicMock()
        request.configure_mock(
            **{
                "cookies": cookies,
                "session": session,
                "headers": headers,
                "store": {},
                "query_params": {},
            }
        )
        return request

    return _request
