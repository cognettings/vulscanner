from ._bins import (
    BinPaths,
)
from dynamo_etl_conf._run import (
    external_run,
)
from fa_purity.cmd import (
    Cmd,
)
from redshift_client.id_objs import (
    SchemaId,
)
from typing import (
    FrozenSet,
    Literal,
)


def _to_str(num: int) -> str:
    return str(num)


def determine_schema(
    tables: FrozenSet[str],
    segments: int,
    max_concurrency: int,
    cache_bucket: str,
) -> Cmd[None]:
    args = (
        BinPaths.DETERMINE_SCHEMAS.value,
        " ".join(tables),
        _to_str(segments),
        _to_str(max_concurrency),
        cache_bucket,
    )
    return external_run(args)


def prepare_loading(loading_schema: SchemaId, cache_bucket: str) -> Cmd[None]:
    args = (
        BinPaths.PREPARE_LOADING.value,
        loading_schema.name,
        cache_bucket,
    )
    return external_run(args)


def parallel_phase_1(
    total_segments: int, segment: int | Literal["auto"]
) -> Cmd[None]:
    args = (
        BinPaths.DYNAMO_CORE_PHASE_1.value,
        _to_str(total_segments),
        _to_str(segment) if isinstance(segment, int) else segment,
    )
    return external_run(args)


def parallel_phase_3(segment: int | Literal["auto"]) -> Cmd[None]:
    args = (
        BinPaths.DYNAMO_CORE_PHASE_3.value,
        _to_str(segment) if isinstance(segment, int) else segment,
    )
    return external_run(args)
