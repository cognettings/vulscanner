from dataclasses import (
    dataclass,
)
from fa_purity import (
    ResultE,
)
from fa_purity.cmd import (
    Cmd,
    CmdUnwrapper,
)
from fa_purity.frozen import (
    freeze,
    FrozenDict,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitiveUnfolder,
    JsonUnfolder,
    JsonValue,
    LegacyAdapter,
    Unfolder,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_singer_io.singer import (
    deserializer,
    emitter,
    SingerMessage,
    SingerRecord,
)
import logging
from shutil import (
    copyfile,
)
import sys
from tap_csv import (
    core,
)
from tap_csv.core import (
    AdjustCsvOptions,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    IO,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class TapCsvInput:
    stream: str
    csv_path: str
    options: AdjustCsvOptions


def _to_bool(raw: JsonValue) -> ResultE[bool]:
    return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_bool)


def _to_str(raw: JsonValue) -> ResultE[str]:
    return Unfolder.to_primitive(raw).bind(JsonPrimitiveUnfolder.to_str)


def _extract_options(raw: JsonObj) -> ResultE[AdjustCsvOptions]:
    file_schema_result = JsonUnfolder.optional(
        raw, "file_schema", lambda v: Unfolder.to_dict_of(v, _to_str)
    )
    empty: FrozenDict[str, str] = freeze({})
    return JsonUnfolder.optional(raw, "quote_nonnum", _to_bool).bind(
        lambda quote_nonnum: JsonUnfolder.optional(
            raw, "add_default_types", _to_bool
        ).bind(
            lambda add_default_types: JsonUnfolder.optional(
                raw, "pkeys_present", _to_bool
            ).bind(
                lambda pkeys_present: JsonUnfolder.optional(
                    raw, "only_records", _to_bool
                ).bind(
                    lambda only_records: file_schema_result.map(
                        lambda file_schema: AdjustCsvOptions(
                            quote_nonnum.value_or(False),
                            add_default_types.value_or(False),
                            pkeys_present.value_or(False),
                            only_records.value_or(False),
                            file_schema.value_or(empty),
                        )
                    )
                )
            )
        )
    )


def _decode_tap_input(record: SingerRecord) -> ResultE[TapCsvInput]:
    _record = LegacyAdapter.json(record.record)
    csv_path = JsonUnfolder.require(_record, "csv_path", _to_str)
    options = JsonUnfolder.require(_record, "options", Unfolder.to_json).bind(
        _extract_options
    )
    return csv_path.bind(
        lambda csv: options.map(
            lambda opt: TapCsvInput(record.stream, csv, opt)
        )
    )


def _process_csv_files(conf: TapCsvInput) -> Cmd[None]:
    def _action(unwrap: CmdUnwrapper) -> None:
        LOG.debug("Tap input %s", conf)
        with NamedTemporaryFile(
            "w+", encoding="UTF-8", delete=False
        ) as temp_data:
            LOG.debug("Copying %s -> %s", conf.csv_path, temp_data.name)
            copyfile(conf.csv_path, temp_data.name)
            unwrap.act(core.to_singer(temp_data, conf.stream, conf.options))

    return Cmd.new_cmd(_action)


def _process_msg(msg: SingerMessage) -> Cmd[None]:
    if isinstance(msg, SingerRecord):
        return (
            _decode_tap_input(msg)
            .map(_process_csv_files)
            .value_or(emitter.emit(sys.stdout, msg))
        )
    return emitter.emit(sys.stdout, msg)


def process_file(file: IO[str]) -> Cmd[None]:
    return deserializer.from_file(file).map(_process_msg).transform(consume)
