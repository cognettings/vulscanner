from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenList,
)
from fa_purity.json_2 import (
    JsonObj,
)
from tap_zoho_crm.api.common import (
    DataPageInfo,
)


class UserType(Enum):
    ANY = "AllUsers"


@dataclass(frozen=True)
class UsersDataPage:
    data: FrozenList[JsonObj]
    info: DataPageInfo
