from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.json_2 import (
    JsonObj,
    UnfoldedFactory,
)
from getpass import (
    getpass,
)
import logging
from pure_requests import (
    basic,
)
from tap_zoho_crm._decode import (
    decode_json,
)

ACCOUNTS_URL = "https://accounts.zoho.com"  # for US region
LOG = logging.getLogger(__name__)


def _user_input() -> Cmd[str]:
    def _action() -> str:
        LOG.info("Refresh token to revoke:")
        return getpass()

    return Cmd.from_cmd(_action)


def revoke_refresh_token() -> Cmd[JsonObj]:
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token/revoke"
    empty: JsonObj = FrozenDict({})
    response = _user_input().bind(
        lambda refresh: basic.post(
            endpoint,
            empty,
            UnfoldedFactory.from_dict({"token": refresh}),
            empty,
        )
    )
    return response.map(lambda r: decode_json(r.unwrap()).unwrap()).bind(
        lambda j: Cmd.from_cmd(
            lambda: LOG.debug("revoke_refresh_token: %s", j)
        ).map(lambda _: j)
    )
