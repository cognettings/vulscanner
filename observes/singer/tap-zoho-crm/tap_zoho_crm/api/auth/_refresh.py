from ._core import (
    Credentials,
    RefreshToken,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    ResultE,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitiveUnfolder,
    JsonUnfolder,
    Primitive,
    UnfoldedFactory,
    Unfolder,
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
from typing import (
    Dict,
)

ACCOUNTS_URL = "https://accounts.zoho.com"  # for US region
LOG = logging.getLogger(__name__)


def _decode(raw: JsonObj) -> ResultE[RefreshToken]:
    return JsonUnfolder.require(
        raw,
        "refresh_token",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    ).map(RefreshToken)


def _user_input_code() -> Cmd[str]:
    def _action() -> str:
        LOG.info("Paste grant token:")
        return getpass()

    return Cmd.from_cmd(_action)


def generate_refresh_token(
    credentials: Credentials,
) -> Cmd[RefreshToken]:
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token"
    msg = Cmd.from_cmd(
        lambda: LOG.info(
            "Generating refresh token with scopes: %s",
            ",".join(credentials.scopes),
        )
    )

    def _data(grant_token_code: str) -> JsonObj:
        raw: Dict[str, Primitive] = {
            "grant_type": "authorization_code",
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "code": grant_token_code,
        }
        return UnfoldedFactory.from_dict(raw)

    empty: JsonObj = FrozenDict({})
    response = msg + _user_input_code().bind(
        lambda code: basic.post(endpoint, empty, empty, _data(code))
    )
    return response.map(lambda r: decode_json(r.unwrap()).unwrap()).map(
        lambda j: _decode(j).unwrap()
    )
