from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from batch.dal import (
    put_action,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from custom_exceptions import (
    InvalidParameter,
)
from custom_utils import (
    logs as logs_utils,
    validations as validation_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    CredentialType,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from organizations import (
    domain as orgs_domain,
)
from organizations.types import (
    CredentialAttributesToAdd,
)
from sessions import (
    domain as sessions_domain,
)


@MUTATION.field("addCredentials")
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    organization_id: str,
    credentials: dict[str, str],
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    is_pat: bool = bool(credentials.get("is_pat", False))
    if "name" not in credentials:
        raise InvalidParameter("name")
    if "type" not in credentials:
        raise InvalidParameter("type")
    if is_pat:
        orgs_domain.verify_azure_org(
            azure_organization=credentials.get("azure_organization")
        )
    if not is_pat and "azure_organization" in credentials:
        raise InvalidParameter("azure_organization")

    name: str = credentials["name"]
    validation_utils.validate_space_field(name)

    credentials_id: str = await orgs_domain.add_credentials(
        loaders,
        CredentialAttributesToAdd(
            name=name,
            key=credentials.get("key"),
            token=credentials.get("token"),
            type=CredentialType[credentials["type"]],
            user=credentials.get("user"),
            password=credentials.get("password"),
            is_pat=is_pat,
            azure_organization=credentials["azure_organization"]
            if is_pat
            else None,
        ),
        organization_id,
        user_email,
    )

    logs_utils.cloudwatch_log(
        info.context,
        "Security: Added credentials to organization"
        f" {organization_id} successfully",
    )

    if is_pat:
        await put_action(
            action=Action.UPDATE_ORGANIZATION_REPOSITORIES,
            vcpus=1,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
            additional_info=json.dumps({"credentials_id": credentials_id}),
            entity=organization_id.lower().lstrip("org#"),
            attempt_duration_seconds=7200,
            subject="integrates@fluidattacks.com",
        )

    return SimplePayload(success=True)
