from .schema import (
    STAKEHOLDER,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@STAKEHOLDER.field("firstLogin")
def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return (
        datetime_utils.get_as_str(parent.registration_date)
        if parent.registration_date
        else None
    )
