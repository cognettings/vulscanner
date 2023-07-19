from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from oauth.gitlab import (
    get_refresh_token,
)
import pytest
from unittest.mock import (
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


async def test_get_refresh_token(mock_session: Callable) -> None:
    with patch(
        MODULE_AT_TEST + "aiohttp.ClientSession",
        mock_session,
    ):
        response = await get_refresh_token(
            code="test_code",
            redirect_uri="https://testing.com",
            code_verifier="testing",
        )
        assert response
        assert response["code"] == "test_code"
        assert response["headers"] == '{"content-type": "application/json"}'
        assert "gitlab" in response["url"]


async def test_get_github_refresh_catches__json_decode_error(
    mock_session: Callable,
) -> None:
    with patch(
        MODULE_AT_TEST + "aiohttp.ClientSession",
        mock_session,
    ):
        response = await get_refresh_token(
            code="error",
            redirect_uri="https://testing.com",
            code_verifier="testing",
        )
        assert response is None
