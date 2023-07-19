from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from oauth.bitbucket import (
    get_bitbucket_refresh_token,
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
        MODULE_AT_TEST + "ClientSession",
        mock_session,
    ):
        response = await get_bitbucket_refresh_token(
            code="test_code",
            redirect_uri="https://testing.com",
        )
        assert response
        assert "bitbucket" in response["url"]
        assert (
            "code=test_code&grant_type=authorization_code" in response["path"]
        )


async def test_get_refresh_token_catches_json_error(
    mock_session: Callable,
) -> None:
    with patch(
        MODULE_AT_TEST + "ClientSession",
        mock_session,
    ):
        response = await get_bitbucket_refresh_token(
            code="error",
            redirect_uri="https://testing.com",
        )
        assert response is None
