from . import (
    _get,
)
from ._objs import (
    UsersDataPage,
    UserType,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.lock import (
    ThreadLock,
)
import logging
from pure_requests.rate_limit import (
    RateLimiter,
)
from tap_zoho_crm.api.common import (
    API_URL,
    PageIndex,
    Token,
)
from typing import (
    Callable,
)

API_ENDPOINT = API_URL + "/crm/v2/users"
LOG = logging.getLogger(__name__)
_rate_limiter = ThreadLock.new().map(
    lambda lock: RateLimiter.new(10, 60, lock).unwrap()
)
rate_limiter = unsafe_unwrap(_rate_limiter)


@dataclass(frozen=True)
class UsersApi:
    get_users: Callable[[UserType, PageIndex], Cmd[UsersDataPage]]


@dataclass(frozen=True)
class UsersApiFactory:
    @staticmethod
    def users_api(token: Token) -> UsersApi:
        return UsersApi(
            lambda ut, p: _get.get_users(rate_limiter, token, ut, p)
        )
