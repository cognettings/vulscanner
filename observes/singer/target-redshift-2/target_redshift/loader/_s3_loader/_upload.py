from fa_purity import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from redshift_client.core.id_objs import (
    SchemaId,
)
from redshift_client.sql_client import (
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
)
from target_redshift._s3 import (
    S3URI,
)
from typing import (
    Dict,
)


def upload_to_redshift(
    db_client: SqlClient,
    schema: SchemaId,
    iam_role: str,
    data_schema: SingerSchema,
    data_file: S3URI,
) -> Cmd[None]:
    fields = (
        Unfolder(data_schema.schema.encode()["properties"])
        .to_json()
        .map(lambda d: frozenset(d))
        .unwrap()
    )
    order = tuple(sorted(fields))
    columns: Dict[str, str] = {f"column_{i}": v for i, v in enumerate(order)}
    columns_ids = ",".join(f"{{column_{i}}}" for i, _ in enumerate(order))
    stm = f"""
        COPY {{schema}}.{{table}} ({columns_ids}) FROM %(data_file)s
        iam_role %(role)s CSV NULL AS 'nan' TRUNCATECOLUMNS FILLRECORD
    """
    identifiers: Dict[str, str] = {
        "schema": schema.name.to_str(),
        "table": data_schema.stream,
    } | columns
    args: Dict[str, PrimitiveVal] = {
        "data_file": data_file.uri,
        "role": iam_role,
    }
    return db_client.execute(
        dynamic_query(stm, freeze(identifiers)),
        QueryValues(freeze(args)),
    )
