from app.utils import (
    get_jwt_userinfo,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from httpx import (
    ConnectTimeout,
    ReadTimeout,
)
import pytest
from unittest.mock import (
    MagicMock,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(["exception"], [[ConnectTimeout], [ReadTimeout]])
async def test_get_jwt_userinfo_retry_on_exception(
    request_fixture: Callable[[str], MagicMock],
    exception: type[Exception],
) -> None:
    client = MagicMock()
    request = request_fixture("testing")
    client.parse_id_token.side_effect = exception("testing")
    with pytest.raises(exception, match="testing"):
        await get_jwt_userinfo(client, request, "mocked_token")
    client.parse_id_token.assert_called_with(
        request, "mocked_token", claims_options=None
    )
    assert client.parse_id_token.call_count == 5
