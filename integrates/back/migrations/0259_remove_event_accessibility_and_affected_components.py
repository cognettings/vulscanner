# pylint: disable=invalid-name
"""
Remove the event accessibility and affected attributes

Execution Time:    2022-08-11 at 20:23:23 UTC
Finalization Time: 2022-08-11 at 20:24:09 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_event(event: Event) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event.id,
            "name": event.group_name,
        },
    )
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item={"accessibility": None, "affected_components": None},
        key=primary_key,
        table=TABLE,
    )


async def get_group_events(
    loaders: Dataloaders, group_name: str
) -> list[Event]:
    return await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    orgs_domain.get_group_names(loaders, organization_id)
                    for organization_id in all_organization_ids
                ),
                workers=100,
            )
        )
    )
    all_events = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_group_events(loaders, group_name)
                    for group_name in all_group_names
                ),
                workers=100,
            )
        )
    )

    await collect(
        tuple(process_event(event) for event in all_events), workers=50
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
