from ._objs import (
    BulkJob,
    BulkJobId,
    BulkJobObj,
    BulkJobResult,
    ModuleName,
)
from fa_purity import (
    ResultE,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonUnfolder,
    JsonValue,
    Unfolder,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveUnfolder,
)


def _to_str(value: JsonValue) -> ResultE[str]:
    return Unfolder.to_primitive(value).bind(JsonPrimitiveUnfolder.to_str)


def decode_bulk_job(
    raw: JsonObj, module: ModuleName, page: int, result: BulkJobResult | None
) -> ResultE[BulkJob]:
    operation_result = JsonUnfolder.require(raw, "operation", _to_str)
    created_by_result = JsonUnfolder.require(
        raw,
        "created_by",
        lambda x: Unfolder.to_json(x).bind(
            lambda j: JsonUnfolder.require(j, "name", _to_str)
        ),
    )
    created_time_result = JsonUnfolder.require(raw, "created_time", _to_str)
    state_result = JsonUnfolder.require(raw, "state", _to_str)
    return operation_result.bind(
        lambda operation: created_by_result.bind(
            lambda created_by: created_time_result.bind(
                lambda created_time: state_result.map(
                    lambda state: BulkJob(
                        operation,
                        created_by,
                        created_time,
                        state,
                        module,
                        page,
                        result,
                    )
                )
            )
        )
    )


def decode_bulk_job_obj(
    raw: JsonObj, module: ModuleName, page: int, result: BulkJobResult | None
) -> ResultE[BulkJobObj]:
    id_result = JsonUnfolder.require(raw, "id", _to_str).map(BulkJobId)
    return id_result.bind(
        lambda i: decode_bulk_job(raw, module, page, result).map(
            lambda j: BulkJobObj(i, j)
        )
    )
