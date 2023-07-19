from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
    JsonValue,
    Maybe,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
from fa_purity.json.primitive.factory import (
    to_opt_primitive,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from target_s3.core import (
    CompletePlainRecord,
    PlainRecord,
    RecordGroup,
)
from typing import (
    FrozenSet,
    Tuple,
)

LOG = logging.getLogger(__name__)


def _truncate_row(
    row: FrozenList[Primitive], _limit: int
) -> FrozenList[Primitive]:
    limit = _limit if _limit >= -1 else -1

    def _truncate(prim: Primitive) -> Primitive:
        if isinstance(prim, str):
            return prim[0:limit] if limit >= 0 else prim
        return prim

    return tuple(_truncate(r) for r in row)


def _ordered_data(record: CompletePlainRecord) -> FrozenList[Primitive]:
    def _key(item: Tuple[str, Primitive]) -> str:
        return item[0]

    items = tuple(record.record.record.items())
    ordered = sorted(items, key=_key)
    return tuple(i[1] for i in ordered)


def _is_datetime(schema: JsonValue) -> ResultE[bool]:
    "schema represents a datetime type?"

    def _err_handle(e: Exception) -> Exception:
        return Exception(f"Failed `_is_datetime` with input {schema} i.e. {e}")

    def _inner(data: FrozenDict[str, Unfolder]) -> ResultE[bool]:
        _type = (
            Maybe.from_optional(data.get("type"))
            .to_result()
            .alt(lambda _: Exception("Missing `type` key"))
            .bind(lambda u: u.to_primitive(str).alt(Exception))
        )
        _format: ResultE[Maybe[str]] = (
            Maybe.from_optional(data.get("format"))
            .map(
                lambda u: u.to_primitive(str)
                .alt(lambda _: Exception("Expected `str` at `format` key"))
                .map(lambda x: Maybe.from_value(x))
            )
            .value_or(Result.success(Maybe.empty()))
        )
        return _type.bind(
            lambda t: _format.map(
                lambda f: t == "string" and f.value_or(None) == "date-time"
            )
        ).alt(_err_handle)

    return (
        Unfolder(schema)
        .to_unfolder_dict()
        .alt(Exception)
        .bind(_inner)
        .alt(_err_handle)
    )


def _format_datetime_on_record(
    datetime_props: FrozenSet[str], record: CompletePlainRecord
) -> ResultE[CompletePlainRecord]:
    "Format datetime properties"

    def _to_prim(item: str) -> Primitive:
        return item

    def _adjust(key: str, value: Primitive) -> ResultE[Primitive]:
        if key in datetime_props:
            return (
                to_opt_primitive(value, str)
                .map(
                    lambda x: _to_prim(
                        isoparse(x).strftime("%Y-%m-%d %H:%M:%S")
                    )
                    if x
                    else None
                )
                .alt(
                    lambda e: Exception(
                        f"Failed `_adjust` with inputs ({key}, {value}) i.e. {e}"
                    )
                )
            )
        return Result.success(value)

    def _log(item: ResultE[Tuple[str, Primitive]]) -> bool:
        LOG.warning(item)
        return False

    _records = all_ok(
        pure_map(
            lambda p: _adjust(p[0], p[1]).map(lambda a: (p[0], a)),
            tuple(record.record.record.items()),
        )
        .filter(lambda r: r.map(lambda _: True).or_else_call(lambda: _log(r)))
        .transform(lambda x: tuple(x))
    ).map(lambda l: FrozenDict(dict(l)))
    return _records.bind(
        lambda r: CompletePlainRecord.new(
            record.schema, PlainRecord.new(record.schema.stream, r)
        )
    )


def _format_datetime_on_group(group: RecordGroup) -> RecordGroup:
    datetime_properties = (
        Maybe.from_optional(group.schema.schema.encode().get("properties"))
        .to_result()
        .alt(lambda _: Exception("Missing `properties` key"))
        .bind(lambda j: Unfolder(j).to_json().alt(Exception))
        .map(lambda d: tuple(d.items()))
        .map(
            lambda p: tuple(
                pure_map(
                    lambda i: _is_datetime(i[1])
                    .map(lambda b: (i[0], b))
                    .alt(lambda e: Exception(f"In key `{i[0]}` i.e. {e}")),
                    p,
                )
            )
        )
        .bind(lambda x: all_ok(x).map(lambda y: from_flist(y)))
        .map(lambda p: p.filter(lambda t: t[1]).map(lambda x: x[0]))
        .map(lambda x: frozenset(x))
    )
    records = datetime_properties.map(
        lambda p: group.records.map(
            lambda c: _format_datetime_on_record(p, c)
            .alt(raise_exception)
            .unwrap()
        )
    ).unwrap()
    return RecordGroup.new(group.schema, records)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class RawFormatedRecord:
    _private: _Private = field(repr=False, hash=False, compare=False)
    record: FrozenList[Primitive]

    @staticmethod
    def format_group_records(
        group: RecordGroup, str_limit: int
    ) -> PureIter[RawFormatedRecord]:
        return (
            _format_datetime_on_group(group)
            .records.map(_ordered_data)
            .map(lambda r: _truncate_row(r, str_limit))
            .map(lambda r: RawFormatedRecord(_Private(), r))
        )
