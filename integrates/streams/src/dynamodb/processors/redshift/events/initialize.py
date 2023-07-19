from ..operations import (
    db_cursor,
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from psycopg2 import (
    sql,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)

METADATA_TABLE: str = "events_metadata"


def _initialize_metadata_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                created_by VARCHAR,
                created_date TIMESTAMPTZ,
                event_date TIMESTAMPTZ,
                group_name VARCHAR,
                hacker VARCHAR,
                root_id VARCHAR,
                solution_reason VARCHAR,
                solving_date TIMESTAMPTZ,
                status VARCHAR,
                type VARCHAR,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    with db_cursor() as cursor:
        initialize_schema(cursor)
        _initialize_metadata_table(cursor)
