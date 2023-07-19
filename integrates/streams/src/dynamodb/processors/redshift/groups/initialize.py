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

CODE_LANGUAGES_TABLE = "groups_code_languages"
METADATA_TABLE = "groups_metadata"
STATE_TABLE = "groups_state"


def _initialize_code_languages_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                group_name VARCHAR,
                language VARCHAR,
                loc INTEGER,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, CODE_LANGUAGES_TABLE),
        ),
    )


def _initialize_metadata_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                created_by VARCHAR,
                created_date TIMESTAMPTZ,
                language VARCHAR,
                name VARCHAR,
                organization_id VARCHAR,
                sprint_duration INTEGER,
                sprint_start_date TIMESTAMPTZ,

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
                comments VARCHAR,
                has_machine BOOLEAN,
                has_squad BOOLEAN,
                justification VARCHAR,
                managed VARCHAR,
                modified_by VARCHAR,
                modified_date TIMESTAMPTZ,
                pending_deletion_date TIMESTAMPTZ,
                service VARCHAR,
                status VARCHAR,
                tier VARCHAR,
                type VARCHAR,

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
        _initialize_code_languages_table(cursor)
        _initialize_state_table(cursor)
