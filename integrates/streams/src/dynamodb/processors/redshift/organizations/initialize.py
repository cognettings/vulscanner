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

METADATA_TABLE = "organizations_metadata"
STATE_TABLE = "organizations_state"


def _initialize_metadata_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                country VARCHAR,
                created_by VARCHAR,
                created_date TIMESTAMPTZ,
                name VARCHAR,

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


def _initialize_state_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_by VARCHAR,
                modified_date TIMESTAMPTZ,
                pending_deletion_date TIMESTAMPTZ,
                status VARCHAR,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """,
        ).format(
            table=sql.Identifier(SCHEMA_NAME, STATE_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    with db_cursor() as cursor:
        initialize_schema(cursor)
        _initialize_metadata_table(cursor)
        _initialize_state_table(cursor)
