from __future__ import (
    annotations,
)

from ._plain_record import (
    PlainRecord,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    FrozenDict,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_singer_io.singer import (
    SingerSchema,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class CompletePlainRecord:
    """
    `PlainRecord` that has all and only the fields specified on the related schema.
    """

    _private: _Private = field(repr=False, hash=False, compare=False)
    schema: SingerSchema
    record: PlainRecord

    @staticmethod
    def new(
        schema: SingerSchema, record: PlainRecord
    ) -> ResultE[CompletePlainRecord]:
        """
        Fills missing record fields (according to the schema) with `None` values
        """
        if schema.stream != record.stream:
            err = ValueError(
                f"Stream mismatch between schema and record: {schema.stream} != {record.stream}"
            )
            return Result.failure(err, CompletePlainRecord).alt(Exception)
        return (
            Maybe.from_optional(schema.schema.encode().get("properties"))
            .to_result()
            .alt(
                lambda _: ValueError(
                    f"Missing `properties` key at schema of stream `{schema.stream}`"
                )
            )
            .alt(Exception)
            .bind(
                lambda p: Unfolder(p)
                .to_json()
                .alt(Exception)
                .map(
                    lambda props: FrozenDict(
                        {i: record.record.get(i) for i in props}
                    )
                )
            )
            .map(
                lambda f: CompletePlainRecord(
                    _Private(), schema, PlainRecord.new(schema.stream, f)
                )
            )
        )
