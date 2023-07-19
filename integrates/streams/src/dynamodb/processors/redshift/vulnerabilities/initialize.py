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

METADATA_TABLE: str = "vulnerabilities_metadata"
STATE_TABLE: str = "vulnerabilities_state"
TREATMENT_TABLE: str = "vulnerabilities_treatment"
VERIFICATION_TABLE: str = "vulnerabilities_verification"
ZERO_RISK_TABLE: str = "vulnerabilities_zero_risk"


def _initialize_metadata_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                custom_severity INTEGER,
                finding_id VARCHAR NOT NULL,
                skims_method VARCHAR,
                type VARCHAR NOT NULL,

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
                modified_date TIMESTAMPTZ NOT NULL,
                modified_by VARCHAR NOT NULL,
                source VARCHAR NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, STATE_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_treatment_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                accepted_until TIMESTAMPTZ,
                acceptance_status VARCHAR,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, TREATMENT_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_verification_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, VERIFICATION_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_zero_risk_table(cursor: cursor_cls) -> None:
    execute(
        cursor,
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, ZERO_RISK_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    with db_cursor() as cursor:
        initialize_schema(cursor)
        _initialize_metadata_table(cursor)
        _initialize_state_table(cursor)
        _initialize_treatment_table(cursor)
        _initialize_verification_table(cursor)
        _initialize_zero_risk_table(cursor)
