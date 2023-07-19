import base64
from custom_exceptions import (
    InvalidFilterCursor,
)
from dynamodb.types import (
    Index,
    Item,
    PrimaryKey,
    Table,
)
from dynamodb.utils_cursor import (
    get_cursor,
    get_key_from_cursor,
)
import json
import pytest


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "index, item, expected",
    [
        (
            Index(
                name="test_index",
                primary_key=PrimaryKey(partition_key="pk2", sort_key="sk2"),
            ),
            {
                "pk": "partition_key",
                "sk": "sort_key",
                "pk2": "partition_key_2",
                "sk2": "sort_key_2",
            },
            {
                "pk": "partition_key",
                "sk": "sort_key",
                "pk2": "partition_key_2",
                "sk2": "sort_key_2",
            },
        ),
        (
            None,
            {
                "pk": "partition_key",
                "sk": "sort_key",
                "pk2": "partition_key_2",
                "sk2": "sort_key_2",
            },
            {
                "pk": "partition_key",
                "sk": "sort_key",
            },
        ),
        (
            None,
            None,
            None,
        ),
    ],
)
def test_get_cursor(
    index: Index | None, item: Item | None, expected: Item | None
) -> None:
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={},
        indexes={},
    )
    cursor: str = get_cursor(index, item, table)
    decoded_cursor = json.loads(base64.b64decode(cursor).decode())
    assert decoded_cursor == expected


@pytest.mark.skims_test_group("unittesting")
def test_get_key_from_cursor_error() -> None:
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={},
        indexes={},
    )
    index = Index(
        name="test_index",
        primary_key=PrimaryKey(
            partition_key="pk_invalid", sort_key="sk_invalid"
        ),
    )
    item = {
        "pk": "partition_key",
        "sk": "sort_key",
    }
    cursor = base64.b64encode(json.dumps(item).encode()).decode()
    with pytest.raises(InvalidFilterCursor):
        get_key_from_cursor(cursor, index, table)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.parametrize(
    "index, expected",
    [
        (
            Index(
                name="test_index",
                primary_key=PrimaryKey(partition_key="pk2", sort_key="sk2"),
            ),
            {
                "pk": "partition_key",
                "sk": "sort_key",
                "pk2": "partition_key_2",
                "sk2": "sort_key_2",
            },
        ),
        (
            None,
            {
                "pk": "partition_key",
                "sk": "sort_key",
            },
        ),
    ],
)
def test_get_key_from_cursor(index: Index | None, expected: Item) -> None:
    table = Table(
        name="test_table",
        primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
        facets={},
        indexes={},
    )
    item = {
        "pk": "partition_key",
        "sk": "sort_key",
        "pk2": "partition_key_2",
        "sk2": "sort_key_2",
    }
    cursor = base64.b64encode(json.dumps(item).encode()).decode()
    result_key = get_key_from_cursor(cursor, index, table)
    assert result_key == expected
