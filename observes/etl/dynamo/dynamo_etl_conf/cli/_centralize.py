from ._core import (
    CmdContext,
    new_sql_client,
    pass_ctx,
)
import click
from dynamo_etl_conf import (
    centralize as centralize_module,
)
from fa_purity import (
    Cmd,
)
import logging
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from typing import (
    NoReturn,
)

LOG = logging.getLogger(__name__)


@click.command()  # type: ignore[misc]
@click.option("--schema", type=str, required=True)  # type: ignore[misc]
@click.option("--tables", type=str, required=True, help="dynamodb tables separated by coma")  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def dynamo_tables(
    ctx: CmdContext,
    schema: str,
    tables: str,
) -> NoReturn:
    _tables = tuple(tables.split(","))
    cmd: Cmd[None] = new_sql_client(ctx).bind(
        lambda c: centralize_module.merge_dynamo_tables(
            SchemaClient(c), frozenset(_tables), SchemaId(schema)
        )
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--schema-prefix", type=str, required=True)  # type: ignore[misc]
@click.option("--schema", type=str, required=True)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def parts(
    ctx: CmdContext,
    schema_prefix: str,
    schema: str,
) -> NoReturn:
    cmd: Cmd[None] = new_sql_client(ctx).bind(
        lambda c: centralize_module.merge_parts(
            SchemaClient(c), schema_prefix, SchemaId(schema)
        )
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--schema", type=str, required=True, help="as in `dynamo_tables` args")  # type: ignore[misc]
@click.option("--tables", type=str, required=True, help="as in `dynamo_tables` args")  # type: ignore[misc]
@click.option("--parts-schema-prefix", type=str, required=True, help="as in `parts` args i.e. `schema-prefix`")  # type: ignore[misc]
@click.option("--parts-loading-schema", type=str, required=True, help="as in `parts` args i.e. `schema`")  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def main(
    ctx: CmdContext,
    schema: str,
    tables: str,
    parts_schema_prefix: str,
    parts_loading_schema: str,
) -> NoReturn:
    _tables = tuple(tables.split(","))
    cmd: Cmd[None] = (
        new_sql_client(ctx)
        .map(lambda c: SchemaClient(c))
        .bind(
            lambda c: centralize_module.main(
                c,
                frozenset(_tables),
                parts_schema_prefix,
                SchemaId(parts_loading_schema),
                SchemaId("dynamodb_integrates_vms"),
                SchemaId(schema),
            )
        )
    )
    cmd.compute()


@click.group()  # type: ignore[misc]
def centralize() -> None:
    pass


centralize.add_command(dynamo_tables)
centralize.add_command(parts)
centralize.add_command(main)
