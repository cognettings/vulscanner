from .schema import (
    GROUP_COMPLIANCE,
)
from .types import (
    GroupUnfulfilledStandard,
)
from api.resolvers.types import (
    Requirement,
)
from custom_utils.compliance import (
    get_compliance_file,
)
from custom_utils.findings import (
    get_requirements_file,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP_COMPLIANCE.field("unfulfilledStandards")
async def resolve(
    parent: GroupUnreliableIndicators,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[GroupUnfulfilledStandard]:
    compliance_file = await get_compliance_file()
    requirements_file = await get_requirements_file()

    return [
        GroupUnfulfilledStandard(
            standard_id=unfulfilled_standard.name,
            title=compliance_file[unfulfilled_standard.name]["title"],
            unfulfilled_requirements=[
                Requirement(
                    id=requirement_id,
                    summary=requirements_file[requirement_id]["en"]["summary"],
                    title=requirements_file[requirement_id]["en"]["title"],
                )
                for requirement_id in (
                    unfulfilled_standard.unfulfilled_requirements
                )
                if requirement_id in requirements_file
            ],
        )
        for unfulfilled_standard in parent.unfulfilled_standards or []
        if unfulfilled_standard.name in compliance_file
    ]
