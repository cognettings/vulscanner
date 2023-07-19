from app.app import (
    APP,
    app,
    confirm_access,
    logout,
    not_found,
    reject_access,
    server_error,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from custom_exceptions import (
    InvalidAuthorization,
    SecureAccessException,
)
from httpx import (
    AsyncClient,
)
from httpx._models import (
    Response,
)
import pytest
from typing import (
    Any,
    Callable,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    Mock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


def test_should_intialize() -> None:
    assert APP is not None


@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
@patch(
    MODULE_AT_TEST + "sessions_domain.check_session_web_validity",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "logout", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "FI_ENVIRONMENT", "testing")
async def test_app(
    mock_logout: AsyncMock,
    mock_check_session_web_validity: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
) -> None:
    mock_get_jwt_content.return_value = {"user_email": "test@fluidattacks.com"}
    mock_check_session_web_validity.side_effect = SecureAccessException
    mock_logout.return_value = "/logout"
    with patch(MODULE_AT_TEST + "FI_ENVIRONMENT", "production"):
        response = await app(request_fixture("testing"))
        # check_session_web_validity raises a SecureAccessException
        mock_check_session_web_validity.assert_called_once()
        # logout is the endpoint when a SecureAccessException is raised
        assert response == "/logout"  # type: ignore
    response = await app(request_fixture("testing"))
    assert response.template.name == "app.html"  # type: ignore
    assert mock_check_session_web_validity.call_count == 1


@patch(MODULE_AT_TEST + "sessions_domain", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "analytics.mixpanel_track", new_callable=AsyncMock)
async def test_logout(
    mock_mixpanel_track: AsyncMock,
    mock_sessions_domain: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
) -> None:
    mock_sessions_domain.get_jwt_content.return_value = {
        "user_email": "test@fluidattacks.com"
    }
    with patch(
        MODULE_AT_TEST + "sessions_domain.get_jwt_content",
        new_callable=AsyncMock,
    ) as mock_jwt_content:
        mock_jwt_content.side_effect = InvalidAuthorization
        response = await logout(request_fixture("testing"))
        assert response.template.name == "unauthorized.html"  # type: ignore
    mock_mixpanel_track.return_value = None
    mock_sessions_domain.remove_session_key.return_value = None
    mock_sessions_domain.remove_session_token.return_value = None
    response = await logout(request_fixture("testing"))
    assert response.status_code == 307


@pytest.mark.parametrize(
    ["path_params"],
    [
        [
            {
                "url_token": "/invalid",
            }
        ],
        [
            {
                "url_token": None,
            }
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "group_access_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "groups_domain.complete_register_for_group_invitation",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "in_thread", new_callable=AsyncMock)
async def test_confirm_access_returns_invalid_invitation_template(
    mock_in_thread: AsyncMock,
    mock_complete_register_for_group_invitation: AsyncMock,
    mock_get_access_by_url_token: AsyncMock,
    path_params: dict,
    request_fixture: Callable[[str], MagicMock],
) -> None:
    mock_in_thread.side_effect = None
    mock_complete_register_for_group_invitation.side_effect = None
    mock_get_access_by_url_token.side_effect = InvalidAuthorization()
    request = request_fixture("testing")
    request.configure_mock(path_params=path_params)
    response = await confirm_access(request)
    assert response.template.name == "invalid_invitation.html"  # type: ignore
    assert response.context["error"] == "Invalid or Expired"  # type: ignore


@pytest.mark.parametrize(
    ["path_params"],
    [
        [
            {
                "url_token": "/valid",
            },
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "group_access_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "groups_domain.complete_register_for_group_invitation",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "in_thread", new_callable=AsyncMock)
async def test_confirm_access(
    # pylint: disable=too-many-arguments
    mock_in_thread: AsyncMock,
    mock_complete_register_for_group_invitation: AsyncMock,
    mock_get_access_by_url_token: AsyncMock,
    path_params: dict,
    request_fixture: Callable[[str], MagicMock],
    mock_data_for_module: Any,
) -> None:
    mock_in_thread.side_effect = None
    mock_complete_register_for_group_invitation.side_effect = None
    mock_get_access_by_url_token.return_value = mock_data_for_module(
        test_name="test_confirm_access",
        mock_name="mock_get_access_by_url_token",
        module_at_test=MODULE_AT_TEST,
    )
    request = request_fixture("testing")
    request.configure_mock(path_params=path_params)
    response = await confirm_access(request)
    assert response.template.name == "valid_invitation.html"  # type: ignore
    assert response.context["entity_name"] == "group"  # type: ignore


@patch(MODULE_AT_TEST + "get_new_context")
@patch(
    MODULE_AT_TEST + "remove_stakeholder_domain.get_email_from_url_token",
    new_callable=AsyncMock,
)
async def test_confirm_deletion_returns_invalid_delete_confirmation(
    mock_get_email_from_urls_token: AsyncMock,
    mock_get_new_context: Mock,
    client: AsyncClient,
) -> None:
    mock_get_new_context.return_value = None
    response: Response = await client.get("/confirm_deletion/")
    assert response.status_code == 200
    # Since the token was not included in the url
    # get_email_from_url_token was not called
    mock_get_email_from_urls_token.assert_not_called()


@patch(MODULE_AT_TEST + "get_new_context")
@patch(MODULE_AT_TEST + "remove_stakeholder_domain", new_callable=AsyncMock)
async def test_confirm_deletion(
    mock_remove_stakeholder_domain: AsyncMock,
    mock_get_new_context: Mock,
    client: AsyncClient,
) -> None:
    mock_get_new_context.return_value = None
    mock_remove_stakeholder_domain.get_email_from_url_token.return_value = (
        "testing@fluidattacks.com"
    )
    mock_remove_stakeholder_domain.complete_deletion.side_effect = None
    response: Response = await client.get("/confirm_deletion/test_token")
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.status_code == 200
    assert response.url == "http://testserver/confirm_deletion/test_token"
    mock_remove_stakeholder_domain.get_email_from_url_token.assert_called_once()  # noqa: E501 pylint: disable=line-too-long
    mock_remove_stakeholder_domain.complete_deletion.assert_called_once()


@patch(MODULE_AT_TEST + "get_new_context")
@patch(
    MODULE_AT_TEST + "orgs_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
async def test_confirm_access_organization_handles_invalid_token(
    mock_get_access_by_url_token: AsyncMock,
    mock_get_new_context: Mock,
    client: AsyncClient,
) -> None:
    mock_get_new_context.return_value = None
    response: Response = await client.get("/confirm_access_organization/")
    assert response.status_code == 200
    mock_get_access_by_url_token.assert_not_called()


@pytest.mark.parametrize("test_name", ["test_confirm_access_organization"])
@patch(MODULE_AT_TEST + "get_new_context")
@patch(
    MODULE_AT_TEST + "orgs_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST
    + "orgs_domain.complete_register_for_organization_invitation",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "orgs_utils.get_organization",
    new_callable=AsyncMock,
)
async def test_confirm_access_organization(
    # pylint: disable=too-many-arguments
    mock_get_organization: AsyncMock,
    mock_complete_register_for_organization_invitation: AsyncMock,
    mock_get_access_by_url_token: AsyncMock,
    mock_get_new_context: Mock,
    test_name: str,
    client: AsyncClient,
    mock_data_for_module: Any,
) -> None:
    mock_get_new_context.return_value = None
    mock_get_access_by_url_token.return_value = mock_data_for_module(
        test_name=test_name,
        mock_name="mock_get_access_by_url_token",
        module_at_test=MODULE_AT_TEST,
    )
    mock_complete_register_for_organization_invitation.side_effect = None
    mock_get_organization.return_value = mock_data_for_module(
        test_name=test_name,
        mock_name="mock_get_organization",
        module_at_test=MODULE_AT_TEST,
    )
    response: Response = await client.get(
        "/confirm_access_organization/test_token"
    )
    assert response.status_code == 200
    mock_complete_register_for_organization_invitation.assert_called_once()
    mock_get_access_by_url_token.assert_called_once()
    mock_get_organization.assert_called_once()


async def test_reject_access_check_if_url_token_in_path(
    client: AsyncClient,
    request_fixture: Callable[[str], MagicMock],
) -> None:
    response: Response = await client.get("/reject_access")
    assert response.status_code == 200
    # Now let's testing endpoint
    request = request_fixture("testing")
    request.configure_mock(path_params={})
    response_from_end_point = await reject_access(request)
    template_name = response_from_end_point.template.name  # type: ignore
    assert template_name == "invalid_invitation.html"
    error = response_from_end_point.context["error"]  # type: ignore
    assert error == "Invalid or Expired"


@patch(
    MODULE_AT_TEST + "group_access_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "groups_domain.reject_register_for_group_invitation",
    new_callable=AsyncMock,
)
async def test_reject_access(
    mock_group_domain_reject_register_for_group_invitation: AsyncMock,
    mock_group_access_domain_get_access_by_url_token: AsyncMock,
    client: AsyncClient,
    mock_data_for_module: Any,
) -> None:
    mock_group_access_domain_get_access_by_url_token.return_value = (
        mock_data_for_module(
            test_name="test_reject_access",
            mock_name="mock_group_access_domain_get_access_by_url_token",
            module_at_test=MODULE_AT_TEST,
        )
    )
    mock_group_domain_reject_register_for_group_invitation.side_effect = None
    response = await client.get("/reject_access/test_token")
    assert response.status_code == 200
    mock_group_access_domain_get_access_by_url_token.assert_called_once()
    mock_group_domain_reject_register_for_group_invitation.assert_called_once()
    assert response.url == "http://testserver/reject_access/test_token"


@pytest.mark.parametrize(
    "url",
    [
        "/reject_access_organization/not_valid_token",
    ],
)
@patch(
    MODULE_AT_TEST + "orgs_domain.get_access_by_url_token",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "in_thread", new_callable=AsyncMock)
async def test_reject_access_organization(
    mock_in_thread: AsyncMock,
    mock_get_access_by_url_token: AsyncMock,
    client: AsyncClient,
    url: str,
) -> None:
    mock_get_access_by_url_token.side_effect = InvalidAuthorization()
    mock_in_thread.side_effect = None
    response: Response = await client.get(url)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    mock_get_access_by_url_token.assert_called_once()
    mock_in_thread.assert_called_once()


def test_not_found(
    request_fixture: Callable[[str], MagicMock],
) -> None:
    response = not_found(
        request_fixture("testing"), Exception("testing exception")
    )
    assert response.template.name == "HTTP401.html"  # type: ignore


def test_server_error(
    request_fixture: Callable[[str], MagicMock],
) -> None:
    response = server_error(
        request_fixture("testing"), Exception("testing exception")
    )
    assert response.template.name == "HTTP500.html"  # type: ignore
