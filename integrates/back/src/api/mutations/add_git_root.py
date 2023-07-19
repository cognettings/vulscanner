from .payloads.types import (
    AddRootPayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    schedule,
)
from batch.dal import (
    generate_key_to_dynamod,
    get_action,
    put_action,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    UnableToSendMail,
)
from custom_utils import (
    logs as logs_utils,
)
from custom_utils.stakeholders import (
    get_full_name,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.enums import (
    CredentialType,
)
from db_model.integration_repositories.remove import (
    remove,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
    retry_on_exceptions,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
import hashlib
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from mailer.trial import (
    new_enrolled_user_mail,
)
import re
from roots import (
    domain as roots_domain,
)
from roots.utils import (
    format_git_repo_url,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)
from urllib3.exceptions import (
    LocationParseError,
)
from urllib3.util.url import (
    parse_url,
)


@MUTATION.field("addGitRoot")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> AddRootPayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    full_name: str = get_full_name(user_info)
    loaders: Dataloaders = info.context.loaders
    root: GitRoot = await roots_domain.add_git_root(
        loaders, user_email, required_credentials=True, **kwargs
    )
    group_name = root.group_name
    group = await groups_domain.get_group(loaders, group_name)
    send_new_enrolled_user_mail = retry_on_exceptions(
        exceptions=(UnableToSendMail, ApiClientError),
        max_attempts=4,
        sleep_seconds=2,
    )(new_enrolled_user_mail)
    if kwargs.get("credentials") and (
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            roots=(root,),
            group_name=root.group_name,
            queue_with_vpn=kwargs.get("use_vpn", False),
        )
    ):
        key = generate_key_to_dynamod(
            action_name=Action.UPDATE_ORGANIZATION_OVERVIEW.value,
            additional_info="*",
            entity=group.organization_id,
            subject="integrates@fluidattacks.com",
        )
        overview_action = await get_action(action_dynamo_pk=key)
        if not overview_action:
            loaders.organization_credentials.clear_all()
            credentials: list[
                Credentials
            ] = await loaders.organization_credentials.load(
                group.organization_id
            )
            if any(
                cred
                for cred in credentials
                if cred.state.type is CredentialType.OAUTH or cred.state.is_pat
            ):
                await put_action(
                    action=Action.UPDATE_ORGANIZATION_OVERVIEW,
                    vcpus=1,
                    product_name=Product.INTEGRATES,
                    queue=IntegratesBatchQueue.SMALL,
                    additional_info="*",
                    entity=group.organization_id.lower().lstrip("org#"),
                    attempt_duration_seconds=7200,
                    subject="integrates@fluidattacks.com",
                )

    with suppress(LocationParseError):
        await remove(
            repository=OrganizationIntegrationRepository(
                id=hashlib.sha256(
                    (
                        kwargs["url"]
                        if kwargs["url"].startswith("ssh://")
                        or bool(re.match(r"^\w+@.*", kwargs["url"]))
                        else parse_url(kwargs["url"])._replace(auth=None).url
                    ).encode("utf-8")
                ).hexdigest(),
                organization_id=group.organization_id,
                branch=(
                    "refs/heads/"
                    f'{kwargs["branch"].rstrip().lstrip("refs/heads/")}'
                ),
                last_commit_date=None,
                url=format_git_repo_url(kwargs["url"]),
            )
        )

    schedule(
        groups_mail.send_mail_added_root(
            loaders=loaders,
            branch=root.state.branch,
            environment=root.state.environment,
            group_name=group_name,
            health_check=root.state.includes_health_check,
            root_nickname=root.state.nickname,
            root_url=root.state.url,
            responsible=user_email,
            modified_date=root.state.modified_date,
            vpn_required=root.state.use_vpn,
        )
    )
    schedule(
        send_new_enrolled_user_mail(
            loaders=loaders,
            user_email=user_email,
            full_name=full_name,
            organization_id=group.organization_id,
            group_name=group_name,
        )
    )

    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added a root in {kwargs["group_name"].lower()}',
    )

    return AddRootPayload(root_id=root.id, success=True)
