from app.views.evidence import (
    enforce_group_level_role,
    get_evidence,
    retrieve_image,
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
import os
import pytest
from starlette.responses import (
    Response,
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


@pytest.mark.parametrize("group", ["organization", "user"])
@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "authz.get_group_level_role", new_callable=AsyncMock)
async def test_enforce_group_level_role(
    # pylint: disable=too-many-arguments
    mock_get_group_level_role: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    group: str,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict,
    set_mock: Callable,
) -> None:
    mocks_info: list[tuple[AsyncMock, str]] = [
        (
            mock_get_jwt_content,
            "sessions_domain.get_jwt_content",
        ),
        (
            mock_get_group_level_role,
            "authz.get_group_level_role",
        ),
    ]

    for mock, mock_path in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=mock_path,
            mock_key=group,
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
        )
    loaders: Dataloaders = get_new_context()
    allowed_roles = [
        "admin",
        "architect",
        "customer_manager",
        "hacker",
        "reattacker",
        "resourcer",
        "reviewer",
        "user",
        "user_manager",
        "vulnerability_manager",
    ]
    response: Response | None = await enforce_group_level_role(
        loaders,
        request_fixture("testing"),
        group,
        *allowed_roles,
    )
    # the mock data for the group 'user' returns a not allowed role
    if group == "user" and response is not None:
        assert response.status_code == 403
    else:
        assert response is None
    mock_get_jwt_content.assert_called_once()
    mock_get_group_level_role.assert_called_once()


@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
async def test_enforce_group_level_role_catches_invalid_authorization(
    mock_get_jwt_content: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    mocked_data_for_module: dict,
    set_mock: Callable,
) -> None:
    set_mock(
        mock=mock_get_jwt_content,
        mocked_functionality_path="sessions_domain.get_jwt_content",
        mock_key="test_enforce_group_level_role_catches_invalid_authorization",
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    response = await enforce_group_level_role(
        MagicMock(),
        request_fixture("testing"),
        "user",
        *["user"],
    )
    assert response is not None
    assert response.status_code == 403
    assert response.body == b"Access denied"
    mock_get_jwt_content.assert_awaited_once()


@pytest.mark.parametrize(
    ["test_case", "expected_response"],
    [
        ["error_in_enforcer_group_level_role", b"Access denied"],
        [
            "wrong_evidence_type",
            b'{"data":[],"message":"Evidence type not found","error":true}',
        ],
        ["file_id_is_none", b"Error - Unsent image ID"],
        [
            "no_evidences",
            b'{"data":[],"message":"Access denied or evidence not found","error":true}',  # noqa: E501 pylint: disable=line-too-long
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "has_access_to_finding", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "enforce_group_level_role", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "list_s3_evidences", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "logs_utils.cloudwatch_log")
async def test_get_evidence_sad_paths(
    # pylint: disable=too-many-arguments,too-many-locals
    mock_logs_utils_cloudwatch_log: Mock,
    mock_list_s3_evidences: AsyncMock,
    mock_enforce_group_level_role: AsyncMock,
    mock_has_access_to_finding: AsyncMock,
    mock_get_jwt_content: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: dict,
    test_case: str,
    expected_response: bytes,
) -> None:
    mocks_info: list[tuple[str, MagicMock | AsyncMock]] = [
        ("list_s3_evidences", mock_list_s3_evidences),
        ("has_access_to_finding", mock_has_access_to_finding),
        ("enforce_group_level_role", mock_enforce_group_level_role),
        ("sessions_domain.get_jwt_content", mock_get_jwt_content),
    ]
    for mock_path, mock in mocks_info:
        set_mock(
            mock=mock,
            mocked_functionality_path=mock_path,
            mock_key=test_case,
            module_at_test=MODULE_AT_TEST,
            mocked_data=mocked_data_for_module,
        )

    mock_logs_utils_cloudwatch_log.side_effect = None

    request = request_fixture("testing")
    path_params = mocked_data_for_module[MODULE_AT_TEST + "request"][test_case]
    request.configure_mock(path_params=path_params)
    response: Response = await get_evidence(request)
    assert response.body == expected_response


@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
async def test_get_evidence_invalid_authorization(
    mock_get_jwt_content: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    set_mock: Callable,
    mocked_data_for_module: dict,
) -> None:
    set_mock(
        mock=mock_get_jwt_content,
        mocked_functionality_path="sessions_domain.get_jwt_content",
        mock_key="Invalid Authorization",
        module_at_test=MODULE_AT_TEST,
        mocked_data=mocked_data_for_module,
        side_effect=True,
    )
    response: Response = await get_evidence(request_fixture("testing"))
    assert response.template.name == "unauthorized.html"  # type: ignore


def test_retrieve_image_not_allowed_mime() -> None:
    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_path, "mock/resources/test_file.txt")
    response: Response = retrieve_image(file_path)
    assert response.body == b"Error: Invalid evidence image format"
