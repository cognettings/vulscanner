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


@STAKEHOLDER.field("lastLogin")
def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return (
        datetime_utils.get_as_str(parent.last_login_date)
        if parent.last_login_date
        else None
    )
