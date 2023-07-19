# pylint: disable=invalid-name
"""
Remove deprecated attr from organization_unreliable_indicators facet

Start Time:        2023-06-08 at 15:56:18 UTC
Finalization Time: 2023-06-08 at 15:57:40 UTC
"""
from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from db_model.organizations.types import (
    Organization,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
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


async def _get_organization_unreliable_indicators(
    organization_id: str,
) -> Item | None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={"id": organization_id},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with("ORG#")
        ),
        facets=(TABLE.facets["organization_unreliable_indicators"],),
        limit=1,
        table=TABLE,
    )
    if not response.items:
        return None

    return response.items[0]


async def update_unreliable_org_indicators(
    *,
    organization_id: str,
    organization_name: str,
    indicators: dict,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={
            "id": organization_id,
            "name": organization_name,
        },
    )

    await operations.update_item(
        item=indicators,
        key=primary_key,
        table=TABLE,
    )


async def process_organization(
    organization: Organization,
) -> None:
    indicators = await _get_organization_unreliable_indicators(organization.id)
    if not indicators:
        return
    if any(
        name in {"missed_commits", "covered_commits"}
        for name in indicators.keys()
    ):
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators={"missed_commits": None, "covered_commits": None},
        )

    LOGGER_CONSOLE.info(
        "Organization unreliable indicators processed",
        extra={
            "extra": {
                "Organization Id": organization.id,
                "Organization Name": organization.name,
            }
        },
    )


async def main() -> None:
    async for organization in orgs_domain.iterate_organizations():
        await process_organization(organization)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Start Time:        %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    LOGGER_CONSOLE.info("\n%s\n%s", execution_time, finalization_time)
