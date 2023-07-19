from .schema import (
    STAKEHOLDER,
)
from aioextensions import (
    collect,
)
from custom_utils import (
    groups as groups_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)


@STAKEHOLDER.field("groups")
async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Group]:
    loaders: Dataloaders = info.context.loaders
    email = parent.email
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_stakeholder(loaders, email),
            groups_domain.get_groups_by_stakeholder(
                loaders, email, active=False
            ),
        ]
    )
    stakeholder_group_names: list[str] = active + inactive
    groups = await collect(
        [
            groups_domain.get_group(loaders, stakeholder_group_name)
            for stakeholder_group_name in stakeholder_group_names
        ]
    )

    return groups_utils.filter_active_groups(groups)
