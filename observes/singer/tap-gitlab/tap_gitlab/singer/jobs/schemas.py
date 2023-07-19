from decimal import (
    Decimal,
)
from fa_purity import (
    FrozenDict,
    JsonValue,
    PureIter,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_list,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
)
from fa_singer_io.json_schema.factory import (
    datetime_schema,
    from_json,
    from_prim_type,
    opt_datetime_schema,
    opt_prim_type,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from tap_gitlab.singer._core import (
    SingerStreams,
)

_int_type = JsonValue(from_prim_type(int).encode())
_big_int_type = JsonValue(
    JSchemaFactory.from_json(
        freeze(dict(from_prim_type(int).encode()) | {"size": JsonValue("big")})
    )
    .unwrap()
    .encode()
)
_str_type = JsonValue(from_prim_type(str).encode())
_bool_type = JsonValue(from_prim_type(bool).encode())
_opt_big_int_type = JsonValue(
    JSchemaFactory.from_json(
        freeze(dict(opt_prim_type(int).encode()) | {"size": JsonValue("big")})
    )
    .unwrap()
    .encode()
)
_opt_str_type = JsonValue(opt_prim_type(str).encode())
_opt_float_type = JsonValue(opt_prim_type(float).encode())
_datetime_type = JsonValue(datetime_schema().encode())
_optdatetime_type = JsonValue(opt_datetime_schema().encode())


def job_tags_schema() -> SingerSchema:
    properties = FrozenDict(
        {
            "job_id": _big_int_type,
            "project_id": _str_type,
            "tag": _str_type,
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.job_tags.value,
        from_json(schema).unwrap(),
        frozenset(["job_id", "project_id", "tag"]),
        None,
    ).unwrap()


def jobs_schema() -> SingerSchema:
    properties = FrozenDict(
        {
            "job_id": _big_int_type,
            "project_id": _str_type,
            "pipe_id": _big_int_type,
            "name": _str_type,
            "user_id": _int_type,
            "runner_id": _opt_big_int_type,
            "coverage": _opt_float_type,
            "commit": _str_type,
            "created_at": _datetime_type,
            "started_at": _optdatetime_type,
            "finished_at": _optdatetime_type,
            "allow_failure": _bool_type,
            "ref_branch": _str_type,
            "stage": _str_type,
            "status": _str_type,
            "failure_reason": _opt_str_type,
            "duration": JsonValue(opt_prim_type(Decimal).encode()),
            "queued_duration": JsonValue(opt_prim_type(Decimal).encode()),
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.jobs.value,
        from_json(schema).unwrap(),
        frozenset(["project_id", "job_id"]),
        None,
    ).unwrap()


def all_schemas() -> PureIter[SingerSchema]:
    return from_list([job_tags_schema(), jobs_schema()])
