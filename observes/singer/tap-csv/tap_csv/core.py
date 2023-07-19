from .auto_cast import (
    auto_cast,
)
import csv
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    PureIter,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitive,
    JsonValue,
    JsonValueFactory,
    LegacyAdapter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
    JsonSchema,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
    SingerSchema,
)
import logging
import sys
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    Dict,
    IO,
    List,
    Optional,
)

LOG = logging.getLogger(__name__)


class ColumnType(Enum):
    FLOAT = "float"
    STRING = "string"
    NUMBER = "number"
    DATE_TIME = "datetime"
    INT = "integer"
    BOOL = "bool"


@dataclass(frozen=True)
class MetadataRows:
    field_names_row: int
    field_types_row: int
    pkeys_row: Optional[int] = None


@dataclass(frozen=True)
class AdjustCsvOptions:
    quote_nonnum: bool
    add_default_types: bool
    pkeys_present: bool
    only_records: bool
    file_schema: FrozenDict[str, str]


prim_from_list = JsonValueFactory.from_list
_str = JsonPrimitive.from_str


def translate_types(raw_field_type: Dict[str, ColumnType]) -> JsonSchema:
    """Translates type names into JSON SCHEMA types."""
    transform: Dict[ColumnType, JsonObj] = {
        ColumnType.STRING: freeze(
            {"type": JsonValue.from_primitive(_str("string"))}
        ),
        ColumnType.NUMBER: freeze(
            {"type": prim_from_list(["number", "null"])}
        ),
        ColumnType.DATE_TIME: freeze(
            {"type": prim_from_list(["string", "null"])}
        ),
        ColumnType.FLOAT: freeze({"type": prim_from_list(["number", "null"])}),
        ColumnType.BOOL: freeze(
            {"type": JsonValue.from_primitive(_str("boolean"))}
        ),
        ColumnType.INT: freeze({"type": prim_from_list(["integer", "null"])}),
    }
    field_type: JsonObj = freeze(
        {
            key: JsonValue.from_json(transform[val])
            for key, val in raw_field_type.items()
        }
    )
    j_schema = freeze({"properties": JsonValue.from_json(field_type)})
    return JSchemaFactory.from_json(
        LegacyAdapter.to_legacy_json(j_schema)
    ).unwrap()


def translate_values(
    name_type_map: Dict[str, ColumnType],
    name_value_map: Dict[str, str],
    auto_type: bool = False,
) -> JsonObj:
    def _to_float(raw: str) -> JsonValue:
        if raw:
            return JsonValue.from_primitive(
                JsonPrimitive.from_float(float(raw))
            )
        return JsonValue.from_primitive(JsonPrimitive.empty())

    def _to_bool(raw: str) -> JsonValue:
        if raw:
            return JsonValue.from_primitive(JsonPrimitive.from_bool(bool(raw)))
        return JsonValue.from_primitive(JsonPrimitive.empty())

    def _to_int(raw: str) -> JsonValue:
        if raw:
            return JsonValue.from_primitive(JsonPrimitive.from_int(int(raw)))
        return JsonValue.from_primitive(JsonPrimitive.empty())

    transform: Dict[ColumnType, Callable[[str], JsonValue]] = {
        ColumnType.STRING: lambda x: JsonValue.from_primitive(
            JsonPrimitive.from_str(x)
        ),
        ColumnType.NUMBER: _to_float,
        ColumnType.DATE_TIME: lambda x: JsonValue.from_primitive(
            JsonPrimitive.from_str(x)
        ),
        ColumnType.FLOAT: _to_float,
        ColumnType.BOOL: _to_bool,
        ColumnType.INT: _to_int,
    }

    def cast_function(name: str, value: str) -> JsonValue:
        if auto_type:
            return auto_cast(value)
        return transform[name_type_map[name]](value)

    return (
        from_flist(tuple(name_value_map.items()))
        .map(lambda x: (x[0], cast_function(x[0], x[1])))
        .transform(lambda i: freeze(dict(i)))
    )


def add_default_types(
    field_names: PureIter[str], options: AdjustCsvOptions
) -> Dict[str, str]:
    field_types = field_names.map(
        lambda name: (
            name,
            options.file_schema.get(name.lower(), ColumnType.STRING.value),
        )
    )
    result = dict(field_types)
    LOG.debug("added types: %s", result)
    return result


def get_fields(file: IO[str]) -> PureIter[str]:
    source_reader = csv.DictReader(file)
    if source_reader.fieldnames:
        return from_flist(tuple(source_reader.fieldnames))
    raise Exception("Missing fieldnames")


def _adjust_csv(
    source_file: IO[str],
    destination: IO[str],
    field_names: PureIter[str],
    options: AdjustCsvOptions,
) -> Cmd[None]:
    def _action() -> None:
        source_reader = csv.DictReader(source_file, field_names.to_list())
        dest_writer = csv.DictWriter(
            destination,
            field_names.to_list(),
            quoting=csv.QUOTE_NONNUMERIC
            if options.quote_nonnum
            else csv.QUOTE_MINIMAL,
        )
        types_row: int = 3 if options.pkeys_present else 2
        dest_writer.writeheader()
        row_num = 1
        for row in source_reader:  # type: ignore[misc]
            if row_num == types_row - 1 and options.add_default_types:
                field_types = add_default_types(field_names, options)
                LOG.debug("Write row: %s", field_types)
                dest_writer.writerow(field_types)
                row_num = row_num + 1
            LOG.debug("Writing row: %s", row)  # type: ignore[misc]
            dest_writer.writerow(row)  # type: ignore[misc]
            row_num = row_num + 1

    return Cmd.from_cmd(_action)


def adjust_csv(source: IO[str], options: AdjustCsvOptions) -> Cmd[str]:
    if not (options.quote_nonnum or options.add_default_types):
        return Cmd.from_cmd(lambda: source.name)

    field_names = get_fields(source)

    def _action(unwrap: CmdUnwrapper) -> str:
        LOG.debug("field names: %s", field_names.to_list())
        with NamedTemporaryFile("w+", encoding="UTF-8", delete=False) as out:
            unwrap.act(_adjust_csv(source, out, field_names, options))
            return out.name

    return Cmd.new_cmd(_action)


@dataclass
class MutableState:
    row_num: int
    pkeys: List[str]
    field_names: List[str]
    name_type_map: Dict[str, ColumnType]
    name_value_map: Dict[str, str]


def process_csv_row(
    meta_rows: MetadataRows,
    options: AdjustCsvOptions,
    record: List[str],
    stream: str,
    state: MutableState,
) -> Cmd[None]:
    _meta_row_nums = frozenset(
        [
            meta_rows.field_names_row,
            meta_rows.pkeys_row,
            meta_rows.field_types_row,
        ]
    )
    do_nothing = Cmd.from_cmd(lambda: None)
    if state.row_num in _meta_row_nums:
        if state.row_num == meta_rows.field_names_row:
            state.field_names = record
            return do_nothing
        if state.row_num == meta_rows.pkeys_row:
            state.pkeys = record
            return do_nothing
        if state.row_num == meta_rows.field_types_row:
            LOG.debug(
                "name_type_map: %s", tuple(zip(state.field_names, record))
            )
            state.name_type_map = (
                from_flist(tuple(zip(state.field_names, record)))
                .map(lambda x: (x[0], ColumnType(x[1])))
                .transform(dict)
            )
            if not options.only_records:
                singer_schema: SingerSchema = SingerSchema.new(
                    stream,
                    translate_types(state.name_type_map),
                    frozenset(state.pkeys),
                    None,
                ).unwrap()
                return emitter.emit(sys.stdout, singer_schema)
            return do_nothing
        return do_nothing
    else:
        state.name_value_map = dict(zip(state.field_names, record))
        singer_record: SingerRecord = SingerRecord(
            stream,
            LegacyAdapter.to_legacy_json(
                translate_values(
                    state.name_type_map,
                    state.name_value_map,
                    options.only_records,
                )
            ),
            None,
        )
        return emitter.emit(sys.stdout, singer_record)


def to_singer(
    csv_file: IO[str],
    stream: str,
    options: AdjustCsvOptions,
) -> Cmd[None]:
    LOG.debug("csv file: %s", csv_file.name)
    # ==== TAP ================================================================
    # line 1, field names
    # line 2, primary field(s)
    # line 3 (or 2 if pkeys are missing), field types:
    #           - string   "example"
    #           - number   "123.4"
    #           - datetime "2019-12-31T16:48:32Z" (MUST be RFC3339 compliant)
    # line >3, records
    # finally:
    #           - use "null" value with "string" type for empty cells

    def emit_singer(procesed_csv: IO[str]) -> Cmd[None]:
        def _action(unwrap: CmdUnwrapper) -> None:
            reader = csv.reader(procesed_csv, delimiter=",", quotechar='"')
            meta_rows = MetadataRows(
                field_names_row=1,
                field_types_row=3 if options.pkeys_present else 2,
                pkeys_row=2 if options.pkeys_present else None,
            )
            LOG.debug("rows: %s", meta_rows)
            state = MutableState(0, [], [], {}, {})
            for record in reader:
                state.row_num += 1
                unwrap.act(
                    process_csv_row(meta_rows, options, record, stream, state)
                )

        return Cmd.new_cmd(_action)

    def _action(unwrap: CmdUnwrapper) -> None:
        _csv = unwrap.act(adjust_csv(csv_file, options))
        with open(_csv, mode="r", encoding="utf-8") as file:
            unwrap.act(emit_singer(file))

    return Cmd.new_cmd(_action)
