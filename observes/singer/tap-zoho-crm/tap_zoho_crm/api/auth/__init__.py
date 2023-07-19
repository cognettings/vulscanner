from . import (
    _access,
    _refresh,
    _revoke,
)
from ._core import (
    Credentials,
    RefreshToken,
    Token,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.json_2 import (
    JsonObj,
)
import logging

ACCOUNTS_URL = "https://accounts.zoho.com"  # for US region
LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class AuthApi:
    new_access_token: Cmd[Token]
    manual_new_refresh_token: Cmd[RefreshToken]
    manual_revoke_token: Cmd[JsonObj]


@dataclass(frozen=True)
class AuthApiFactory:
    @staticmethod
    def auth_api(creds: Credentials) -> AuthApi:
        return AuthApi(
            _access.new_access_token(creds),
            _refresh.generate_refresh_token(creds),
            _revoke.revoke_refresh_token(),
        )


__all__ = [
    "Credentials",
    "RefreshToken",
    "Token",
]
