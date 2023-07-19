from ._core import (
    Credentials,
    Token,
)
from dataclasses import (
    dataclass,
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
    JsonValue,
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
import requests
from tap_zoho_crm._decode import (
    decode_json,
)
from typing import (
    Dict,
    FrozenSet,
)

ACCOUNTS_URL = "https://accounts.zoho.com"  # for US region
LOG = logging.getLogger(__name__)


def _decode(raw: JsonObj) -> ResultE[Token]:
    return JsonUnfolder.require(
        raw,
        "access_token",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    ).map(Token)


def new_access_token(credentials: Credentials) -> Cmd[Token]:
    LOG.info("Generating access token")
    endpoint = f"{ACCOUNTS_URL}/oauth/v2/token"
    params: Dict[str, Primitive] = {
        "refresh_token": credentials.refresh_token,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "grant_type": "refresh_token",
    }
    empty: JsonObj = FrozenDict({})
    response = basic.post(
        endpoint, empty, UnfoldedFactory.from_dict(params), empty
    )
    data = response.map(lambda r: decode_json(r.unwrap()).unwrap())

    return data.map(lambda j: _decode(j).unwrap())
