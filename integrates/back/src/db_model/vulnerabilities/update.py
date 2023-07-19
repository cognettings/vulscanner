from .constants import (
    ASSIGNED_INDEX_METADATA,
    EVENT_INDEX_METADATA,
    HASH_INDEX_METADATA,
    ROOT_INDEX_METADATA,
)
from .types import (
    Vulnerability,
    VulnerabilityHistoric,
    VulnerabilityHistoricEntry,
    VulnerabilityMetadataToUpdate,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicatorsToUpdate,
    VulnerabilityVerification,
)
from .utils import (
    format_unreliable_indicators_item,
    format_unreliable_indicators_to_update_item,
    get_assigned,
    get_current_entry,
    get_new_group_index_key,
    get_new_zr_index_key_gsi_6,
    get_zr_index_key_gsi_6,
    historic_entry_type_to_str,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    EmptyHistoric,
    IndicatorAlreadyUpdated,
    VulnNotFound,
)
from db_model import (
    TABLE,
)
from db_model.utils import (
    adjust_historic_dates,
    get_as_utc_iso_format,
    serialize,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
    ValidationException,
)
import logging
import simplejson as json

# Constants
LOGGER = logging.getLogger(__name__)


async def update_metadata(
    *,
    finding_id: str,
    metadata: VulnerabilityMetadataToUpdate,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "id": vulnerability_id},
    )

    vulnerability_item = {
        key: None if not value else value
        for key, value in json.loads(
            json.dumps(metadata, default=serialize), parse_float=Decimal
        ).items()
        if value is not None
    }
    if vulnerability_item:
        try:
            if metadata.root_id:
                gsi_2_index = TABLE.indexes["gsi_2"]
                gsi_2_key = keys.build_key(
                    facet=ROOT_INDEX_METADATA,
                    values={
                        "root_id": metadata.root_id,
                        "vuln_id": vulnerability_id,
                    },
                )
                vulnerability_item[
                    gsi_2_index.primary_key.partition_key
                ] = gsi_2_key.partition_key
                vulnerability_item[
                    gsi_2_index.primary_key.sort_key
                ] = gsi_2_key.sort_key
            if metadata.hash:
                gsi_hash_index = TABLE.indexes["gsi_hash"]
                gsi_hash_key = keys.build_key(
                    facet=HASH_INDEX_METADATA,
                    values={
                        "root_id": metadata.root_id or "",
                        "hash": str(metadata.hash),
                    },
                )
                vulnerability_item[
                    gsi_hash_index.primary_key.partition_key
                ] = gsi_hash_key.partition_key
                if metadata.root_id:
                    vulnerability_item[
                        gsi_hash_index.primary_key.sort_key
                    ] = gsi_hash_key.sort_key

            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=vulnerability_item,
                key=vulnerability_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise VulnNotFound() from ex


async def update_assigned_index(
    *,
    finding_id: str,
    entry: VulnerabilityTreatment | None,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    gsi_3_index = TABLE.indexes["gsi_3"]

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        base_condition = Attr(key_structure.partition_key).exists()
        gsi_3_key = keys.build_key(
            facet=ASSIGNED_INDEX_METADATA,
            values={
                "email": get_assigned(treatment=entry),
                "vuln_id": vulnerability_id,
            },
        )
        vulnerability_item = {
            gsi_3_index.primary_key.partition_key: gsi_3_key.partition_key,
            gsi_3_index.primary_key.sort_key: gsi_3_key.sort_key,
        }
        await operations.update_item(
            condition_expression=(base_condition),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex


async def update_event_index(
    *,
    finding_id: str,
    entry: VulnerabilityVerification,
    vulnerability_id: str,
    delete_index: bool = False,
) -> None:
    key_structure = TABLE.primary_key
    gsi_4_index = TABLE.indexes["gsi_4"]

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        base_condition = (
            Attr(key_structure.partition_key).exists()
            & Attr("verification").exists()
        )
        if isinstance(entry.event_id, str):
            gsi_4_key = keys.build_key(
                facet=EVENT_INDEX_METADATA,
                values={
                    "event_id": entry.event_id,
                    "vuln_id": vulnerability_id,
                },
            )
            vulnerability_item = {
                gsi_4_index.primary_key.partition_key: gsi_4_key.partition_key,
                gsi_4_index.primary_key.sort_key: gsi_4_key.sort_key,
            }
            await operations.update_item(
                condition_expression=(base_condition),
                item=vulnerability_item,
                key=vulnerability_key,
                table=TABLE,
            )
        if delete_index:
            vulnerability_item_to_delete = {
                gsi_4_index.primary_key.partition_key: None,
                gsi_4_index.primary_key.sort_key: None,
            }
            await operations.update_item(
                condition_expression=(base_condition),
                item=vulnerability_item_to_delete,
                key=vulnerability_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex


async def update_treatment(
    *,
    current_value: Vulnerability,
    finding_id: str,
    vulnerability_id: str,
    treatment: VulnerabilityTreatment,
) -> None:
    await update_historic_entry(
        current_value=current_value,
        entry=treatment,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
    )
    await update_assigned_index(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        entry=treatment,
    )


async def update_historic_entry(  # pylint: disable=too-many-locals
    *,
    current_value: Vulnerability,
    finding_id: str,
    entry: VulnerabilityHistoricEntry,
    vulnerability_id: str,
    force_update: bool = False,
) -> None:
    key_structure = TABLE.primary_key
    group_index = TABLE.indexes["gsi_5"]
    gsi_6_index = TABLE.indexes["gsi_6"]
    entry_type = historic_entry_type_to_str(entry)
    entry_item = json.loads(json.dumps(entry, default=serialize))
    current_entry = get_current_entry(entry, current_value)
    current_zr_index_key = get_zr_index_key_gsi_6(current_value)
    new_group_index_key = get_new_group_index_key(current_value, entry)
    new_zr_index_key = get_new_zr_index_key_gsi_6(current_value, entry)

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={"finding_id": finding_id, "id": vulnerability_id},
        )
        vulnerability_item = {entry_type: entry_item}
        if new_group_index_key:
            vulnerability_item[
                group_index.primary_key.sort_key
            ] = new_group_index_key.sort_key
        if new_zr_index_key:
            vulnerability_item[
                gsi_6_index.primary_key.sort_key
            ] = new_zr_index_key.sort_key

        condition_expression = Attr(key_structure.partition_key).exists()
        if not force_update:
            condition_expression &= Attr(gsi_6_index.primary_key.sort_key).eq(
                current_zr_index_key.sort_key
            )
            condition_expression &= (
                Attr(f"{entry_type}.modified_date").eq(
                    get_as_utc_iso_format(current_entry.modified_date)
                )
                if current_entry
                else condition_expression & Attr(entry_type).not_exists()
            )
        await operations.update_item(
            condition_expression=condition_expression,
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise VulnNotFound() from ex

    historic_entry_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={
            "id": vulnerability_id,
            "iso8601utc": get_as_utc_iso_format(entry.modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_entry_key.partition_key,
        key_structure.sort_key: historic_entry_key.sort_key,
        **entry_item,
    }
    await operations.put_item(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        item=historic_item,
        table=TABLE,
    )


async def add_historic_entry(
    *,
    entry: VulnerabilityHistoricEntry,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    entry_type = historic_entry_type_to_str(entry)
    entry_item = json.loads(json.dumps(entry, default=serialize))

    historic_entry_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={
            "id": vulnerability_id,
            "iso8601utc": get_as_utc_iso_format(entry.modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_entry_key.partition_key,
        key_structure.sort_key: historic_entry_key.sort_key,
        **entry_item,
    }
    await operations.put_item(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        item=historic_item,
        table=TABLE,
    )


async def update_historic(  # pylint: disable=too-many-locals
    *,
    current_value: Vulnerability,
    historic: VulnerabilityHistoric,
) -> None:
    if not historic:
        raise EmptyHistoric()
    key_structure = TABLE.primary_key
    group_index = TABLE.indexes["gsi_5"]
    gsi_6_index = TABLE.indexes["gsi_6"]
    historic = adjust_historic_dates(historic)
    latest_entry = historic[-1]
    entry_type = historic_entry_type_to_str(latest_entry)
    current_entry = get_current_entry(latest_entry, current_value)
    new_group_index_key = get_new_group_index_key(current_value, latest_entry)
    new_zr_index_key = get_new_zr_index_key_gsi_6(current_value, latest_entry)

    try:
        vulnerability_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={
                "finding_id": current_value.finding_id,
                "id": current_value.id,
            },
        )
        vulnerability_item = {
            entry_type: json.loads(json.dumps(latest_entry, default=serialize))
        }
        if new_group_index_key:
            vulnerability_item[
                group_index.primary_key.sort_key
            ] = new_group_index_key.sort_key
        if new_zr_index_key:
            vulnerability_item[
                gsi_6_index.primary_key.sort_key
            ] = new_zr_index_key.sort_key

        base_condition = Attr(key_structure.partition_key).exists()
        await operations.update_item(
            condition_expression=(
                base_condition
                & Attr(f"{entry_type}.modified_date").eq(
                    get_as_utc_iso_format(current_entry.modified_date)
                )
                if current_entry
                else base_condition & Attr(entry_type).not_exists()
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise VulnNotFound() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={"id": current_value.id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets[f"vulnerability_historic_{entry_type}"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": current_value.id,
                "iso8601utc": item["sk"].split("#")[1],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": current_value.id,
                "iso8601utc": get_as_utc_iso_format(entry.modified_date),
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry, default=serialize)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_put_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def update_unreliable_indicators(
    *,
    current_value: Vulnerability,
    indicators: VulnerabilityUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": current_value.finding_id,
            "id": current_value.id,
        },
    )

    unreliable_indicators_item = {
        f"unreliable_indicators.{key}": value
        for key, value in format_unreliable_indicators_to_update_item(
            indicators
        ).items()
    }
    current_indicators_item = {
        f"unreliable_indicators.{key}": value
        for key, value in format_unreliable_indicators_item(
            current_value.unreliable_indicators
        ).items()
    }

    conditions = (
        Attr(indicator_name).eq(current_indicators_item[indicator_name])
        for indicator_name in unreliable_indicators_item
        if indicator_name in current_indicators_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=unreliable_indicators_item,
            key=vulnerability_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise IndicatorAlreadyUpdated() from ex
    except ValidationException:
        await operations.update_item(
            condition_expression=condition_expression,
            item={"unreliable_indicators": {}},
            key=vulnerability_key,
            table=TABLE,
        )
        try:
            await operations.update_item(
                condition_expression=condition_expression,
                item=unreliable_indicators_item,
                key=vulnerability_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise IndicatorAlreadyUpdated() from ex
