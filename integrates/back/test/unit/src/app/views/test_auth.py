from app.views.auth import (
    authz_azure,
    authz_bitbucket,
    authz_google,
    do_azure_login,
    do_bitbucket_login,
    log_stakeholder_in,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from sessions.types import (
    UserAccessInfo,
)
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["user_info"],
    [
        [
            UserAccessInfo(
                first_name="First_Name",
                last_name="Last_Name",
                user_email="integratesuser2@fluidattacks.com",
            )
        ]
    ],
)
@patch(
    MODULE_AT_TEST + "stakeholders_domain.update_last_login",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "utils.send_autoenroll_mixpanel_event",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "Dataloaders.stakeholder", new_callable=AsyncMock)
async def test_log_stakeholder_in(
    # pylint: disable=too-many-arguments
    mock_dataloaders_stakeholder: AsyncMock,
    mock_utils_send_autoenroll_mixpanel_event: AsyncMock,
    mock_stakeholders_domain_update_last_login: AsyncMock,
    user_info: UserAccessInfo,
    mocked_data_for_module: dict,
    set_mock: Callable,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, str]] = [
        (
            mock_dataloaders_stakeholder.load,
            "Dataloaders.stakeholder",
            user_info.user_email,
        ),
        (
            mock_utils_send_autoenroll_mixpanel_event,
            "utils.send_autoenroll_mixpanel_event",
            user_info.user_email,
        ),
        (
            mock_stakeholders_domain_update_last_login,
            "stakeholders_domain.update_last_login",
            user_info.user_email,
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for mock_item in mocks_setup_list:
        mock, path, key = mock_item
        set_mock(
            mock=mock,
            mocked_functionality_path=path,
            mock_key=key,
            mocked_data=mocked_data_for_module,
            module_at_test=MODULE_AT_TEST,
            side_effect=False,
        )
    loaders: Dataloaders = get_new_context()

    await log_stakeholder_in(
        loaders=loaders,
        user_info=user_info,
    )
    assert mock_dataloaders_stakeholder.load.called is True
    assert mock_utils_send_autoenroll_mixpanel_event.called is True
    assert mock_stakeholders_domain_update_last_login.called is True


@pytest.mark.parametrize(["test_case"], [["MismatchingStateError"]])
async def test_authz_azure_catches_errors(
    test_case: str,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict[str, dict[str, Any]],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    set_mock(
        mock=client.authorize_access_token,
        mocked_functionality_path="OAUTH.azure.authorize_access_token",
        mock_key=test_case,
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    with patch(MODULE_AT_TEST + "OAUTH", azure=client):
        response = await authz_azure(request_fixture("testing"))
        assert response.template.name == "unauthorized.html"  # type: ignore


@pytest.mark.parametrize(["test_case"], [["OAuthError"]])
async def test_authz_azure_catches_errors_retry_on_exception(
    test_case: str,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict[str, dict[str, Any]],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    set_mock(
        mock=client.authorize_access_token,
        mocked_functionality_path="OAUTH.azure.authorize_access_token",
        mock_key=test_case,
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    request = request_fixture("testing")
    with patch(MODULE_AT_TEST + "OAUTH", azure=client):
        response = await authz_azure(request)
        assert response.template.name == "unauthorized.html"  # type: ignore
    client.authorize_access_token.assert_called_with(request)
    assert client.authorize_access_token.call_count == 5


@patch(MODULE_AT_TEST + "utils.get_jwt_userinfo", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "handle_user", new_callable=AsyncMock)
async def test_authz_azure(
    mock_handle_user: AsyncMock,
    mock_get_jwt_userinfo: AsyncMock,
    mocked_data_for_module: dict[str, dict[str, Any]],
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    mocks_info: list[tuple[str, AsyncMock, bool]] = [
        (
            "OAUTH.azure.authorize_access_token",
            client.authorize_access_token,
            False,
        ),
        ("utils.get_jwt_userinfo", mock_get_jwt_userinfo, False),
        ("utils.get_jwt_userinfo", mock_handle_user, True),
    ]
    for functionality_to_mock, mock, is_side_effect in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality_to_mock,
            mock_key="test_authz_azure",
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=is_side_effect,
        )
    with patch(MODULE_AT_TEST + "OAUTH", azure=client):
        response = await authz_azure(request_fixture("testing"))
        assert response.status_code == 307
    mock_get_jwt_userinfo.assert_awaited_once()
    mock_handle_user.assert_awaited_once()
    client.authorize_access_token.assert_awaited_once()


@pytest.mark.parametrize(
    ["test_case"],
    [
        ["MismatchingStateError"],
        ["OAuthError"],
    ],
)
async def test_authz_bitbucket_catches_errors_after_retry_on_exception(
    test_case: str,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict[str, dict[str, Any]],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    set_mock(
        mock=client.authorize_access_token,
        mocked_functionality_path="OAUTH.azure.authorize_access_token",
        mock_key=test_case,
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    request = request_fixture("testing")
    with patch(MODULE_AT_TEST + "OAUTH", bitbucket=client):
        response = await authz_bitbucket(request)
        assert response.template.name == "unauthorized.html"  # type: ignore
    client.authorize_access_token.assert_called_with(request)
    assert client.authorize_access_token.call_count == 5


@patch(
    MODULE_AT_TEST + "utils.get_bitbucket_oauth_userinfo",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "handle_user", new_callable=AsyncMock)
@pytest.mark.parametrize(
    ["test_case"],
    [
        ["test_authz_bitbucket"],
        ["test_authz_bitbucket_invalid_authorization_error"],
    ],
)
async def test_authz_bitbucket(
    # pylint: disable=too-many-arguments
    mock_handled_user: AsyncMock,
    mock_get_bitbucket_oauth_userinfo: AsyncMock,
    mocked_data_for_module: dict,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    test_case: str,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    mocks_info: list[tuple[str, MagicMock | AsyncMock, bool]] = [
        (
            "utils.get_bitbucket_oauth_userinfo",
            mock_get_bitbucket_oauth_userinfo,
            False,
        ),
        ("handle_user", mock_handled_user, True),
        (
            "OAUTH.bitbucket.authorize_access_token",
            client.authorize_access_token,
            False,
        ),
    ]

    for functionality, mock, is_side_effect in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key=test_case,
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=is_side_effect,
        )
    with patch(MODULE_AT_TEST + "OAUTH", bitbucket=client):
        response = await authz_bitbucket(request_fixture("testing"))
    if test_case == "test_authz_bitbucket":
        assert response.status_code == 307
    else:
        assert response.template.name == "unauthorized.html"  # type: ignore
    mock_handled_user.assert_awaited_once()
    mock_get_bitbucket_oauth_userinfo.assert_awaited_once()


@pytest.mark.parametrize(
    ["test_case"],
    [
        ["OAuthError"],
        ["MismatchingStateError"],
    ],
)
async def test_authz_google_retry_on_exception(
    test_case: str,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict[str, dict[str, Any]],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    set_mock(
        mock=client.authorize_access_token,
        mocked_functionality_path="OAUTH.azure.authorize_access_token",
        mock_key=test_case,
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    request = request_fixture("testing")
    with patch(MODULE_AT_TEST + "OAUTH", google=client):
        response = await authz_google(request)
        assert response.template.name == "unauthorized.html"  # type: ignore
    client.authorize_access_token.assert_called_with(request)
    assert client.authorize_access_token.call_count == 5


@patch(
    MODULE_AT_TEST + "utils.get_jwt_userinfo",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "handle_user", new_callable=AsyncMock)
async def test_authz_google(
    mock_handled_user: AsyncMock,
    mock_get_jtw_userinfo: AsyncMock,
    mocked_data_for_module: dict,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
) -> None:
    client = MagicMock(authorize_access_token=AsyncMock())
    mocks_info: list[tuple[str, MagicMock | AsyncMock, bool]] = [
        (
            "utils.get_jwt_userinfo",
            mock_get_jtw_userinfo,
            False,
        ),
        ("handle_user", mock_handled_user, True),
        (
            "OAUTH.google.authorize_access_token",
            client.authorize_access_token,
            False,
        ),
    ]

    for functionality, mock, is_side_effect in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key="test_authz_google",
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=is_side_effect,
        )
    with patch(MODULE_AT_TEST + "OAUTH", google=client):
        response = await authz_google(request_fixture("testing"))
    assert response.status_code == 307
    mock_handled_user.assert_awaited_once()
    mock_get_jtw_userinfo.assert_awaited_once()


async def test_do_azure_login(
    request_fixture: Callable[[str], MagicMock],
) -> None:
    request = request_fixture("testing")
    request.url_for.return_value = "https://testing.fluids/en/azure.html"
    response = await do_azure_login(request)
    assert response.status_code == 302
    assert response.headers["location"].startswith(
        "https://login.microsoftonline.com/common/oauth2/"
    )
    request.url_for.assert_called_once()


async def test_do_bitbucket_login(
    request_fixture: Callable[[str], MagicMock],
) -> None:
    request = request_fixture("testing")
    request.url_for.return_value = (
        "https://testing.fluids/en/authz_bitbucket.html"
    )
    response = await do_bitbucket_login(request)
    assert response.status_code == 302
    assert response.headers["location"].startswith(
        "https://bitbucket.org/site/oauth2/"
    )
    request.url_for.assert_called_once()
