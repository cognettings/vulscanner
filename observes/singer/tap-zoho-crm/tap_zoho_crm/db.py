from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Result,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
import logging
from redshift_client.sql_client import (
    Query,
    QueryValues,
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from tap_zoho_crm.api.bulk import (
    BulkJob,
    BulkJobId,
    BulkJobObj,
    ModuleName,
)
from typing import (
    Callable,
    FrozenSet,
)

LOG = logging.getLogger(__name__)
SCHEMA = "zoho_crm"


@dataclass(frozen=True)
class Client:
    get_bulk_jobs: Cmd[FrozenSet[BulkJobObj]]
    save_bulk_job: Callable[[BulkJobObj], Cmd[None]]
    update_bulk_job: Callable[[BulkJobObj], Cmd[None]]


def _to_primitive(item: PrimitiveVal) -> ResultE[JsonPrimitive]:
    if isinstance(item, datetime):
        return Result.failure(Exception(TypeError("datetime not expected")))
    return Result.success(JsonPrimitiveFactory.from_raw(item))


def _decode_bulkjob(item: RowData) -> ResultE[BulkJobObj]:
    try:

        def _item_to_str(index: int) -> ResultE[str]:
            return _to_primitive(item.data[index]).bind(
                JsonPrimitiveUnfolder.to_str
            )

        module_raw = _item_to_str(5).bind(ModuleName.from_raw)
        page_raw = _to_primitive(item.data[6]).bind(
            JsonPrimitiveUnfolder.to_int
        )
        return _item_to_str(0).bind(
            lambda op: _item_to_str(1).bind(
                lambda created_by: _item_to_str(2).bind(
                    lambda created_time: _item_to_str(3).bind(
                        lambda state: _item_to_str(4).bind(
                            lambda _id: module_raw.bind(
                                lambda module: page_raw.map(
                                    lambda page: BulkJobObj(
                                        BulkJobId(_id),
                                        BulkJob(
                                            op,
                                            created_by,
                                            created_time,
                                            state,
                                            module,
                                            page,
                                            None,
                                        ),
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    except IndexError as err:
        return Result.failure(Exception(err))


def _get_bulk_jobs(
    client: SqlClient, db_schema: str
) -> Cmd[FrozenSet[BulkJobObj]]:
    statement = "SELECT * FROM {schema_name}.bulk_jobs"
    identifiers: FrozenDict[str, str] = freeze({"schema_name": db_schema})
    query = Query.dynamic_query(statement, identifiers)
    results = client.execute(query, None) + client.fetch_all()
    x = results.map(lambda r: pure_map(_decode_bulkjob, r)).map(
        lambda i: all_ok(i.to_list()).map(lambda x: frozenset(x))
    )
    return x.map(lambda r: r.unwrap())


def _save_bulk_job(
    client: SqlClient, job: BulkJobObj, db_schema: str
) -> Cmd[None]:
    statement = """
        INSERT INTO {schema_name}.bulk_jobs VALUES (
            %(operation)s,
            %(created_by)s,
            %(created_time)s,
            %(state)s,
            %(id)s,
            %(module)s,
            %(page)s
        )
    """
    identifiers: FrozenDict[str, str] = freeze({"schema_name": db_schema})
    query = Query.dynamic_query(
        statement,
        identifiers,
    )
    args: FrozenDict[str, PrimitiveVal] = freeze(
        {
            "operation": job.job.operation,
            "created_by": job.job.created_by,
            "created_time": job.job.created_time,
            "state": job.job.state,
            "id": job.job_id.job_id,
            "module": job.job.module.value,
            "page": job.job.page,
        }
    )
    return client.execute(query, QueryValues(args))


def _update_bulk_job(
    client: SqlClient, job: BulkJobObj, db_schema: str
) -> Cmd[None]:
    statement = """
        UPDATE {schema_name}.bulk_jobs SET
            state = %(state)s
        WHERE id = %(id)s
    """
    identifiers: FrozenDict[str, str] = freeze({"schema_name": db_schema})
    query = Query.dynamic_query(
        statement,
        identifiers,
    )
    args: FrozenDict[str, PrimitiveVal] = freeze(
        {
            "operation": job.job.operation,
            "created_by": job.job.created_by,
            "created_time": job.job.created_time,
            "state": job.job.state,
            "id": job.job_id.job_id,
            "module": job.job.module.value,
            "page": job.job.page,
        }
    )
    return client.execute(query, QueryValues(args))


def init_db(client: SqlClient) -> Cmd[None]:
    create_schema = f"""
        CREATE SCHEMA IF NOT EXISTS {SCHEMA};
    """
    create_table = f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}.bulk_jobs (
            operation VARCHAR,
            created_by VARCHAR,
            created_time VARCHAR,
            state VARCHAR,
            id VARCHAR,
            module VARCHAR,
            page INTEGER,
            result VARCHAR DEFAULT NULL
        );
    """
    return client.execute(
        Query.new_query(create_schema), None
    ) + client.execute(Query.new_query(create_table), None)


def new_job_client(client: SqlClient, db_schema: str = SCHEMA) -> Client:
    return Client(
        _get_bulk_jobs(client, db_schema),
        lambda j: _save_bulk_job(client, j, db_schema),
        lambda j: _update_bulk_job(client, j, db_schema),
    )
