import atexit
from collections.abc import (
    Iterator,
)
from context import (
    FI_AWS_REDSHIFT_DBNAME,
    FI_AWS_REDSHIFT_HOST,
    FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_PORT,
    FI_AWS_REDSHIFT_USER,
)
from contextlib import (
    contextmanager,
)
import psycopg2
from psycopg2.extensions import (
    connection as connection_cls,
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)

_cache: dict[str, connection_cls] = {}


def _db_connection() -> connection_cls:
    # _cache ensures that only 1 connection is used in the current machine
    if _cache.get("connection") is None:
        connection = psycopg2.connect(
            dbname=FI_AWS_REDSHIFT_DBNAME,
            host=FI_AWS_REDSHIFT_HOST,
            password=FI_AWS_REDSHIFT_PASSWORD,
            port=FI_AWS_REDSHIFT_PORT,
            user=FI_AWS_REDSHIFT_USER,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        _cache["connection"] = connection
        return connection
    return _cache["connection"]


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    try:
        cursor: cursor_cls = _db_connection().cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    except Exception as err:
        _db_connection().close()
        raise err


def exit_handler() -> None:
    # Handler for closing the connection when
    # the python interpreter terminates normally
    if _cache.get("connection"):
        _db_connection().close()


atexit.register(exit_handler)
