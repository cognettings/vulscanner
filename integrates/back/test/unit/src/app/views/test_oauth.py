from app.views.oauth import (
    _begin_repo_oauth,
    _end_repo_oauth,
    _generate_name,
    _get_fast_track_org,
    _get_organization_id,
    _get_params_from_uri,
    AZURE_REDIRECT_URI,
    get_authorized_redirect,
    RepoProvider,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
from custom_exceptions import (
    CredentialAlreadyExists,
)
from datetime import (
    datetime,
)
from freezegun import (
    freeze_time,
)
import pytest
from starlette.responses import (
    RedirectResponse,
    Response,
)
from typing import (
    Callable,
    Dict,
    List,
    Tuple,
    Union,
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
    ["provider"], [[RepoProvider.AZURE], [RepoProvider.GITLAB]]
)
async def test_get_authorized_redirect(
    provider: RepoProvider,
    request_fixture: Callable[[str], MagicMock],
) -> None:
    def url_for(name: Union[str, RepoProvider]) -> str:
        return f"http://base_url/{name}"

    query_params: Dict[str, str] = {
        "code": "3t4syd",
        "subject": "434223ewr49204wkf02",
    }
    request: MagicMock = request_fixture("testing")
    request.configure_mock(
        **{"url_for": url_for, "query_params": query_params}
    )
    response: Response = await get_authorized_redirect(request, provider)
    assert response.status_code == 302
    response.headers["location"].endswith(
        f"{url_for(provider)}?code=3t4syd&subject=434223ewr49204wkf02"
    )


@pytest.mark.parametrize(
    ["test_case"],
    [["fast_track_in_query_params"], ["fast_track_no_in_query_params"]],
)
@patch(MODULE_AT_TEST + "get_authorized_redirect", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_jwt_content", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "_validate", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "validate_credentials_oauth", new_callable=AsyncMock)
async def test_begin_repo_oauth(
    # pylint: disable=too-many-arguments
    mock_validate_credentials: AsyncMock,
    mock_validate: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    mock_get_authorized_redirect: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: dict,
    test_case: str,
) -> None:
    mocks_info: List[Tuple[str, AsyncMock]] = [
        ("get_jwt_content", mock_get_jwt_content),
        ("get_authorized_redirect", mock_get_authorized_redirect),
        ("_validate", mock_validate),
        ("validate_credentials_oauth", mock_validate_credentials),
    ]
    for functionality, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key="test_begin_repo_oauth",
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=True,
        )
    request = request_fixture("testing")
    request.query_params["subject"] = "434223ewr49204wkf02"
    if test_case == "fast_track_in_query_params":
        request.query_params["fast_track"] = True

    await _begin_repo_oauth(request, RepoProvider.BITBUCKET)
    mock_get_authorized_redirect.assert_awaited_once_with(
        request, RepoProvider.BITBUCKET
    )
    if test_case == "fast_track_no_in_query_params":
        for _, mock in mocks_info:
            mock.assert_awaited_once()


@pytest.mark.parametrize(
    ["test_case"], [["PermissionError"], ["CredentialAlreadyExists"]]
)
@patch(MODULE_AT_TEST + "get_authorized_redirect", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_jwt_content", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "_validate", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "validate_credentials_oauth", new_callable=AsyncMock)
async def test_begin_repo_oauth_redirects_home(
    # pylint: disable=too-many-arguments
    mock_validate_credentials: AsyncMock,
    mock_validate: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    mock_get_authorized_redirect: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: dict,
    test_case: str,
) -> None:
    mocks_info: List[Tuple[str, AsyncMock]] = [
        ("get_authorized_redirect", mock_get_authorized_redirect),
        ("get_jwt_content", mock_get_jwt_content),
        ("_validate", mock_validate),
        ("validate_credentials_oauth", mock_validate_credentials),
    ]
    for functionality, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key=test_case,
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=True,
        )
    request = request_fixture("testing")
    request.query_params["subject"] = "434223ewr49204wkf02"

    response: Response = await _begin_repo_oauth(
        request, RepoProvider.BITBUCKET
    )
    assert response.status_code == 307
    assert response.headers["location"] == "/home"
    mock_get_authorized_redirect.assert_not_awaited()
    if test_case == "CredentialAlreadyExists":
        for _, mock in mocks_info[1:]:
            mock.assert_awaited_once()


@pytest.mark.parametrize(
    ["test_case"],
    [
        ["no_code_in_query_params"],
        ["no_subject_in_query_params"],
        ["error_when_awaiting_get_secret"],
    ],
)
@patch(MODULE_AT_TEST + "_get_organization_id", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "get_jwt_content",
    AsyncMock(return_value={"user_email": "testing@fluidattacks.com"}),
)
@patch(MODULE_AT_TEST + "_validate", AsyncMock(side_effect=None))
@patch(MODULE_AT_TEST + "_get_azure_secret", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "validate_credentials_name_in_organization",
    AsyncMock(side_effect=CredentialAlreadyExists()),
)
@patch(
    MODULE_AT_TEST + "validate_credentials_oauth",
    AsyncMock(side_effect=CredentialAlreadyExists()),
)
async def test_end_repo_oauth(
    # pylint: disable=too-many-arguments
    mock_get_azure_secret: AsyncMock,
    mock_get_organization_id: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: dict,
    test_case: str,
) -> None:
    mocks_info: List[Tuple[str, AsyncMock]] = [
        ("_get_azure_secret", mock_get_azure_secret),
        ("_get_organization_id", mock_get_organization_id),
    ]
    for functionality, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key=test_case,
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
            side_effect=True,
        )
    request: MagicMock = request_fixture("")
    request.configure_mock(query_params={})

    if test_case != "no_code_in_query_params":
        request.query_params["code"] = "mock_code"

    response: RedirectResponse = await _end_repo_oauth(
        request, RepoProvider.AZURE
    )
    assert response.status_code == 307
    if test_case != "no_code_in_query_params":
        mock_get_organization_id.assert_awaited_once_with(
            request, RepoProvider.AZURE
        )
        if test_case != "no_subject_in_query_params":
            mock_get_azure_secret.assert_awaited_once_with(request)


@pytest.mark.parametrize(
    ["test_case", "provider", "expected_id"],
    [
        ["azure_as_provider", RepoProvider.AZURE, "1404973626"],
        ["fast_track_in_query_params", RepoProvider.AZURE, "1404973626"],
        ["neither_azure_nor_fast_track", RepoProvider.GITHUB, "1404973626"],
    ],
)
@patch(MODULE_AT_TEST + "_get_fast_track_org")
async def test_get_organization_id(
    # pylint: disable=too-many-arguments
    mock_get_fast_track_org: MagicMock,
    test_case: str,
    provider: RepoProvider,
    expected_id: str,  # it is the same as in the conftest file
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict,
    set_mock: Callable,
) -> None:
    set_mock(
        mock=mock_get_fast_track_org,
        mocked_functionality_path="_get_fast_track_org",
        mock_key="test_get_organization_id",
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    request = request_fixture("testing")
    request.configure_mock(**{"query_params": {}})
    if test_case == "azure_as_provider":
        request.session[
            AZURE_REDIRECT_URI
        ] = f"azure.com/path?subject={expected_id}"
    elif test_case == "fast_track_in_query_params":
        request.query_params["fast_track"] = True
    request.query_params["subject"] = expected_id

    assert await _get_organization_id(request, provider) == expected_id


@patch(MODULE_AT_TEST + "orgs_domain.add_organization", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "groups_domain.add_group", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "stakeholders_domain.add_enrollment",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_jwt_content", new_callable=AsyncMock)
@freeze_time("2020-12-31T18:40:37+00:00")
async def test_get_fast_track_org(
    # pylint: disable=too-many-arguments
    mock_get_jwt_content: AsyncMock,
    mock_add_enrollment: AsyncMock,
    mock_add_group: AsyncMock,
    mock_add_org: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict,
    set_mock: Callable,
) -> None:
    mocks_info: List[Tuple[str, AsyncMock]] = [
        ("orgs_domain.add_organization", mock_add_org),
        ("groups_domain.add_group", mock_add_group),
        ("stakeholders_domain.add_enrollment", mock_add_enrollment),
        ("get_jwt_content", mock_get_jwt_content),
    ]

    for functionality, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=functionality,
            mock_key="test_get_fast_track_org",
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
        )
    request: MagicMock = request_fixture("testing")
    request.headers["cf-ipcountry"] = "CO"
    organization = await _get_fast_track_org(request)
    assert organization.name == "unitfluidattacks"
    assert organization.created_by == "unitest@fluidattacks.com"
    assert organization.country == "CO"
    assert organization.created_date == datetime(2020, 12, 31, 18, 40, 37)
    mock_get_jwt_content.assert_awaited_once_with(request)
    mock_add_enrollment.assert_awaited_once()
    mock_add_group.assert_awaited_once()
    mock_add_org.assert_awaited_once()


@pytest.mark.parametrize(
    ["email", "expected_output"],
    [
        ["s@testing.com", "stesting"],
        ["test_email@testing.com", "testetesting"],
        ["test2@testing_long_domain.com", "testtestinglon"],
    ],
)
async def test_generate_name(email: str, expected_output: str) -> None:
    generated_name: str = _generate_name(email)
    assert generated_name == expected_output


@pytest.mark.parametrize(
    ["uri"],
    [["https://testing.com/funtion?email=test@domain.com&&org=testing"]],
)
async def test_get_params_from_uri(uri: str) -> None:
    query_params = _get_params_from_uri(uri)
    assert str(query_params) == "email=test%40domain.com&org=testing"
