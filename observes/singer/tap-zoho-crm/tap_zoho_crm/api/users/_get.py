from ._objs import (
    UsersDataPage,
    UserType,
)
from fa_purity import (
    Cmd,
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
from fa_purity.utils import (
    raise_exception,
)
import logging
from pure_requests import (
    basic,
)
from pure_requests.rate_limit import (
    RateLimiter,
)
from tap_zoho_crm import (
    _decode,
)
from tap_zoho_crm.api.common import (
    API_URL,
    DataPageInfo,
    PageIndex,
    Token,
)
from typing import (
    Dict,
)

API_ENDPOINT = API_URL + "/crm/v2/users"
LOG = logging.getLogger(__name__)
require = JsonUnfolder.require


def _to_int(value: JsonValue) -> ResultE[int]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_int)


def _to_bool(value: JsonValue) -> ResultE[bool]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_bool)


def _decode_info(raw: JsonObj) -> ResultE[DataPageInfo]:
    page_index_result = require(raw, "page", _to_int).bind(
        lambda page: require(raw, "per_page", _to_int).map(
            lambda per_page: PageIndex(page, per_page)
        )
    )
    return require(raw, "count", _to_int).bind(
        lambda count: require(raw, "more_records", _to_bool).bind(
            lambda more_records: page_index_result.map(
                lambda p: DataPageInfo(p, count, more_records)
            )
        )
    )


def _decode_users(raw: JsonObj) -> ResultE[UsersDataPage]:
    users_result = require(
        raw, "users", lambda u: Unfolder.to_list_of(u, Unfolder.to_json)
    )
    info = require(
        raw, "info", lambda r: Unfolder.to_json(r).bind(_decode_info)
    )
    return users_result.bind(
        lambda users: info.map(lambda info: UsersDataPage(users, info))
    )


def get_users(
    limiter: RateLimiter, token: Token, user_type: UserType, page_i: PageIndex
) -> Cmd[UsersDataPage]:
    msg = Cmd.from_cmd(lambda: LOG.info("API: Get users (%s)", user_type))
    endpoint = API_ENDPOINT
    headers: Dict[str, Primitive] = {
        "Authorization": "Zoho-oauthtoken " + token.raw_token
    }
    params: Dict[str, Primitive] = {
        "type": user_type.value,
        "page": page_i.page,
        "per_page": page_i.per_page,
    }
    cmd: Cmd[UsersDataPage] = msg + basic.get(
        endpoint,
        UnfoldedFactory.from_dict(headers),
        UnfoldedFactory.from_dict(params),
    ).map(lambda r: r.unwrap()).map(
        lambda r: _decode.decode_json(r).unwrap()
    ).map(
        lambda j: _decode_users(j)
        .alt(
            lambda e: Exception(
                f"_decode_users failed i.e. {e} @ {Unfolder.dumps(j)}"
            )
        )
        .alt(raise_exception)
        .unwrap()
    )
    return limiter.call_or_wait(cmd)
