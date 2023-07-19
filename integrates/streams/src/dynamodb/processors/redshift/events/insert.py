from ..operations import (
    execute,
)
from ..utils import (
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    METADATA_TABLE,
)
from .types import (
    MetadataTableRow,
)
from .utils import (
    format_row_metadata,
)
from dynamodb.types import (
    Item,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)


def insert_metadata(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    sql_fields = get_query_fields(MetadataTableRow)
    sql_values = format_row_metadata(item)
    execute(
        cursor,
        format_sql_query_metadata(METADATA_TABLE, sql_fields),
        sql_values,
    )
