from .schema import (
    QUERY,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    GroupFile,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Any,
)

Resource = dict[str, str | None]
Resources = dict[str, str | list[Resource] | None]


def _format_group_files(group_files: list[GroupFile]) -> list[Resource]:
    return [
        {
            "description": file.description,
            "file_name": file.file_name,
            "uploader": file.modified_by,
            "upload_date": datetime_utils.get_as_str(file.modified_date)
            if file.modified_date
            else None,
        }
        for file in group_files
    ]


@QUERY.field("resources")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> Resources:
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    group = await groups_domain.get_group(loaders, group_name.lower())

    return {
        "files": _format_group_files(group.files) if group.files else None,
        "group_name": group_name,
    }
