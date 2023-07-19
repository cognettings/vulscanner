from .payloads.types import (
    UpdateToeInputPayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
)
from custom_exceptions import (
    ToeInputNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    logs as logs_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputRequest,
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
from sessions import (
    domain as sessions_domain,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)
from typing import (
    Any,
)


@MUTATION.field("updateToeInput")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(  # pylint: disable=too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    be_present: bool,
    component: str,
    entry_point: str,
    group_name: str,
    root_id: str,
    **kwargs: Any,
) -> UpdateToeInputPayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        loaders: Dataloaders = info.context.loaders
        current_value: ToeInput | None = await loaders.toe_input.load(
            ToeInputRequest(
                component=component,
                entry_point=entry_point,
                group_name=group_name,
                root_id=root_id,
            )
        )
        if current_value:
            be_present_to_update = (
                None
                if be_present is current_value.state.be_present
                else be_present
            )
            attacked_at_to_update = (
                datetime_utils.get_utc_now()
                if kwargs.get("has_recent_attack") is True
                else None
            )
            attacked_by_to_update = (
                None if attacked_at_to_update is None else user_email
            )
            await toe_inputs_domain.update(
                current_value=current_value,
                attributes=ToeInputAttributesToUpdate(
                    attacked_at=attacked_at_to_update,
                    attacked_by=attacked_by_to_update,
                    be_present=be_present_to_update,
                ),
                modified_by=user_email,
            )
        else:
            raise ToeInputNotFound()

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated toe input in group {group_name} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update toe input in group {group_name}",
        )
        raise

    return UpdateToeInputPayload(
        component=component,
        entry_point=entry_point,
        group_name=group_name,
        root_id=root_id,
        success=True,
    )
