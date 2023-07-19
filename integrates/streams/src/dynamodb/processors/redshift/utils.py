from .operations import (
    SCHEMA_NAME,
)
from .queries import (
    SQL_INSERT_HISTORIC,
    SQL_INSERT_METADATA,
    SQL_INSERT_VERIFICATION_VULNS_IDS,
)
from dataclasses import (
    fields,
)
from psycopg2 import (
    sql,
)
from typing import (
    Any,
)


def format_sql_query_metadata(
    table_name: str, _fields: list[str]
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_METADATA).format(
        table=sql.Identifier(SCHEMA_NAME, table_name),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def format_sql_query_historic(
    table_historic: str, table_metadata: str, _fields: list[str]
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_HISTORIC).format(
        table_historic=sql.Identifier(SCHEMA_NAME, table_historic),
        table_metadata=sql.Identifier(SCHEMA_NAME, table_metadata),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def format_sql_query_verification_vulns_ids(
    table_vulns_ids: str,
    table_metadata: str,
    _fields: list[str],
) -> sql.Composed:
    return sql.SQL(SQL_INSERT_VERIFICATION_VULNS_IDS).format(
        table_vulns_ids=sql.Identifier(SCHEMA_NAME, table_vulns_ids),
        table_metadata=sql.Identifier(SCHEMA_NAME, table_metadata),
        fields=sql.SQL(", ").join(map(sql.Identifier, _fields)),
        values=sql.SQL(", ").join(map(sql.Placeholder, _fields)),
    )


def get_query_fields(table_row_class: Any) -> list[str]:
    return list(f.name for f in fields(table_row_class))
