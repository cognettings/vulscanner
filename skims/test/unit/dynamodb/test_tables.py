from dynamodb.tables import (
    _get_key,
    _load_facets,
    _load_indexes,
    load_tables,
)
from dynamodb.types import (
    Facet,
    Index,
    Item,
    PrimaryKey,
    Table,
)
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.skims_test_group("unittesting")
def test_get_key() -> None:
    key_attrs: Item = {
        "PartitionKey": {"AttributeName": "pk"},
        "SortKey": {"AttributeName": "sk"},
    }
    result: PrimaryKey = _get_key(key_attrs)
    assert result.partition_key == "pk"
    assert result.sort_key == "sk"


@pytest.mark.skims_test_group("unittesting")
def test_load_facets() -> None:
    facets: tuple[Item, Item] = (
        Item(
            {
                "FacetName": "facet1",
                "KeyAttributeAlias": {
                    "PartitionKeyAlias": "pk_alias1",
                    "SortKeyAlias": "sk_alias1",
                },
                "NonKeyAttributes": ["attr1", "attr2"],
            }
        ),
        Item(
            {
                "FacetName": "facet2",
                "KeyAttributeAlias": {
                    "PartitionKeyAlias": "pk_alias2",
                    "SortKeyAlias": "sk_alias2",
                },
            }
        ),
    )
    result: dict[str, Facet] = _load_facets(facets)
    facet_1 = result["facet1"]
    facet_2 = result["facet2"]
    assert len(result) == len(facets)
    assert facet_1.attrs == ("attr1", "attr2")
    assert facet_1.pk_alias == "pk_alias1"
    assert facet_1.sk_alias == "sk_alias1"
    assert facet_2.attrs == ()
    assert facet_2.pk_alias == "pk_alias2"
    assert facet_2.sk_alias == "sk_alias2"


@pytest.mark.skims_test_group("unittesting")
def test_load_indexes(mocker: MockerFixture) -> None:
    indexes = (
        Item(
            {
                "IndexName": "index1",
                "KeyAttributes": {
                    "PartitionKey": {"AttributeName": "pk_attr1"},
                    "SortKey": {"AttributeName": "sk_attr1"},
                },
            }
        ),
        Item(
            {
                "IndexName": "index2",
                "KeyAttributes": {
                    "PartitionKey": {"AttributeName": "pk_attr2"},
                    "SortKey": {"AttributeName": "sk_attr2"},
                },
            }
        ),
    )
    mock_get_key = mocker.patch(
        "dynamodb.tables._get_key", return_value="mock_get_key"
    )
    result: dict[str, Index] = _load_indexes(indexes)
    index_1 = result["index1"]
    index_2 = result["index2"]
    assert len(result) == 2
    assert index_1.name == "index1"
    assert index_1.primary_key == mock_get_key.return_value
    assert index_2.name == "index2"
    assert index_2.primary_key == mock_get_key.return_value


@pytest.mark.skims_test_group("unittesting")
def test_load_tables(mocker: MockerFixture) -> None:
    model = {
        "DataModel": [
            {
                "TableName": "table1",
                "KeyAttributes": {
                    "PartitionKey": {"AttributeName": "pk_attr1"},
                    "SortKey": {"AttributeName": "sk_attr1"},
                },
                "TableFacets": [
                    {
                        "FacetName": "facet1",
                        "NonKeyAttributes": ["attr1", "attr2"],
                        "KeyAttributeAlias": {
                            "PartitionKeyAlias": "pk_alias1",
                            "SortKeyAlias": "sk_alias1",
                        },
                    }
                ],
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "index1",
                        "KeyAttributes": {
                            "PartitionKey": {"AttributeName": "pk_attr2"},
                            "SortKey": {"AttributeName": "sk_attr2"},
                        },
                    }
                ],
            },
        ]
    }
    str_db_tables = "dynamodb.tables"
    mock_get_key = mocker.patch(
        f"{str_db_tables}._get_key", return_value="mock_get_key"
    )
    mock_load_facets = mocker.patch(
        f"{str_db_tables}._load_facets", return_value="mock_load_facets"
    )
    mock_load_indexes = mocker.patch(
        f"{str_db_tables}._load_indexes", return_value="mock_load_indexes"
    )
    result: tuple[Table, ...] = load_tables(model)
    table_1 = result[0]
    assert table_1.name == "table1"
    assert table_1.primary_key == mock_get_key.return_value
    assert table_1.facets == mock_load_facets.return_value
    assert table_1.indexes == mock_load_indexes.return_value
