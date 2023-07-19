from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections import (
    defaultdict,
)
from custom_exceptions import (
    InvalidAuthorization,
    SecureAccessException,
)
from custom_utils import (
    datetime as datetime_utils,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest
from sessions.domain import (
    check_session_web_validity,
    decode_token,
    encode_token,
    get_jwt_content,
    get_request_store,
)
from settings import (
    SESSION_COOKIE_AGE,
)
from typing import (
    Any,
    Callable,
    Dict,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    Mock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


@pytest.mark.parametrize(
    ["expiration_time", "payload", "subject"],
    [
        [1683681291, {"user_email": "unittest@fluidattacks.com"}, "api_token"],
        [
            1683681291,
            {"user_email": "unittest@fluidattacks.com"},
            "starlette_session",
        ],
    ],
)
def test_encode_token(
    expiration_time: int, payload: Dict[str, str], subject: str
) -> None:
    response = encode_token(
        expiration_time, payload, subject, subject == "api_token"
    )
    assert response


@pytest.mark.parametrize(
    ["expiration_time", "payload", "subject"],
    [[1683681291, {"user_email": "unittest@fluidattacks.com"}, "api_token"]],
)
def test_decode_token_catches_jwt_expired(
    expiration_time: int, payload: Dict[str, str], subject: str
) -> None:
    token = encode_token(
        expiration_time, payload, subject, subject == "api_token"
    )
    with pytest.raises(InvalidAuthorization):
        decode_token(token)


@pytest.mark.parametrize(
    ["payload", "subject"],
    [[{"user_email": "unittest@fluidattacks.com"}, "api_token"]],
)
def test_decode_token(
    payload: Dict[str, str],
    subject: str,
) -> None:
    expiration_time = datetime_utils.get_as_epoch(
        datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
    )
    token = encode_token(
        expiration_time, payload, subject, subject == "api_token"
    )
    decoded_token = decode_token(token)
    assert decoded_token == {
        "user_email": "unittest@fluidattacks.com",
        "exp": expiration_time,
        "sub": "api_token",
    }


@pytest.mark.parametrize(
    ["token"],
    [
        ["token_whit_invalid_format"],
        ["invalid.format."],
    ],
)
def test_decode_token_catches_value_error(token: str) -> None:
    with pytest.raises(InvalidAuthorization):
        decode_token(token)


@pytest.mark.parametrize(
    ["expected_output"],
    [
        [
            {
                "user_email": "unittest@fluidattacks.com",
                "sub": "starlette_session",
            },
        ],
        [
            {
                "user_email": "unittest@fluidattacks.com",
                "sub": "api_token",
            },
        ],
    ],
)
@patch(MODULE_AT_TEST + "verify_session_token", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "decode_token")
async def test_get_jwt_content(
    # pylint: disable=too-many-arguments
    mock_decode_token: Mock,
    mock_verify_session_token: AsyncMock,
    request_fixture: Callable[[str], MagicMock],
    get_mocked_data: Callable[[Dict[str, Dict[str, Any]], str, str, str], Any],
    mocked_data_for_module: Dict[str, Dict[str, Any]],
    expected_output: Dict[str, str | int],
) -> None:
    mock_decode_token.return_value = get_mocked_data(  # type: ignore
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="decode_token",
        mock_key=expected_output["sub"],
        module_at_test=MODULE_AT_TEST,
    )
    mock_verify_session_token.side_effect = get_mocked_data(  # type: ignore
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="verify_session_token",
        mock_key=expected_output["sub"],
        module_at_test=MODULE_AT_TEST,
    )
    assert (
        await get_jwt_content(request_fixture("starlette_session"))
        == expected_output
    )
    if expected_output["sub"] == "starlette_session":
        mock_verify_session_token.assert_called_once()
    mock_decode_token.assert_called_once()


async def test_get_jwt_content_catches_index_error(
    request_fixture: Callable[[str], MagicMock]
) -> None:
    request = request_fixture("api_token")
    request.headers["Authorization"] = "ERROR"
    with pytest.raises(InvalidAuthorization):
        await get_jwt_content(request)


@patch(MODULE_AT_TEST + "decode_token")
async def test_get_jwt_content_catches_expired_token_error(
    mock_decode_token: Mock,
    request_fixture: Callable[[str], MagicMock],
    get_mocked_data: Callable[[Dict[str, Dict[str, Any]], str, str, str], Any],
    mocked_data_for_module: Dict[str, Dict[str, Any]],
) -> None:
    mock_decode_token.side_effect = get_mocked_data(  # type:ignore
        mocked_data=mocked_data_for_module,
        mocked_functionality_path="decode_token",
        mock_key="test_get_jwt_content_catches_ExpiredToken_Error",
        module_at_test=MODULE_AT_TEST,
    )
    with pytest.raises(InvalidAuthorization):
        await get_jwt_content(request_fixture("starlette_session"))


@pytest.mark.parametrize(
    ["attribute", "value"],
    [
        ["store", defaultdict()],
        ["state", defaultdict()],
    ],
)
def test_get_request_store(
    attribute: str,
    value: defaultdict,
) -> None:
    # pylint: disable=too-few-public-methods
    class Context:
        def __init__(self) -> None:
            self.state = Mock()

    request = Context()
    if attribute == "state":
        setattr(request.state, "store", value)
    else:
        setattr(request, attribute, value)
    assert get_request_store(request) == value


async def test_check_session_web_validity_no_session_key(
    request_fixture: Callable[[str], MagicMock]
) -> None:
    request: MagicMock = request_fixture("testing")
    request.session.pop("session_key")
    with pytest.raises(SecureAccessException):
        await check_session_web_validity(request, "testing@fluidattacks.com")


@patch(
    MODULE_AT_TEST + "get_session_key", AsyncMock(return_value="f2Mu6UsPXT")
)
@patch(MODULE_AT_TEST + "remove_session_key", AsyncMock(side_effect=None))
async def test_check_session_web_validity_session_or_cookie_expired(
    request_fixture: Callable[[str], MagicMock],
) -> None:
    with pytest.raises(SecureAccessException):
        await check_session_web_validity(
            request_fixture("starlette_session"), "testing@fluidattacks.com"
        )


@pytest.mark.parametrize(["is_current"], [[False], [True], [None]])
@patch(
    MODULE_AT_TEST + "get_session_key", AsyncMock(return_value="f2Mu6UsPXT8")
)
@patch(
    MODULE_AT_TEST + "stakeholders_model.update_metadata",
    AsyncMock(side_effect=None),
)
async def test_check_session_web_validity(
    request_fixture: Callable[[str], MagicMock],
    is_current: bool | None,
) -> None:
    request: MagicMock = request_fixture("starlette_session")
    request.session["is_concurrent"] = is_current
    await check_session_web_validity(request, "testing@fluidattacks.com")
