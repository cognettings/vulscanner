from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from oauth.github import (
    get_access_token,
)
import pytest
from unittest.mock import (
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


async def test_get_github_refresh_token(mock_session: Callable) -> None:
    with patch(
        MODULE_AT_TEST + "aiohttp.ClientSession",
        mock_session,
    ):
        response = await get_access_token(code="test_code")
        assert response == "testing"


async def test_get_github_refresh_catches__json_decode_error(
    mock_session: Callable,
) -> None:
    with patch(
        MODULE_AT_TEST + "aiohttp.ClientSession",
        mock_session,
    ):
        response = await get_access_token(
            code="error",
        )
        assert response is None
