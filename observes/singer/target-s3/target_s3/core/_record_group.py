from __future__ import (
    annotations,
)

from ._complete_record import (
    CompletePlainRecord,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    JsonObj,
    Maybe,
    PureIter,
    Result,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerSchema,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class RecordGroup:
    """
    Group of CompletePlainRecord that share same schema
    """

    _private: _Private = field(repr=False, hash=False, compare=False)
    schema: SingerSchema
    records: PureIter[CompletePlainRecord]

    @staticmethod
    def filter(
        schema: SingerSchema, records: PureIter[CompletePlainRecord]
    ) -> RecordGroup:
        items = records.filter(lambda r: r.schema == schema)
        return RecordGroup(_Private(), schema, items)

    @staticmethod
    def new(
        schema: SingerSchema, records: PureIter[CompletePlainRecord]
    ) -> RecordGroup:
        """
        [WARNING] because PureIter is lazy evaluated the records of
        the `RecordGroup` will provably raise an error. i.e. the
        correct return type of this funcion is a `RecordGroup`
        with `records: PureIter[CompletePlainRecord | NoReturn]`
        """
        items = (
            records.map(
                lambda r: Result.success(r, CompletePlainRecord)
                if r.schema == schema
                else Result.failure(r, CompletePlainRecord)
            )
            .map(
                lambda r: r.alt(
                    lambda x: ValueError(
                        "A record does not belong to the RecordGroup."
                        f" Expected schema `{schema}` but got `{x.schema}`"
                        f"i.e. at record {x}"
                    )
                )
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )
        return RecordGroup(_Private(), schema, items)

    @property
    def json_schema_properties(self) -> Maybe[JsonObj]:
        return Maybe.from_optional(
            self.schema.schema.encode().get("properties")
        ).map(
            lambda j: Unfolder(j)
            .to_json()
            .alt(lambda e: Exception(f"Decode error json_schema i.e. {e}"))
            .unwrap()
        )
