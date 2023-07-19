from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToePort,
)
from .utils import (
    format_toe_port_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
    RepeatedToePort,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def add(*, toe_port: ToePort, validate_state: bool = True) -> None:
    if validate_state and toe_port.state.modified_date is None:
        raise InvalidParameter("modified_date")
    if validate_state and toe_port.state.modified_by is None:
        raise InvalidParameter("modified_by")

    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_port_metadata"]
    toe_port_key = keys.build_key(
        facet=facet,
        values={
            "address": toe_port.address,
            "port": toe_port.port,
            "group_name": toe_port.group_name,
            "root_id": toe_port.root_id,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_port.state.be_present).lower(),
            "group_name": toe_port.group_name,
            "address": toe_port.address,
            "port": toe_port.port,
            "root_id": toe_port.root_id,
        },
    )
    toe_port_item = format_toe_port_item(
        toe_port_key, key_structure, gsi_2_key, gsi_2_index, toe_port
    )
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_port_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToePort() from ex

    if not isinstance(toe_port_item["state"]["modified_date"], str):
        raise InvalidParameter("modified_date")

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_state"],
        values={
            "address": toe_port.address,
            "port": toe_port.port,
            "group_name": toe_port.group_name,
            "root_id": toe_port.root_id,
            "iso8601utc": toe_port_item["state"]["modified_date"],
        },
    )
    await operations.put_item(
        facet=TABLE.facets["toe_port_historic_state"],
        item={
            **toe_port_item["state"],
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
