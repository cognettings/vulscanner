from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .types import (
    StakeholderState,
)
from .utils import (
    format_stakeholder,
    format_state,
)
from aiodataloader import (
    DataLoader,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    ErrorLoadingStakeholders,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)


async def get_all_stakeholders() -> list[Stakeholder]:
    primary_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={"all": "all"},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ALL_STAKEHOLDERS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingStakeholders()

    return [format_stakeholder(item) for item in response.items]


async def _get_stakeholder_items(*, emails: list[str]) -> list[Item]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["stakeholder_metadata"],
            values={"email": email},
        )
        for email in emails
    )

    return list(
        await operations.batch_get_item(keys=primary_keys, table=TABLE)
    )


async def get_historic_state(*, email: str) -> list[StakeholderState]:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_state"],
        values={
            "email": email,
        },
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["stakeholder_historic_state"],),
        table=TABLE,
    )

    return [format_state(state) for state in response.items]


async def _get_stakeholders_no_fallback(
    *, emails: Iterable[str]
) -> list[Stakeholder | None]:
    emails_formatted = [email.lower().strip() for email in emails]
    items = await _get_stakeholder_items(emails=emails_formatted)

    stakeholders: list[Stakeholder | None] = []
    for email in emails_formatted:
        stakeholder = next(
            (
                format_stakeholder(item)
                for item in items
                if (item.get("email") or str(item["pk"]).split("#")[1])
                == email
            ),
            None,
        )
        stakeholders.append(stakeholder)
    return stakeholders


class StakeholderLoader(DataLoader[str, Stakeholder | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> list[Stakeholder | None]:
        return await _get_stakeholders_no_fallback(emails=emails)
