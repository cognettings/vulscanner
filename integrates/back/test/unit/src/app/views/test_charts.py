from app.views.charts import (
    graphics_for_entity,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from custom_utils import (
    templates,
)
from httpx import (
    AsyncClient,
)
import pytest
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
@patch(
    MODULE_AT_TEST + "analytics_domain.handle_graphics_for_entity_request",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "sessions_domain.create_session_token",
    new_callable=AsyncMock,
)
async def test_graphics_for_entity(
    # pylint: disable=too-many-arguments
    mock_create_session_token: AsyncMock,
    mock_handle_graphics_for_entity_request: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: Callable,
) -> None:
    mocks_info: list[tuple[str, AsyncMock]] = [
        ("sessions_domain.get_jwt_content", mock_get_jwt_content),
        ("sessions_domain.create_session_token", mock_create_session_token),
    ]
    for functionality, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key="test_graphics_for_entity",
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=False,
        )

    request = request_fixture("testing")
    mock_handle_graphics_for_entity_request.return_value = (
        templates.graphics_for_entity_view(request, "group")
    )

    response = await graphics_for_entity(entity="group", request=request)
    assert (
        "0J1SkZPT1RiZ0xodUxtdk0iLCJlbmNyeXB0ZWRfa2"
        in response.headers["set-cookie"]
    )
    assert response.template.name == "graphics-for-entity.html"  # type: ignore
    assert response.status_code == 200
    mock_get_jwt_content.assert_awaited_once()
    mock_create_session_token.assert_awaited_once()
    mock_handle_graphics_for_entity_request.assert_awaited_with(
        entity="group", request=request
    )


async def test_unauthorize_access_to_graphics(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/graphics-for-organization?reportMode=true&bgChange=true&organization=ORG%2338b8f25-7945-4173"  # noqa: E501 pylint: disable=line-too-long
    )
    assert response.status_code == 200
