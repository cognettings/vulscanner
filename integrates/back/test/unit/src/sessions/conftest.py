from custom_exceptions import (
    ExpiredToken,
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
    encode_token,
)
from sessions.utils import (
    calculate_hash_token,
)
from settings import (
    SESSION_COOKIE_AGE,
)
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Optional,
    Union,
)

MOCKED_DATA: Dict[str, Dict[str, Any]] = {
    "sessions.domain.decode_token": {
        "api_token": {
            "user_email": "unitTest@fluidattacks.com",
            "sub": "api_token",
        },
        "starlette_session": {
            "user_email": "UNITTEST@fluidattacks.com",
            "sub": "starlette_session",
        },
        "test_get_jwt_content_catches_ExpiredToken_Error": ExpiredToken(),
    },
    "sessions.domain.verify_session_token": {
        "api_token": None,
        "starlette_session": None,
    },
}


@pytest.fixture(scope="session")
def mocked_data_for_module() -> Dict[str, Dict[str, Any]]:
    return MOCKED_DATA


@pytest.fixture
def create_token() -> (
    Callable[
        [Optional[str]], Generator[Union[str, Dict[str, str]], None, None]
    ]
):
    def _create_token(
        subject: Optional[str] = None,
    ) -> Generator[Union[str, Dict[str, str]], None, None]:
        expiration_time: int = datetime_utils.get_as_epoch(
            datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)
        )
        payload: Dict[str, str] = {
            "user_email": "unittest@fluidattacks.com",
            "jti": calculate_hash_token()["jti"],
        }
        token: str = encode_token(
            expiration_time=expiration_time,
            payload=payload,
            subject=subject if subject else "",
        )
        yield token
        yield payload

    return _create_token
