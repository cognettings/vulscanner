from fa_purity import (
    FrozenDict,
    ResultE,
)
from fa_purity.json_2 import (
    JsonPrimitiveUnfolder,
    JsonValue,
    JsonValueFactory,
    Unfolder,
)
from target_s3 import (
    _utils,
)
from target_s3.executor import (
    MultifileConf,
)
from typing import (
    IO,
)


def decode_multifile_conf(raw: JsonValue) -> ResultE[MultifileConf]:
    return Unfolder.to_dict_of(
        raw,
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_int),
    ).bind(
        lambda d: _utils.get_required(d, "chunks").bind(
            lambda chunks: _utils.get_required(d, "parts").map(
                lambda parts: MultifileConf(chunks, parts)
            )
        )
    )


def decode_full_conf(file: IO[str]) -> ResultE[FrozenDict[str, MultifileConf]]:
    return (
        JsonValueFactory.load(file)
        .bind(
            lambda j: Unfolder.to_dict_of(
                JsonValue.from_json(j),
                lambda r: decode_multifile_conf(r).alt(
                    lambda e: ValueError(
                        f"A json value is not a `MultifileConf` i.e. {str(e)}"
                    )
                ),
            )
        )
        .alt(lambda e: ValueError(f"`decode_full_conf` failed i.e. {str(e)}"))
    )
