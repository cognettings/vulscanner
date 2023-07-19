from .utils_cursor import (
    get_cursor,
    get_key_from_cursor,
)
from aioboto3.dynamodb.table import (
    BatchWriter,
)
import aioextensions
from boto3.dynamodb.conditions import (
    ConditionBase,
)
from botocore.exceptions import (
    ClientError,
)
from decimal import (
    Decimal,
)
from dynamodb.exceptions import (
    handle_error,
)
from dynamodb.resource import (
    get_table_resource,
)
from dynamodb.types import (
    Facet,
    Index,
    Item,
    PageInfo,
    PrimaryKey,
    QueryResponse,
    SimpleKey,
    Table,
)
from itertools import (
    chain,
)
from more_itertools import (
    chunked,
)

# Fix for https://github.com/boto/boto3/pull/2867


class PatchedBatchWriter(BatchWriter):
    async def _flush(self) -> None:
        items_to_send = self._items_buffer[
            : self._flush_amount
        ]  # type: list[Item]
        self._items_buffer = self._items_buffer[
            self._flush_amount :
        ]  # type: list[Item]
        response = await self._client.batch_write_item(
            RequestItems={self._table_name: items_to_send}
        )
        unprocessed_items = response["UnprocessedItems"].get(
            self._table_name, []
        )

        if unprocessed_items:
            self._items_buffer.extend(unprocessed_items)


def _build_key_arg_item(*, key: PrimaryKey | SimpleKey, table: Table) -> Item:
    key_formatted = {
        table.primary_key.partition_key: key.partition_key,
    }
    if isinstance(key, PrimaryKey):
        key_formatted[table.primary_key.sort_key] = key.sort_key

    return key_formatted


def _build_facet_item(*, facet: Facet, item: Item, table: Table) -> Item:
    key_structure = table.primary_key
    attrs = (key_structure.partition_key, key_structure.sort_key, *facet.attrs)
    return {attr: item[attr] for attr in attrs if item.get(attr) is not None}


def _build_query_args(
    *,
    condition_expression: ConditionBase,
    facets: tuple[Facet, ...],
    filter_expression: ConditionBase | None,
    index: Index | None,
    limit: int | None,
    start_key: dict[str, str] | None,
    table: Table,
) -> Item:
    facet_attrs = tuple({attr for facet in facets for attr in facet.attrs})
    attrs = {
        table.primary_key.partition_key,
        table.primary_key.sort_key,
        *facet_attrs,
    }
    if index:
        attrs.add(index.primary_key.partition_key)
        attrs.add(index.primary_key.sort_key)
    args = {
        "ExpressionAttributeNames": {f"#{attr}": attr for attr in attrs},
        "FilterExpression": filter_expression,
        "IndexName": index.name if index else None,
        "KeyConditionExpression": condition_expression,
        "ProjectionExpression": ",".join([f"#{attr}" for attr in attrs]),
    }
    if limit:
        args["Limit"] = limit
    if start_key:
        args["ExclusiveStartKey"] = start_key
    return _exclude_none(args=args)


def _parse_floats(*, args: Item) -> Item:
    """
    Converts floats into Decimal.
    Needed as floats are currently unsupported by DynamoDB
    """
    return {
        key: _parse_floats(args=value)
        if isinstance(value, dict)
        else Decimal(str(value))
        if isinstance(value, float)
        else value
        for key, value in args.items()
    }


def _exclude_none(*, args: Item) -> Item:
    return {
        key: _exclude_none(args=value) if isinstance(value, dict) else value
        for key, value in args.items()
        if value is not None
    }


async def batch_put_item(*, items: tuple[Item, ...], table: Table) -> None:
    table_resource = await get_table_resource(table)

    async with PatchedBatchWriter(
        table_resource.name,
        table_resource.meta.client,
        flush_amount=25,
        overwrite_by_pkeys=None,
        on_exit_loop_sleep=0,
    ) as batch_writer:
        try:
            await aioextensions.collect(
                tuple(
                    batch_writer.put_item(
                        Item=_exclude_none(args=_parse_floats(args=item))
                    )
                    for item in items
                )
            )
        except ClientError as error:
            handle_error(error=error)


async def batch_delete_item(
    *, keys: tuple[PrimaryKey | SimpleKey, ...], table: Table
) -> None:
    table_resource = await get_table_resource(table)

    async def _delete_chunk(chunk_keys: list[PrimaryKey | SimpleKey]) -> None:
        async with table_resource.batch_writer() as batch_writer:
            await aioextensions.collect(
                tuple(
                    batch_writer.delete_item(
                        Key=_build_key_arg_item(key=primary_key, table=table)
                    )
                    for primary_key in chunk_keys
                )
            )

    try:
        for keys_chunk in chunked(keys, 100):
            await _delete_chunk(keys_chunk)
    except ClientError as error:
        handle_error(error=error)


async def delete_item(
    *,
    condition_expression: ConditionBase | None = None,
    key: PrimaryKey,
    table: Table,
) -> None:
    key_structure = table.primary_key
    table_resource = await get_table_resource(table)
    args = {
        "ConditionExpression": condition_expression,
        "Key": {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
        },
    }

    try:
        await table_resource.delete_item(**_exclude_none(args=args))
    except ClientError as error:
        handle_error(error=error)


async def put_item(
    *,
    condition_expression: ConditionBase | None = None,
    facet: Facet,
    item: Item,
    table: Table,
) -> None:
    table_resource = await get_table_resource(table)
    facet_item = _build_facet_item(facet=facet, item=item, table=table)
    args = {
        "ConditionExpression": condition_expression,
        "Item": _parse_floats(args=facet_item),
    }

    try:
        await table_resource.put_item(**_exclude_none(args=args))
    except ClientError as error:
        handle_error(error=error)


async def query(  # pylint: disable=too-many-locals
    *,
    after: str | None = None,
    condition_expression: ConditionBase,
    facets: tuple[Facet, ...],
    filter_expression: ConditionBase | None = None,
    index: Index | None = None,
    limit: int | None = None,
    paginate: bool = False,
    table: Table,
) -> QueryResponse:
    table_resource = await get_table_resource(table)
    start_key = None
    if after:
        start_key = get_key_from_cursor(after, index, table)

    query_args = _build_query_args(
        condition_expression=condition_expression,
        facets=facets,
        filter_expression=filter_expression,
        index=index,
        limit=limit,
        start_key=start_key,
        table=table,
    )
    items: list[Item] = []
    cursor: str = ""
    has_next_page: bool = False
    try:
        response = await table_resource.query(**query_args)
        items = response.get("Items", [])
        if paginate:
            cursor = get_cursor(
                index, items[-1] if items else start_key, table
            )
            has_next_page = bool(response.get("LastEvaluatedKey"))
        else:
            while last_key := response.get("LastEvaluatedKey"):
                response = await table_resource.query(
                    **query_args,
                    ExclusiveStartKey=last_key,
                )
                items += response.get("Items", [])
            cursor = get_cursor(index, None, table)
            has_next_page = False
    except ClientError as error:
        handle_error(error=error)

    return QueryResponse(
        items=tuple(items),
        page_info=PageInfo(has_next_page=has_next_page, end_cursor=cursor),
    )


def _format_map_attrs(attr: str) -> str:
    return ".".join([f"#{map_attr}" for map_attr in attr.split(".")])


def _format_update_args(
    *,
    condition_expression: ConditionBase | None = None,
    item: Item,
    key: PrimaryKey,
    key_structure: PrimaryKey,
) -> Item:
    list_to_remove = []
    list_to_update = []
    attr_values = {}
    list_item_attrs = []
    for attr, value in item.items():
        list_item_attrs.append(attr.split("."))
        if value is None:
            list_to_remove.append(f"{_format_map_attrs(attr)}")
        else:
            list_to_update.append(
                f"{_format_map_attrs(attr)} = :{attr.replace('.', '')}"
            )
            attr_values[f":{attr.replace('.', '')}"] = value
    item_attrs = chain(*list_item_attrs)
    attrs_to_remove = ",".join(list_to_remove)
    attrs_to_update = ",".join(list_to_update)
    attr_names = {f"#{attr}": attr for attr in item_attrs}
    base_args: Item = {
        "ConditionExpression": condition_expression,
        "ExpressionAttributeNames": attr_names,
        "Key": {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
        },
        "UpdateExpression": " ".join(
            (
                f"SET {attrs_to_update}" if attrs_to_update else "",
                f"REMOVE {attrs_to_remove}" if attrs_to_remove else "",
            )
        ),
    }
    if attrs_to_update:
        base_args["ExpressionAttributeValues"] = attr_values
    return base_args


async def update_item(
    *,
    condition_expression: ConditionBase | None = None,
    item: Item,
    key: PrimaryKey,
    table: Table,
) -> None:
    args = _format_update_args(
        condition_expression=condition_expression,
        item=item,
        key=key,
        key_structure=table.primary_key,
    )
    table_resource = await get_table_resource(table)
    try:
        await table_resource.update_item(**_exclude_none(args=args))
    except ClientError as error:
        handle_error(error=error)


async def scan(*, table: Table) -> list[Item]:
    try:
        response_items: list[Item] = []
        scan_attrs: Item = {}
        table_resource = await get_table_resource(table)
        response = await table_resource.scan(**scan_attrs)
        response_items = response.get("Items", [])
        while last_key := response.get("LastEvaluatedKey"):
            scan_attrs.update({"ExclusiveStartKey": last_key})
            response = await table_resource.scan(**scan_attrs)
            response_items += response.get("Items", [])
    except ClientError as error:
        handle_error(error=error)

    return response_items
