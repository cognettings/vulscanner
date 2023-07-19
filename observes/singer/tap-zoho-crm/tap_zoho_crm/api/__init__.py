from .bulk import (
    BulkJobApi,
    BulkJobApiFactory,
)
from .users import (
    UsersApi,
    UsersApiFactory,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from tap_zoho_crm.api.auth import (
    AuthApiFactory,
    Credentials,
)


@dataclass(frozen=True)
class ApiClient:
    bulk: BulkJobApi
    users: UsersApi


@dataclass(frozen=True)
class ApiClientFactory:
    @staticmethod
    def new_client(credentials: Credentials) -> Cmd[ApiClient]:
        token = AuthApiFactory.auth_api(credentials).new_access_token
        return token.map(
            lambda t: ApiClient(
                BulkJobApiFactory.bulk_job_api(t),
                UsersApiFactory.users_api(t),
            )
        )
