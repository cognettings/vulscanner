from collections.abc import (
    Iterator,
)
from contextlib import (
    contextmanager,
)
from dynamodb.context import (
    FI_AWS_REDSHIFT_DBNAME,
    FI_AWS_REDSHIFT_HOST,
    FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_USER,
    FI_ENVIRONMENT,
)
from dynamodb.decorators import (
    retry_on_exceptions,
)
import logging
import psycopg2
from psycopg2 import (
    Error,
    extras,
    InternalError,
    OperationalError,
    sql,
)
from psycopg2.errors import (
    QueryCanceled,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)
SCHEMA_NAME: str = "integrates"
AWS_REDSHIFT_PORT = 5439


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    try:
        connection = psycopg2.connect(
            dbname=FI_AWS_REDSHIFT_DBNAME,
            host=FI_AWS_REDSHIFT_HOST,
            password=FI_AWS_REDSHIFT_PASSWORD,
            port=AWS_REDSHIFT_PORT,
            user=FI_AWS_REDSHIFT_USER,
        )
    except OperationalError as exc:
        LOGGER.error(exc)
        return
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        cursor: cursor_cls = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    finally:
        connection.close()


def initialize_schema(cursor: cursor_cls) -> None:
    LOGGER.info("Ensuring %s schema exists...", SCHEMA_NAME)
    execute(
        cursor,
        sql.SQL(
            """
            CREATE SCHEMA IF NOT EXISTS {schema_name}
            """
        ).format(
            schema_name=sql.Identifier(SCHEMA_NAME),
        ),
    )


def execute(
    cursor: cursor_cls,
    sql_query: sql.Composed,
    sql_vars: dict[str, Any] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        try:
            retry_on_exceptions(
                exceptions=(OperationalError, InternalError, Error),
                max_attempts=3,
                sleep_seconds=10,
            )(cursor.execute)(sql_query, sql_vars)
        except Error as exc:
            LOGGER.exception(
                exc,
                extra={"query": sql_query, "vars": sql_vars},
            )


def execute_many(
    cursor: cursor_cls,
    sql_query: sql.Composed,
    sql_vars: list[dict[str, Any]] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        try:
            retry_on_exceptions(
                exceptions=(
                    OperationalError,
                    InternalError,
                    Error,
                    QueryCanceled,
                ),
                max_attempts=3,
                sleep_seconds=10,
            )(cursor.executemany)(sql_query, sql_vars)
        except Error as exc:
            LOGGER.exception(exc, extra={"query": sql_query, "vars": sql_vars})
            raise


@retry_on_exceptions(
    exceptions=(OperationalError, InternalError, Error),
    max_attempts=3,
    sleep_seconds=10,
)
def execute_batch(
    cursor: cursor_cls,
    sql_query: sql.Composed,
    sql_vars: list[dict[str, Any]] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        extras.execute_batch(cursor, sql_query, sql_vars, page_size=1000)
