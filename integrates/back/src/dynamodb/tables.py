from dynamodb.types import (
    Facet,
    Index,
    Item,
    PrimaryKey,
    Table,
)


def _load_facets(facets: tuple[Item, ...]) -> dict[str, Facet]:
    return {
        facet["FacetName"]: Facet(
            attrs=tuple(facet.get("NonKeyAttributes", [])),
            pk_alias=facet["KeyAttributeAlias"]["PartitionKeyAlias"],
            sk_alias=facet["KeyAttributeAlias"]["SortKeyAlias"],
        )
        for facet in facets
    }


def _get_key(key_attrs: Item) -> PrimaryKey:
    return PrimaryKey(
        partition_key=key_attrs["PartitionKey"]["AttributeName"],
        sort_key=key_attrs["SortKey"]["AttributeName"],
    )


def _load_indexes(indexes: tuple[Item, ...]) -> dict[str, Index]:
    return {
        index["IndexName"]: Index(
            name=index["IndexName"],
            primary_key=_get_key(index["KeyAttributes"]),
        )
        for index in indexes
    }


def load_tables(model: Item) -> tuple[Table, ...]:
    tables: tuple[Item, ...] = model["DataModel"]

    return tuple(
        Table(
            name=table["TableName"],
            primary_key=_get_key(table["KeyAttributes"]),
            facets=_load_facets(tuple(table["TableFacets"])),
            indexes=_load_indexes(tuple(table["GlobalSecondaryIndexes"])),
        )
        for table in tables
    )
