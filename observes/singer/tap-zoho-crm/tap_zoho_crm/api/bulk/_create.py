from ._decode import (
    decode_bulk_job_obj,
)
from ._objs import (
    BulkJobObj,
    ModuleName,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonUnfolder,
    JsonValue,
    JsonValueFactory,
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
    Token,
)
from typing import (
    Dict,
)

API_ENDPOINT = API_URL + "/crm/bulk/v2/read"
LOG = logging.getLogger(__name__)


def _details_unfolder(raw: JsonObj) -> ResultE[JsonObj]:
    return (
        JsonUnfolder.require(raw, "data", Unfolder.to_list)
        .bind(lambda i: _decode.require_index(i, 0))
        .bind(Unfolder.to_json)
        .bind(lambda j: JsonUnfolder.require(j, "details", Unfolder.to_json))
    )


def create_bulk_read_job(
    rate_limiter: RateLimiter, token: Token, module: ModuleName, page: int
) -> Cmd[BulkJobObj]:
    msg = Cmd.from_cmd(
        lambda: LOG.info("API: Create bulk job for %s @page:%s", module, page)
    )
    endpoint = API_ENDPOINT
    headers: Dict[str, Primitive] = {
        "Authorization": "Zoho-oauthtoken " + token.raw_token
    }
    _data: JsonObj = freeze(
        {
            "module": JsonValueFactory.from_unfolded(module.value),
            "page": JsonValueFactory.from_unfolded(page),
        }
    )
    data: JsonObj = freeze({"query": JsonValue.from_json(_data)})
    empty: JsonObj = FrozenDict({})
    response = basic.post(
        endpoint, UnfoldedFactory.from_dict(headers), empty, data
    )
    response_json = response.map(
        lambda r: _decode.decode_json(r.unwrap())
        .alt(lambda x: x.map(Exception, lambda y: y.map(Exception, Exception)))
        .alt(raise_exception)
        .unwrap()
    )

    cmd: Cmd[BulkJobObj] = msg + response_json.map(_details_unfolder).map(
        lambda r: r.unwrap()
    ).map(
        lambda j: decode_bulk_job_obj(j, module, page, None)
        .alt(
            lambda e: Exception(
                f"decode_bulk_job_obj error i.e. {e} @ {Unfolder.dumps(j)}"
            )
        )
        .alt(raise_exception)
        .unwrap()
    )

    return rate_limiter.call_or_wait(cmd)
