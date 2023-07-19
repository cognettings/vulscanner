from ..operations import (
    execute,
    execute_many,
)
from ..utils import (
    format_sql_query_metadata,
    get_query_fields,
)
from .initialize import (
    CODE_LANGUAGES_TABLE,
    METADATA_TABLE,
)
from .types import (
    CodeLanguagesTableRow,
    MetadataTableRow,
)
from .utils import (
    format_row_code_languages,
    format_row_metadata,
)
from dynamodb.types import (
    Item,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)


def insert_code_languages(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    sql_fields = get_query_fields(CodeLanguagesTableRow)
    sql_values = format_row_code_languages(item=item)
    if not sql_values:
        return
    execute_many(
        cursor,
        format_sql_query_metadata(CODE_LANGUAGES_TABLE, sql_fields),
        sql_values,
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


def insert_root(
    *,
    cursor: cursor_cls,
    item: Item,
) -> None:
    insert_metadata(cursor=cursor, item=item)
    insert_code_languages(cursor=cursor, item=item)
