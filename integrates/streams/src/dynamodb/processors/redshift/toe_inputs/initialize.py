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

METADATA_TABLE: str = "toe_inputs_metadata"


def _initialize_metadata_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                attacked_at TIMESTAMPTZ,
                attacked_by VARCHAR,
                be_present BOOLEAN,
                be_present_until TIMESTAMPTZ,
                first_attack_at TIMESTAMPTZ,
                group_name VARCHAR,
                has_vulnerabilities BOOLEAN,
                root_id VARCHAR,
                seen_at TIMESTAMPTZ,
                seen_first_time_by VARCHAR,

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
