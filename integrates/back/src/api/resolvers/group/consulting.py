from .schema import (
    GROUP,
)
from custom_utils.group_comments import (
    format_group_consulting_resolve,
)
from db_model.group_comments.types import (
    GroupComment,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
from dynamodb.types import (
    Item,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    domain as group_comments_domain,
)
from sessions import (
    domain as sessions_domain,
)


@GROUP.field("consulting")
@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Item]:
    user_data: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    group_comments: tuple[
        GroupComment, ...
    ] = await group_comments_domain.get_comments(
        loaders=info.context.loaders,
        group_name=parent.name,
        email=user_data["user_email"],
    )

    return [
        format_group_consulting_resolve(
            group_comment=comment, target_email=user_data["user_email"]
        )
        for comment in group_comments
    ]
