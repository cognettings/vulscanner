from back.test.unit.src.utils import (
    get_module_at_test,
)
from context import (
    FI_JWT_SECRET_API_RS512,
    FI_JWT_SECRET_RS512,
)
from custom_exceptions import (
    ExpiredToken,
)
from freezegun import (
    freeze_time,
)
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jws import (
    InvalidJWSSignature,
)
from jwcrypto.jwt import (
    JWT,
)
import pytest
from sessions.utils import (
    decode_jwe,
    get_secret,
    validate_expiration_time,
)
from typing import (
    Callable,
    Dict,
    Generator,
    Optional,
    Union,
)

pytestmark = [
    pytest.mark.asyncio,
]

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


def test_get_secret_session_token(
    create_token: Callable[
        [Optional[str]], Generator[Union[str, Dict[str, str]], None, None]
    ],
) -> None:
    secret = get_secret(JWT(jwt=next(create_token("starlette_session"))))
    assert secret == FI_JWT_SECRET_RS512


def test_get_secret_api_token(
    create_token: Callable[
        [Optional[str]], Generator[Union[str, Dict[str, str]], None, None]
    ]
) -> None:
    secret = get_secret(JWT(jwt=next(create_token("api_token"))))
    assert secret == FI_JWT_SECRET_API_RS512


def test_decode_jwe(
    create_token: Callable[
        [Optional[str]], Generator[Union[str, Dict[str, str]], None, None]
    ]
) -> None:
    token_generator = create_token("")
    jwt_token = JWT(jwt=next(token_generator))
    secret = get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    jwt_token.validate(jws_key)
    decoded_payload = decode_jwe(jwt_token.token.payload)
    assert decoded_payload == next(token_generator)


def test_invalid_token_signature(
    create_token: Callable[
        [Optional[str]], Generator[Union[str, Dict[str, str]], None, None]
    ]
) -> None:
    jwt_token = JWT(jwt=next(create_token("api_token")))
    secret = get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    with pytest.raises(InvalidJWSSignature):
        jwt_token.validate(jws_key)


@pytest.mark.parametrize(
    ["expiration_time"],
    [
        [1673452711],
        ["2023-01-11T15:58:31.280182"],
        [None],
    ],
)
@freeze_time("2022-11-11T15:58:31.280182")
def test_validate_expiration_time(
    expiration_time: Union[str, int, None]
) -> None:
    payload: Dict[str, Union[str, int, None]] = {
        "user_email": "unittest@fluidattacks.com",
        "exp": expiration_time,
    }
    if expiration_time is None:
        payload.pop("exp")
    assert validate_expiration_time(payload) == payload


@pytest.mark.parametrize(
    ["expiration_time"],
    [
        [1673452711],
        ["2023-01-11T15:58:31.280182"],
    ],
)
def test_validate_expiration_time_expired_token(
    expiration_time: Union[str, int, None]
) -> None:
    payload: Dict[str, Union[str, int, None]] = {
        "user_email": "unittest@fluidattacks.com",
        "exp": expiration_time,
    }
    with pytest.raises(ExpiredToken):
        validate_expiration_time(payload)
