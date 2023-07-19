from ._decode import (
    decode_bulk_job,
)
from ._objs import (
    BulkJob,
    BulkJobId,
    BulkJobObj,
    BulkJobResult,
    ModuleName,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    ResultE,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonUnfolder,
    JsonValue,
    Primitive,
    UnfoldedFactory,
    Unfolder,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from pure_requests import (
    basic,
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


def _require_first_item(raw: JsonObj) -> ResultE[JsonObj]:
    return JsonUnfolder.require(raw, "data", Unfolder.to_list).bind(
        lambda items: _decode.require_index(items, 0).bind(Unfolder.to_json)
    )


def _to_int(value: JsonValue) -> ResultE[int]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_int)


def _to_str(value: JsonValue) -> ResultE[str]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_str)


def _to_bool(value: JsonValue) -> ResultE[bool]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_bool)


def _decode_job_result(raw: JsonObj) -> ResultE[BulkJobResult]:
    return JsonUnfolder.require(raw, "page", _to_int).bind(
        lambda page: JsonUnfolder.require(raw, "count", _to_int).bind(
            lambda count: JsonUnfolder.require(
                raw, "download_url", _to_str
            ).bind(
                lambda download_url: JsonUnfolder.require(
                    raw, "more_records", _to_bool
                ).map(
                    lambda more_records: BulkJobResult(
                        page, count, download_url, more_records
                    )
                )
            )
        )
    )


def _decode_bulk_job(raw: JsonObj) -> ResultE[BulkJob]:
    module_page_result = JsonUnfolder.require(
        raw,
        "query",
        lambda j: Unfolder.to_json(j).bind(
            lambda v: JsonUnfolder.require(
                v,
                "module",
                lambda c: Unfolder.to_primitive(c)
                .bind(JsonPrimitiveUnfolder.to_str)
                .bind(ModuleName.from_raw),
            ).bind(
                lambda module: JsonUnfolder.require(
                    v,
                    "page",
                    lambda x: Unfolder.to_primitive(x)
                    .bind(JsonPrimitiveUnfolder.to_int)
                    .map(lambda page: (module, page)),
                ),
            )
        ),
    )
    bulk_result = JsonUnfolder.optional(
        raw, "result", lambda v: Unfolder.to_json(v).bind(_decode_job_result)
    )
    return bulk_result.bind(
        lambda r: module_page_result.bind(
            lambda t: decode_bulk_job(raw, t[0], t[1], r.value_or(None))
        )
    )


def get_bulk_job(token: Token, job_id: BulkJobId) -> Cmd[BulkJob]:
    msg = Cmd.from_cmd(lambda: LOG.info("API: Get bulk job #%s", job_id))
    endpoint = f"{API_ENDPOINT}/" + job_id.job_id
    headers: Dict[str, Primitive] = {
        "Authorization": "Zoho-oauthtoken " + token.raw_token
    }
    empty: JsonObj = FrozenDict({})
    response = (
        basic.get(endpoint, UnfoldedFactory.from_dict(headers), empty)
        .map(lambda r: r.unwrap())
        .map(lambda r: _decode.decode_json(r).unwrap())
    )
    return msg + response.map(_require_first_item).map(
        lambda r: r.alt(
            lambda _: ValueError("Missing job_id: " + job_id.__repr__())
        )
        .alt(raise_exception)
        .unwrap()
    ).map(_decode_bulk_job).map(
        lambda r: r.alt(
            lambda e: ValueError(f"Get BulkJob decode failed i.e. {e}")
        )
        .alt(raise_exception)
        .unwrap()
    )
