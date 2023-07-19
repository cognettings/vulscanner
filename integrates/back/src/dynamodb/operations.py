from .utils import (
    get_cursor,
    get_key_from_cursor,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    ConditionBase,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    ReadTimeoutError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from decimal import (
    Decimal,
)
from dynamodb.exceptions import (
    handle_error,
)
from dynamodb.resource import (
    get_resource,
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
import logging
from more_itertools import (
    chunked,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


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
    forward: bool,
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
        "ScanIndexForward": forward,
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


async def batch_delete_item(
    *, keys: tuple[PrimaryKey | SimpleKey, ...], table: Table
) -> None:
    table_resource = await get_table_resource(table)

    async def _delete_chunk(chunk_keys: list[PrimaryKey | SimpleKey]) -> None:
        async with table_resource.batch_writer() as batch_writer:
            await collect(
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
        handle_error(error=error, keys=keys)


async def batch_get_item(
    *, keys: tuple[PrimaryKey | SimpleKey, ...], table: Table
) -> tuple[Item, ...]:
    items: list[Item] = []
    resource = await get_resource()

    async def _get_chunk(
        chunk_keys: list[PrimaryKey | SimpleKey],
    ) -> tuple[Item, ...]:
        response = await resource.batch_get_item(
            RequestItems={
                table.name: {
                    "Keys": [
                        _build_key_arg_item(key=primary_key, table=table)
                        for primary_key in chunk_keys
                    ]
                }
            },
        )
        return response["Responses"][table.name]

    try:
        items = [
            item
            for items_chunk in await collect(
                tuple(
                    _get_chunk(keys_chunk) for keys_chunk in chunked(keys, 100)
                ),
                workers=900,
            )
            for item in items_chunk
        ]
    except ClientError as error:
        handle_error(error=error, keys=list(chunked(keys, 100)))

    return tuple(items)


async def batch_put_item(*, items: tuple[Item, ...], table: Table) -> None:
    table_resource = await get_table_resource(table)

    async with table_resource.batch_writer() as batch_writer:
        try:
            await collect(
                tuple(
                    batch_writer.put_item(
                        Item=_exclude_none(args=_parse_floats(args=item))
                    )
                    for item in items
                )
            )
        except ClientError as error:
            handle_error(error=error)


async def delete_item(
    *,
    condition_expression: ConditionBase | None = None,
    key: PrimaryKey | SimpleKey,
    table: Table,
) -> None:
    table_resource = await get_table_resource(table)
    args = {
        "ConditionExpression": condition_expression,
        "Key": _build_key_arg_item(key=key, table=table),
    }

    try:
        await table_resource.delete_item(**_exclude_none(args=args))
    except ClientError as error:
        handle_error(error=error)


def _build_get_item_args(
    *, facets: tuple[Facet, ...], key: PrimaryKey | SimpleKey, table: Table
) -> Item:
    facet_attrs = tuple({attr for facet in facets for attr in facet.attrs})
    attrs = {
        table.primary_key.partition_key,
        table.primary_key.sort_key,
        *facet_attrs,
    }

    return {
        "ExpressionAttributeNames": {f"#{attr}": attr for attr in attrs},
        "Key": _build_key_arg_item(key=key, table=table),
        "ProjectionExpression": ",".join([f"#{attr}" for attr in attrs]),
    }


async def get_item(
    *, facets: tuple[Facet, ...], key: PrimaryKey | SimpleKey, table: Table
) -> Item | None:
    item: Item | None = None
    table_resource = await get_table_resource(table)
    get_item_args = _build_get_item_args(key=key, facets=facets, table=table)

    try:
        response = await table_resource.get_item(**get_item_args)
        item = response.get("Item")
    except ClientError as error:
        handle_error(error=error)

    return item


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
    forward: bool = True,
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
        forward=forward,
        index=index,
        limit=limit,
        start_key=start_key,
        table=table,
    )

    try:
        response = await table_resource.query(**query_args)
        items: list[Item] = response.get("Items", [])
        if paginate:
            cursor = get_cursor(
                index, items[-1] if items else start_key, table
            )
            has_next_page = bool(response.get("LastEvaluatedKey"))
        else:
            while response.get("LastEvaluatedKey"):
                response = await table_resource.query(
                    **query_args,
                    ExclusiveStartKey=response.get("LastEvaluatedKey"),
                )
                items += response.get("Items", [])
            cursor = get_cursor(index, None, table)
            has_next_page = False
    except ClientError as error:
        handle_error(
            error=error,
            query_args=query_args,
            message="Client Error while querying",
        )
    except (ReadTimeoutError, ConnectTimeoutError) as error:
        LOGGER.exception(error, extra={"extra": {"query_args": query_args}})
        raise UnavailabilityError() from error

    return QueryResponse(
        items=tuple(items),
        page_info=PageInfo(has_next_page=has_next_page, end_cursor=cursor),
    )


def _format_map_attrs(attr: str) -> str:
    return ".".join([f"#{map_attr}" for map_attr in attr.split(".")])


async def update_item(
    *,
    condition_expression: ConditionBase | None = None,
    item: Item,
    key: PrimaryKey | SimpleKey,
    table: Table,
) -> None:
    item_attrs = chain(
        *[attr.split(".") if "." in attr else [attr] for attr in item]
    )
    attr_names = {f"#{attr}": attr for attr in item_attrs}
    attr_values = {
        f":{attr.replace('.', '')}": value
        for attr, value in item.items()
        if value is not None
    }
    attrs_to_update = ",".join(
        f"{_format_map_attrs(attr)} = :{attr.replace('.', '')}"
        if "." in attr
        else f"#{attr} = :{attr}"
        for attr, value in item.items()
        if value is not None
    )
    attrs_to_remove = ",".join(
        f"{_format_map_attrs(attr)}"
        for attr, value in item.items()
        if value is None
    )
    table_resource = await get_table_resource(table)
    base_args: Item = {
        "ConditionExpression": condition_expression,
        "ExpressionAttributeNames": attr_names,
        "Key": _build_key_arg_item(key=key, table=table),
        "UpdateExpression": " ".join(
            (
                f"SET {attrs_to_update}" if attrs_to_update else "",
                f"REMOVE {attrs_to_remove}" if attrs_to_remove else "",
            )
        ),
    }
    args = (
        {**base_args, "ExpressionAttributeValues": attr_values}
        if attrs_to_update
        else base_args
    )

    try:
        await table_resource.update_item(**_exclude_none(args=args))
    except ClientError as error:
        handle_error(error=error, item=item)
    except ReadTimeoutError as exc:
        LOGGER.exception(
            "item could not be updated",
            extra=dict(exc=exc, item=item),
        )
        raise UnavailabilityError() from exc


async def scan(*, table: Table) -> list[Item]:
    try:
        scan_attrs: Item = {}
        table_resource = await get_table_resource(table)
        response = await table_resource.scan(**scan_attrs)
        response_items = response.get("Items", [])
        while response.get("LastEvaluatedKey"):
            scan_attrs.update(
                {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
            )
            response = await table_resource.scan(**scan_attrs)
            response_items += response.get("Items", [])
    except ClientError as error:
        handle_error(error=error)

    return response_items
