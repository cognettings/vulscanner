from boto3.dynamodb.conditions import (
    ConditionBase,
)
from botocore.exceptions import (
    ClientError,
)
from decimal import (
    Decimal,
)
from dynamodb.operations import (
    _build_facet_item,
    _build_key_arg_item,
    _build_query_args,
    _exclude_none,
    _format_map_attrs,
    _format_update_args,
    _parse_floats,
    batch_delete_item,
    batch_put_item,
    delete_item,
    PatchedBatchWriter,
    put_item,
    query,
    scan,
    update_item,
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
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_patched_batch_writer_flush(mocker: MockerFixture) -> None:
    # pylint: disable=protected-access
    mock_client = mocker.AsyncMock()
    mock_client.batch_write_item.return_value = {
        "UnprocessedItems": {"mock_table": []}
    }
    batch_writer = PatchedBatchWriter(
        client=mock_client, table_name="mock_table", flush_amount=2
    )
    batch_writer._items_buffer = [
        {"item1": "value1"},
        {"item2": "value2"},
        {"item3": "value3"},
    ]
    await batch_writer._flush()
    assert batch_writer._items_buffer == [{"item3": "value3"}]
    assert mock_client.batch_write_item.call_args.kwargs == (
        {
            "RequestItems": {
                "mock_table": [
                    {"item1": "value1"},
                    {"item2": "value2"},
                ]
            }
        }
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "key, expected",
    [
        (
            PrimaryKey(partition_key="partition_key", sort_key="sort_key"),
            {"pk": "partition_key", "sk": "sort_key"},
        ),
        (
            SimpleKey(partition_key="partition_key"),
            {"pk": "partition_key"},
        ),
    ],
)
def test_build_key_arg_item(
    key: PrimaryKey | SimpleKey, expected: Item
) -> None:
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={},
        indexes={},
    )
    result_item: Item = _build_key_arg_item(key=key, table=table)
    assert result_item == expected


@pytest.mark.skims_test_group("unittesting")
def test_build_facet_item() -> None:
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={
            "facet1": Facet(
                attrs=("attr1", "attr2"),
                pk_alias="pk_alias",
                sk_alias="sk_alias",
            ),
        },
        indexes={},
    )
    item = Item(
        {
            "pk": "partition_key",
            "sk": "sort_key",
            "attr1": "value1",
            "attr2": "value2",
            "attr3": "value3",
        }
    )
    facet = table.facets["facet1"]
    facet_item: Item = _build_facet_item(facet=facet, item=item, table=table)
    assert facet_item == {
        "pk": "partition_key",
        "sk": "sort_key",
        "attr1": "value1",
        "attr2": "value2",
    }


@pytest.mark.skims_test_group("unittesting")
def test_exclude_none() -> None:
    args = {
        "key1": "value1",
        "key2": None,
        "key3": {
            "subkey1": "subvalue1",
            "subkey2": None,
        },
        "key4": {
            "subkey3": None,
            "subkey4": "subvalue4",
        },
    }
    result = _exclude_none(args=args)
    assert result == {
        "key1": "value1",
        "key3": {
            "subkey1": "subvalue1",
        },
        "key4": {
            "subkey4": "subvalue4",
        },
    }


@pytest.mark.skims_test_group("unittesting")
def test_parse_floats() -> None:
    args = {
        "key1": 10,
        "key2": 3.14,
        "key3": "value",
        "key4": {"subkey1": 2.718, "subkey2": "subvalue"},
        "key5": {"subkey3": 1.618, "subkey4": "list_value"},
    }
    result = _parse_floats(args=args)
    assert isinstance(result, dict)
    assert result == {
        "key1": 10,
        "key2": Decimal("3.14"),
        "key3": "value",
        "key4": {"subkey1": Decimal("2.718"), "subkey2": "subvalue"},
        "key5": {"subkey3": Decimal("1.618"), "subkey4": "list_value"},
    }


@pytest.mark.skims_test_group("unittesting")
def test_build_query_args(mocker: MockerFixture) -> None:
    condition_expression = ConditionBase()
    facets = (
        Facet(
            attrs=("attr1", "attr2"),
            pk_alias="pk_alias",
            sk_alias="sk_alias",
        ),
    )
    filter_expression = ConditionBase()
    index = Index(
        name="index_name",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
    )
    limit = 10
    start_key = {
        "pk": "start_partition_key",
        "sk": "start_sort_key",
    }
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={
            "facet1": Facet(
                attrs=("attr1", "attr2"),
                pk_alias="pk_alias",
                sk_alias="sk_alias",
            ),
        },
        indexes={},
    )
    mock_exclude_none = mocker.patch(
        "dynamodb.operations._exclude_none", side_effect=lambda args: args
    )
    result: Item = _build_query_args(  # NOSONAR
        condition_expression=condition_expression,
        facets=facets,
        filter_expression=filter_expression,
        index=index,
        limit=limit,
        start_key=start_key,
        table=table,
    )
    result["ProjectionExpression"] = ",".join(
        sorted(result["ProjectionExpression"].split(","))
    )
    assert mock_exclude_none.call_count == 1
    assert result == {
        "ExpressionAttributeNames": {
            "#pk": "pk",
            "#sk": "sk",
            "#attr1": "attr1",
            "#attr2": "attr2",
        },
        "FilterExpression": filter_expression,
        "IndexName": "index_name",
        "KeyConditionExpression": condition_expression,
        "ProjectionExpression": "#attr1,#attr2,#pk,#sk",
        "Limit": 10,
        "ExclusiveStartKey": start_key,
    }


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "attr, expected",
    [
        ("attr1.attr2.attr3", "#attr1.#attr2.#attr3"),
        ("test", "#test"),
        ("attr1.attr2", "#attr1.#attr2"),
    ],
)
def test_format_map_attrs(attr: str, expected: str) -> None:
    formatted_attr: str = _format_map_attrs(attr)
    assert formatted_attr == expected


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_scan(mocker: MockerFixture) -> None:
    table = mocker.MagicMock()
    mock_table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource",
        return_value=mock_table_resource,
    )
    mock_table_resource.scan.side_effect = [
        {"Items": [{"id": 1, "name": "Item1"}], "LastEvaluatedKey": {"id": 1}},
        {"Items": [{"id": 2, "name": "Item2"}], "LastEvaluatedKey": None},
    ]
    response: list[Item] = await scan(table=table)
    assert mock_get_table_resource.await_count == 1
    assert mock_table_resource.scan.await_count == 2
    assert response == [
        {"id": 1, "name": "Item1"},
        {"id": 2, "name": "Item2"},
    ]


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_scan_error(mocker: MockerFixture) -> None:
    table = mocker.MagicMock()
    mock_table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource",
        return_value=mock_table_resource,
    )
    mock_table_resource.scan.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch(
        "dynamodb.operations.handle_error",
    )
    await scan(table=table)
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert mock_get_table_resource.await_count == 1
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_put_item(mocker: MockerFixture) -> None:
    items = (
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"},
    )
    len_items = len(items)
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource",
    )
    mock_get_table_resource.return_value.name = "table_name"
    mock_get_table_resource.return_value.meta.client = "meta_client"
    mock_patched_writer = mocker.patch(
        "dynamodb.operations.PatchedBatchWriter",
    )
    mock_exclude_none = mocker.patch("dynamodb.operations._exclude_none")
    mock_parse_floats = mocker.patch("dynamodb.operations._parse_floats")
    table = mocker.MagicMock()
    mock_put_item = (
        mock_patched_writer.return_value.__aenter__.return_value.put_item
    )
    await batch_put_item(items=items, table=table)
    call_args_patched_writer = mock_patched_writer.call_args
    assert call_args_patched_writer.args == ("table_name", "meta_client")
    assert call_args_patched_writer.kwargs == {
        "flush_amount": 25,
        "overwrite_by_pkeys": None,
        "on_exit_loop_sleep": 0,
    }
    assert mock_get_table_resource.call_count == 1
    assert mock_parse_floats.call_count == len_items
    assert mock_exclude_none.call_count == len_items
    assert mock_put_item.call_count == len_items


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_put_item_error(mocker: MockerFixture) -> None:
    items = ({"id": 1, "name": "Item 1"},)
    mocker.patch(
        "dynamodb.operations.get_table_resource",
    )
    mock_patched_writer = mocker.patch(
        "dynamodb.operations.PatchedBatchWriter",
    )
    mocker.patch("dynamodb.operations._exclude_none")
    mocker.patch("dynamodb.operations._parse_floats")
    table = mocker.MagicMock()
    mock_put_item = (
        mock_patched_writer.return_value.__aenter__.return_value.put_item
    )
    mock_put_item.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await batch_put_item(items=items, table=table)
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert mock_handle_error.call_count == 1
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_delete_item(mocker: MockerFixture) -> None:
    key = PrimaryKey(partition_key="pk", sort_key="sk")
    table = mocker.MagicMock()
    table.primary_key.partition_key = "partition_key_attr"
    table.primary_key.sort_key = "sort_key_attr"
    table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mock_exclude_none = mocker.patch(
        "dynamodb.operations._exclude_none",
        return_value={
            "Key": {
                "partition_key_attr": "pk",
                "sort_key_attr": "sk",
            }
        },
    )
    await delete_item(condition_expression=None, key=key, table=table)
    assert mock_get_table_resource.await_count == 1
    assert mock_exclude_none.call_count == 1
    assert (
        table_resource.delete_item.call_args.kwargs
        == mock_exclude_none.return_value
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_delete_item_error(mocker: MockerFixture) -> None:
    key = PrimaryKey(partition_key="pk", sort_key="sk")
    table = mocker.MagicMock()
    table.primary_key.partition_key = "partition_key_attr"
    table.primary_key.sort_key = "sort_key_attr"
    table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    table_resource.delete_item.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mocker.patch("dynamodb.operations._exclude_none")
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await delete_item(condition_expression=None, key=key, table=table)
    assert mock_get_table_resource.await_count == 1
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert mock_handle_error.call_count == 1
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_put_item(mocker: MockerFixture) -> None:
    magick_mock = mocker.MagicMock()
    item: Item = {}
    table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mock_build_facet_item = mocker.patch(
        "dynamodb.operations._build_facet_item",
        return_value={
            "pk": "partition_key",
            "sk": "sort_key",
        },
    )
    mock_parse_floats = mocker.patch(
        "dynamodb.operations._parse_floats", side_effect=lambda args: args
    )
    mock_exclude_none = mocker.patch(
        "dynamodb.operations._exclude_none", side_effect=lambda args: args
    )
    await put_item(
        condition_expression=magick_mock,
        facet=magick_mock,
        item=item,
        table=magick_mock,
    )
    assert mock_get_table_resource.await_count == 1
    assert mock_build_facet_item.call_count == 1
    assert mock_parse_floats.call_count == 1
    assert mock_exclude_none.call_count == 1
    assert table_resource.put_item.call_args.kwargs == {
        "ConditionExpression": magick_mock,
        "Item": mock_build_facet_item.return_value,
    }


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_put_item_error(mocker: MockerFixture) -> None:
    magick_mock = mocker.MagicMock()
    item: Item = {}
    table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mocker.patch("dynamodb.operations._build_facet_item")
    mocker.patch("dynamodb.operations._parse_floats")
    mocker.patch("dynamodb.operations._exclude_none")
    table_resource.put_item.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await put_item(
        condition_expression=magick_mock,
        facet=magick_mock,
        item=item,
        table=magick_mock,
    )
    assert mock_get_table_resource.await_count == 1
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_delete_item(mocker: MockerFixture) -> None:
    keys = (
        mocker.MagicMock(partition_key="pk1", sort_key="sk1"),
        mocker.MagicMock(partition_key="pk2", sort_key="sk2"),
    )
    table = mocker.MagicMock()
    table_resource = mocker.Mock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mock_build_key = mocker.patch(
        "dynamodb.operations._build_key_arg_item", return_value="build_return"
    )
    mock_batch_writer = mocker.AsyncMock()
    mock_batch_writer.__aenter__.return_value = mock_batch_writer
    table_resource.batch_writer.return_value = mock_batch_writer
    await batch_delete_item(keys=keys, table=table)
    mock_delete_item = mock_batch_writer.__aenter__.return_value.delete_item
    assert mock_get_table_resource.await_count == 1
    assert table_resource.batch_writer.call_count == 1
    assert mock_build_key.call_count == 2
    assert mock_delete_item.call_count == 2
    expected_calls = [
        ({"Key": "build_return"},),
        ({"Key": "build_return"},),
    ]
    assert mock_delete_item.call_args_list == expected_calls


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_delete_item_error(mocker: MockerFixture) -> None:
    keys = (mocker.MagicMock(partition_key="pk1", sort_key="sk1"),)
    table = mocker.MagicMock()
    table_resource = mocker.Mock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mocker.patch("dynamodb.operations._build_key_arg_item")
    mock_batch_writer = mocker.AsyncMock()
    mock_batch_writer.__aenter__.return_value = mock_batch_writer
    table_resource.batch_writer.return_value = mock_batch_writer
    mock_delete_item = mock_batch_writer.__aenter__.return_value.delete_item
    mock_delete_item.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await batch_delete_item(keys=keys, table=table)
    assert mock_get_table_resource.await_count == 1
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "after, paginate, last_key",
    [
        (None, False, None),
        ("test_key", True, {"pk": "pk_value"}),
    ],
)
async def test_query(
    mocker: MockerFixture,
    after: str | None,
    paginate: bool,
    last_key: dict | None,
) -> None:
    magic_mock = mocker.MagicMock()
    facets = (
        mocker.MagicMock(attrs=["attr1", "attr2"]),
        mocker.MagicMock(attrs=["attr3", "attr4"]),
    )
    table_resource = mocker.AsyncMock()
    mock_get_table_resource = mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    items = [
        {"attr1": "value1", "attr2": "value2"},
        {"attr1": "value3", "attr2": "value4"},
    ]
    response = {"Items": items, "LastEvaluatedKey": last_key}
    table_resource.query.return_value = response
    mock_get_cursor = mocker.patch(
        "dynamodb.operations.get_cursor", return_value="cursor"
    )
    mock_build_query_args = mocker.patch(
        "dynamodb.operations._build_query_args", return_value=response
    )
    mock_get_key_from_cursor = mocker.patch(
        "dynamodb.operations.get_key_from_cursor", return_value="cursor"
    )
    result = await query(
        after=after,
        condition_expression=magic_mock,
        facets=facets,
        filter_expression=magic_mock,
        index=magic_mock,
        limit=10,
        paginate=paginate,
        table=magic_mock,
    )
    expected_query_response = QueryResponse(
        items=tuple(items),
        page_info=PageInfo(
            has_next_page=bool(last_key),
            end_cursor=mock_get_cursor.return_value,
        ),
    )
    if after:
        assert mock_get_key_from_cursor.call_count == 1
    assert mock_get_table_resource.await_count == 1
    assert mock_build_query_args.call_count == 1
    assert table_resource.query.call_count == 1
    assert mock_get_cursor.call_count == 1
    assert table_resource.query.call_args.kwargs == response
    assert result == expected_query_response


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_query_error(mocker: MockerFixture) -> None:
    magic_mock = mocker.MagicMock()
    facets = (mocker.MagicMock(attrs=["attr1", "attr2"]),)
    table_resource = mocker.AsyncMock()
    mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    items = [{"attr1": "value1", "attr2": "value2"}]
    response = {"Items": items, "LastEvaluatedKey": None}
    mocker.patch(
        "dynamodb.operations._build_query_args", return_value=response
    )
    table_resource.query.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await query(
        condition_expression=magic_mock,
        facets=facets,
        filter_expression=magic_mock,
        index=magic_mock,
        limit=10,
        paginate=False,
        table=magic_mock,
    )
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_update_item_error(mocker: MockerFixture) -> None:
    magic_mock = mocker.MagicMock()
    table_resource = mocker.AsyncMock()
    mocker.patch(
        "dynamodb.operations.get_table_resource", return_value=table_resource
    )
    mocker.patch("dynamodb.operations._format_update_args")
    mocker.patch("dynamodb.operations._exclude_none", return_value={})
    table_resource.update_item.side_effect = ClientError(
        {"Error": {"Code": "UnknownCode"}},
        operation_name="test_operation",
    )
    mock_handle_error = mocker.patch("dynamodb.operations.handle_error")
    await update_item(
        condition_expression=magic_mock,
        item=magic_mock,
        key=magic_mock,
        table=magic_mock,
    )
    error_called = mock_handle_error.call_args.kwargs["error"]
    assert isinstance(error_called, ClientError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_update_item(mocker: MockerFixture) -> None:
    condition_expression = mocker.MagicMock()
    item = mocker.MagicMock()
    key = mocker.MagicMock()
    table = mocker.MagicMock()
    table.primary_key = PrimaryKey("test", "test")
    mock_table_resource = mocker.AsyncMock()
    mock_get_table = mocker.patch(
        "dynamodb.operations.get_table_resource",
        return_value=mock_table_resource,
    )
    mock_format_update_args = mocker.patch(
        "dynamodb.operations._format_update_args",
        return_value={"key": "value"},
    )
    mock__exclude_none = mocker.patch(
        "dynamodb.operations._exclude_none",
        return_value=mock_format_update_args.return_value,
    )
    await update_item(
        condition_expression=condition_expression,
        item=item,
        key=key,
        table=table,
    )
    assert mock_format_update_args.call_args.kwargs == {
        "condition_expression": condition_expression,
        "item": item,
        "key": key,
        "key_structure": table.primary_key,
    }
    assert mock_get_table.await_count == 1
    assert mock_table_resource.update_item.await_count == 1
    assert (
        mock_table_resource.update_item.call_args.kwargs
        == mock__exclude_none.return_value
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "item, formatted_map, attrs_upd, attrs_rm, attr_values",
    [
        (
            {"attr1": "value1", "attr2.attr3": "value2", "attr4": None},
            ["#attr1", "#attr2.#attr3", "#attr4"],
            "SET #attr1 = :attr1,#attr2.#attr3 = :attr2attr3",
            "REMOVE #attr4",
            {":attr1": "value1", ":attr2attr3": "value2"},
        ),
        (
            {"attr1.attr2": "value1", "attr3.attr4": "value2"},
            ["#attr1.#attr2", "#attr3.#attr4"],
            "SET #attr1.#attr2 = :attr1attr2,#attr3.#attr4 = :attr3attr4",
            "",
            {":attr1attr2": "value1", ":attr3attr4": "value2"},
        ),
        (
            {"attr1.attr2.attr3.attr4": None},
            ["#attr1.#attr2.#attr3.#attr4"],
            "",
            "REMOVE #attr1.#attr2.#attr3.#attr4",
            {},
        ),
    ],
)
def test_format_update_args(  # pylint: disable=too-many-arguments
    mocker: MockerFixture,
    item: Item,
    formatted_map: list[str],
    attrs_upd: str,
    attrs_rm: str,
    attr_values: dict[str, str],
) -> None:
    condition_expression = "condition_expression"
    key = PrimaryKey(
        partition_key="partition_key_value", sort_key="sort_key_value"
    )
    key_structure = PrimaryKey(partition_key="pk_attr", sort_key="sk_attr")
    mock_format_map_attrs = mocker.patch(
        "dynamodb.operations._format_map_attrs", side_effect=formatted_map
    )
    args = _format_update_args(
        condition_expression=condition_expression,
        item=item,
        key=key,
        key_structure=key_structure,
    )
    expected_args = {
        "ConditionExpression": "condition_expression",
        "ExpressionAttributeNames": {
            "#attr1": "attr1",
            "#attr2": "attr2",
            "#attr3": "attr3",
            "#attr4": "attr4",
        },
        "Key": {
            "pk_attr": "partition_key_value",
            "sk_attr": "sort_key_value",
        },
        "UpdateExpression": " ".join(
            (
                attrs_upd,
                attrs_rm,
            )
        ),
    }
    if attr_values:
        expected_args["ExpressionAttributeValues"] = attr_values
    assert mock_format_map_attrs.call_count == len(item)
    assert args == expected_args
