from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from tap_zoho_crm.api import (
    ApiClient,
)
from tap_zoho_crm.api.bulk import (
    BulkData,
    BulkJobId,
    BulkJobObj,
    ModuleName,
)
from tap_zoho_crm.api.common import (
    PageIndex,
)
from tap_zoho_crm.api.users import (
    UsersDataPage,
    UserType,
)
from tap_zoho_crm.core import (
    bulk,
)
from tap_zoho_crm.db import (
    Client as DbClient,
)
from typing import (
    Callable,
    FrozenSet,
)


@dataclass(frozen=True)
class IBulk:
    create: Callable[[ModuleName, int], Cmd[None]]
    update_all: Cmd[None]
    get_all: Cmd[FrozenSet[BulkJobObj]]
    extract_data: Callable[[FrozenSet[BulkJobId]], Cmd[FrozenSet[BulkData]]]


@dataclass(frozen=True)
class IUsers:
    get_users: Callable[[UserType, PageIndex], Cmd[UsersDataPage]]


@dataclass(frozen=True)
class CoreClient:
    users: IUsers
    bulk: IBulk


def new_client(api_client: ApiClient, db_client: DbClient) -> CoreClient:
    return CoreClient(
        IUsers(api_client.users.get_users),
        IBulk(
            lambda m, page: bulk.create_bulk_job(
                api_client.bulk, db_client, m, page
            ),
            bulk.update_all(api_client.bulk, db_client),
            db_client.get_bulk_jobs,
            lambda jobs_id: bulk.get_bulk_data(api_client.bulk, jobs_id),
        ),
    )
