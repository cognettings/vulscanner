from .utf8_truncation import (
    utf8_byte_truncate,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from redshift_client.core.column import (
    Column,
)
from redshift_client.core.data_type.core import (
    PrecisionType,
    PrecisionTypes,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client import (
    RowData,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)


def _truncate_str(column: Column, item: PrimitiveVal) -> PrimitiveVal:
    def _precision_type(value: PrecisionType) -> PrimitiveVal:
        if value.data_type in (
            PrecisionTypes.CHAR,
            PrecisionTypes.VARCHAR,
        ):
            if isinstance(item, str):
                return utf8_byte_truncate(item, value.precision).unwrap()
            if column.nullable and item is None:
                return item
            raise Exception(
                f"`CHAR` or `VARCHAR` item must be an str instance; got {type(item)}"
            )
        return item

    return column.data_type.map(
        lambda _: item,
        _precision_type,
        lambda _: item,
    )


def truncate_row(table: Table, row: RowData) -> RowData:
    columns = pure_map(
        lambda c: (c[0], table.columns[c[1]]), tuple(enumerate(table.order))
    )
    trucated = columns.map(lambda c: _truncate_str(c[1], row.data[c[0]]))
    return RowData(tuple(trucated))
