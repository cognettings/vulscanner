from aioextensions import (
    collect,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    GroupAuthor,
    GroupBilling,
    OrganizationActiveGroup,
    OrganizationAuthor,
    OrganizationBilling,
    Price,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET as SERVICES_DATA_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
import csv
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    retry_on_exceptions,
)
import io
from itertools import (
    chain,
)
import logging
import logging.config
from more_itertools import (
    flatten,
)
import os
from s3.resource import (
    get_s3_resource,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@retry_on_exceptions(
    exceptions=(ConnectTimeoutError,),
    sleep_seconds=float("0.2"),
)
async def _get_billing_buffer(*, date: datetime, group: str) -> io.BytesIO:
    year: str = date.strftime("%Y")
    month: str = date.strftime("%m")
    # The day is also available after 2019-09 in case it's needed

    billing_buffer = io.BytesIO()

    key: str = os.path.join("bills", year, month, f"{group}.csv")
    client = await get_s3_resource()

    try:
        await client.download_fileobj(
            SERVICES_DATA_BUCKET,
            f"{FI_AWS_S3_PATH_PREFIX}continuous-data/{key}",
            billing_buffer,
        )
    except ClientError as ex:
        # Do not send object not found to bugsnag
        if ex.response["Error"]["Code"] != "404":
            LOGGER.exception(ex, extra=dict(extra=locals()))
    else:
        billing_buffer.seek(0)

    return billing_buffer


async def get_group_authors(
    *, date: datetime, group: str
) -> tuple[GroupAuthor, ...]:
    expected_columns: dict[str, list[str]] = {
        "actor": ["actor"],
        "groups": ["groups"],
        "commit": ["commit", "sha1"],
        "repository": ["repository"],
    }
    buffer_object: io.BytesIO = await _get_billing_buffer(
        date=date, group=group
    )
    buffer_str: io.StringIO = io.StringIO(buffer_object.read().decode())

    data: list[dict[str, str]] = [
        {
            column: next(value_generator, "-")
            for column, possible_names in expected_columns.items()
            for value_generator in [
                # This attempts to get the column value by trying the
                # possible names the column may have
                # this only yields truthy values (values with data)
                filter(None, (row.get(name) for name in possible_names)),
            ]
        }
        for row in csv.DictReader(buffer_str)
    ]

    return tuple(
        GroupAuthor(
            actor=author["actor"],
            commit=author.get("commit"),
            groups=frozenset(author["groups"].replace(" ", "").split(",")),
            organization=author.get("organization"),
            repository=author.get("repository"),
        )
        for author in data
    )


async def get_group_billing(
    *, date: datetime, org: Organization, group: Group, loaders: Dataloaders
) -> GroupBilling:
    group_authors: tuple[GroupAuthor, ...] = await get_group_authors(
        date=date,
        group=group.name,
    )
    number_authors: int = len(group_authors)

    prices: dict[str, Price] = await billing_domain.get_prices()
    org_authors: dict[str, OrganizationAuthor] = {
        author.actor: author
        for author in await get_organization_authors(
            date=date,
            org=org,
            loaders=loaders,
        )
    }
    group_squad_authors: tuple[GroupAuthor, ...] = tuple(
        author
        for author in group_authors
        if GroupTier.SQUAD
        in tuple(
            group.tier for group in org_authors[author.actor].active_groups
        )
    )
    costs_authors: int = int(
        sum(
            tuple(
                prices["squad"].amount
                / len(
                    tuple(
                        group
                        for group in org_authors[
                            squad_author.actor
                        ].active_groups
                        if group.tier == GroupTier.SQUAD
                    )
                )
                for squad_author in group_squad_authors
            )
        )
        / 100
    )
    costs_base: int = (
        int(prices["machine"].amount / 100)
        if group.state.tier in (GroupTier.SQUAD, GroupTier.MACHINE)
        else 0
    )
    costs_total: int = costs_base + costs_authors

    return GroupBilling(
        authors=group_authors,
        costs_authors=costs_authors,
        costs_base=costs_base,
        costs_total=costs_total,
        number_authors=number_authors,
    )


async def get_organization_authors(
    *,
    date: datetime,
    org: Organization,
    loaders: Dataloaders,
) -> tuple[OrganizationAuthor, ...]:
    org_groups: dict[str, Group] = {
        group.name: group
        for group in await loaders.organization_groups.load(
            org.id,
        )
    }
    org_authors: tuple[GroupAuthor, ...] = tuple(
        flatten(
            await collect(
                [
                    get_group_authors(date=date, group=group)
                    for group in org_groups
                ],
                workers=10,
            )
        )
    )
    unique_authors: frozenset[str] = frozenset(
        author.actor for author in org_authors
    )
    unique_author_groups: dict[str, frozenset[str]] = {
        unique_author: frozenset(
            flatten(
                chain(
                    tuple(
                        author.groups
                        for author in org_authors
                        if author.actor == unique_author
                    )
                )
            )
        )
        for unique_author in unique_authors
    }
    return tuple(
        OrganizationAuthor(
            actor=actor,
            active_groups=tuple(
                OrganizationActiveGroup(
                    name=group, tier=org_groups[group].state.tier
                )
                for group in groups
                if group in org_groups
            ),
        )
        for actor, groups in unique_author_groups.items()
    )


async def get_organization_billing(
    *,
    date: datetime,
    org: Organization,
    loaders: Dataloaders,
) -> OrganizationBilling:
    groups_total: list[Group] = await loaders.organization_groups.load(org.id)
    groups_machine: frozenset[str] = frozenset(
        group.name
        for group in groups_total
        if group.state.tier == GroupTier.MACHINE
    )
    groups_squad: frozenset[str] = frozenset(
        group.name
        for group in groups_total
        if group.state.tier == GroupTier.SQUAD
    )

    authors_total: tuple[
        OrganizationAuthor, ...
    ] = await get_organization_authors(
        date=date,
        org=org,
        loaders=loaders,
    )
    authors_machine: frozenset[str] = frozenset(
        author.actor
        for author in authors_total
        if bool(
            frozenset(group.name for group in author.active_groups)
            & groups_machine
        )
    )
    authors_squad: frozenset[str] = frozenset(
        author.actor
        for author in authors_total
        if bool(
            frozenset(group.name for group in author.active_groups)
            & groups_squad
        )
    )

    prices: dict[str, Price] = await billing_domain.get_prices()
    costs_base: int = int(
        prices["machine"].amount
        * (len(groups_squad) + len(groups_machine))
        / 100
    )
    costs_authors: int = int(len(authors_squad) * prices["squad"].amount / 100)
    costs_total: int = costs_base + costs_authors

    return OrganizationBilling(
        authors=authors_total,
        costs_authors=costs_authors,
        costs_base=costs_base,
        costs_total=costs_total,
        number_authors_machine=len(authors_machine),
        number_authors_squad=len(authors_squad),
        number_authors_total=len(authors_total),
        number_groups_machine=len(groups_machine),
        number_groups_squad=len(groups_squad),
        number_groups_total=len(groups_total),
        organization=org.id,
    )
