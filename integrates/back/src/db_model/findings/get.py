from .enums import (
    FindingStateStatus,
)
from .types import (
    Finding,
    FindingState,
    FindingVerification,
)
from .utils import (
    filter_non_state_status_findings,
    format_finding,
    format_state,
    format_verification,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections.abc import (
    Iterable,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from typing import (
    Self,
)


async def _get_finding_by_id(finding_id: str) -> Finding | None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"id": finding_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        return None

    return format_finding(response.items[0])


async def _get_findings_by_group(
    group_name: str,
) -> list[Finding]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_metadata"],),
        index=index,
        table=TABLE,
    )

    return [format_finding(item) for item in response.items]


class GroupFindingsLoader(DataLoader[str, list[Finding]]):
    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Finding]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Finding]]:
        return list(
            await collect(tuple(map(_get_findings_by_group, group_names)))
        )


class GroupFindingsNonDeletedLoader(DataLoader[str, list[Finding]]):
    def __init__(self, dataloader: GroupFindingsLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    def clear(self, key: str) -> Self:  # type: ignore
        self.dataloader.clear(key)
        return super().clear(key)

    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Finding]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Finding]]:
        findings_by_groups = await self.dataloader.load_many(group_names)
        return [
            list(
                filter_non_state_status_findings(
                    tuple(findings),
                    {
                        FindingStateStatus.DELETED,
                        FindingStateStatus.MASKED,
                    },
                )
            )
            for findings in findings_by_groups
        ]


class FindingLoader(DataLoader[str, Finding | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[Finding | None]:
        return list(
            await collect(
                tuple(_get_finding_by_id(find_id) for find_id in finding_ids)
            )
        )


async def _get_historic_verification(
    finding_id: str,
) -> list[FindingVerification]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_verification"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_verification"],),
        table=TABLE,
    )

    return list(map(format_verification, response.items))


class FindingHistoricVerificationLoader(
    DataLoader[str, list[FindingVerification]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[list[FindingVerification]]:
        return list(
            await collect(
                tuple(map(_get_historic_verification, finding_ids)),
                workers=32,
            )
        )


async def _get_historic_state(finding_id: str) -> list[FindingState]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={"id": finding_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_historic_state"],),
        table=TABLE,
    )

    return list(map(format_state, response.items))


class FindingHistoricStateLoader(DataLoader[str, list[FindingState]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: Iterable[str]
    ) -> list[list[FindingState]]:
        return list(
            await collect(tuple(map(_get_historic_state, finding_ids)))
        )
