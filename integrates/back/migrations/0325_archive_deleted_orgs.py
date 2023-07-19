# pylint: disable=invalid-name,import-error
"""
Archive deleted orgs in redshift and remove all related items from vms.

Execution Time:    2022-11-18 at 18:07:03 UTC
Finalization Time: 2022-11-18 at 18:33:35 UTC
"""

from aioextensions import (
    collect,
    run,
)
from class_types.types import (
    Item,
)
from db_model import (
    credentials as credentials_model,
    organizations as orgs_model,
    portfolios as portfolios_model,
)
from db_model.organizations.get import (  # type: ignore
    get_all_organizations_items,
    get_organization_historic_state_items,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.model import (
    remove_org_finding_policies,
)
import logging
import logging.config
from operator import (
    itemgetter,
)
import psycopg2
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from redshift import (
    operations as redshift_ops,
    organizations as redshift_orgs,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(psycopg2.OperationalError,),
    sleep_seconds=1,
)
async def _process_organization(
    cursor: cursor_cls,
    metadata: Item,
    progress: float,
) -> None:
    organization_id = metadata["id"]
    organization_name = metadata["name"]
    redshift_orgs.insert_organization(
        cursor=cursor,
        item=metadata,
    )
    redshift_orgs.insert_historic_state(
        cursor=cursor,
        historic_state=await get_organization_historic_state_items(
            organization_id=organization_id
        ),
        organization_id=organization_id,
    )

    await credentials_model.remove_organization_credentials(
        organization_id=organization_id
    )
    await remove_org_finding_policies(organization_name=organization_name)
    await portfolios_model.remove_organization_portfolios(
        organization_name=organization_name
    )
    await orgs_model.remove(
        organization_id=organization_id, organization_name=organization_name
    )
    LOGGER_CONSOLE.info(
        "Organization processed",
        extra={
            "extra": {
                "id": organization_id,
                "name": organization_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    all_orgs = await get_all_organizations_items()
    deleted_orgs: list[Item] = sorted(
        [org for org in all_orgs if org["state"]["status"] == "DELETED"],
        key=itemgetter("name"),
    )
    LOGGER_CONSOLE.info(
        "Deleted orgs",
        extra={
            "extra": {
                "all_len": len(all_orgs),
                "deleted_len": len(deleted_orgs),
            }
        },
    )

    with redshift_ops.db_cursor() as cursor:
        await collect(
            tuple(
                _process_organization(
                    cursor=cursor,
                    metadata=item,
                    progress=count / len(deleted_orgs),
                )
                for count, item in enumerate(deleted_orgs)
            ),
            workers=1,
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
