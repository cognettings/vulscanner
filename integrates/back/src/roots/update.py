from aioextensions import (
    collect,
    schedule,
)
import authz
from custom_exceptions import (
    GroupNotFound,
    InvalidParameter,
    PermissionDenied,
)
from custom_utils import (
    datetime as datetime_utils,
    validations_deco as validation_deco_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as creds_model,
    roots as roots_model,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    GitRootState,
    IPRoot,
    IPRootState,
    Root,
    RootEnvironmentUrlType,
    RootRequest,
    RootState,
    URLRoot,
    URLRootState,
)
from itertools import (
    groupby,
)
from operator import (
    attrgetter,
)
from organizations import (
    utils as orgs_utils,
    validations as orgs_validations,
)
from roots import (
    domain,
    utils as roots_utils,
    validations,
)
from typing import (
    Any,
    cast,
)


async def update_url_root(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not (
        isinstance(root, URLRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    domain.assign_nickname(
        new_nickname=nickname,
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )
    new_state: URLRootState = URLRootState(
        host=root.state.host,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        nickname=nickname,
        other=None,
        path=root.state.path,
        port=root.state.port,
        protocol=root.state.protocol,
        reason=None,
        status=RootStatus.ACTIVE,
    )

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    schedule(
        roots_utils.send_mail_updated_root(
            loaders=loaders,
            group_name=group_name,
            root=root,
            new_state=new_state,
            user_email=user_email,
        )
    )


async def update_git_environments(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    environment_urls: list[str],
    reason: str | None,
    other: str | None,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    modified_date = datetime_utils.get_utc_now()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    is_valid: bool = root.state.status == RootStatus.ACTIVE and all(
        validations.is_valid_url(url) for url in environment_urls
    )
    if not is_valid:
        raise InvalidParameter()

    root_urls = await loaders.root_environment_urls.load(root_id)
    urls = {
        url.url
        for url in root_urls
        if url.url_type == RootEnvironmentUrlType.URL
    }
    urls_deleted: list[str] = list(set(urls).difference(set(environment_urls)))
    urls_added: list[str] = [
        url for url in environment_urls if url not in urls
    ]

    if urls_deleted:
        if not reason:
            raise InvalidParameter(field="Reason")
        if reason == "OTHER" and not other:
            raise InvalidParameter(field="Other")

    await collect(
        [
            roots_utils.remove_environment_url(root_id, url)
            for url in urls_deleted
        ]
    )
    await collect(
        [
            domain.add_root_environment_url(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                url=url,
                url_type="URL",
                user_email=user_email,
            )
            for url in urls_added
        ]
    )

    if urls_added or urls_deleted:
        schedule(
            roots_utils.send_mail_environment(
                loaders=loaders,
                modified_date=modified_date,
                group_name=group_name,
                git_root=root.state.nickname,
                git_root_url=root.state.url,
                urls_added=urls_added,
                urls_deleted=urls_deleted,
                user_email=user_email,
                other=other,
                reason=reason,
            )
        )


async def _update_git_root_credentials(  # noqa: MC0001
    loaders: Dataloaders,
    group: Group,
    credentials: dict[str, str] | None,
    user_email: str,
) -> str | None:
    credential_id = credentials.get("id") if credentials else None
    credential_to_add: Credentials | None = None
    if credentials and credential_id is None:
        credential_to_add = roots_utils.format_root_credential_new(
            credentials, group.organization_id, user_email
        )

    if not credential_to_add and credential_id is None:
        return None

    if credential_to_add and credential_id is None:
        await orgs_validations.validate_credentials_name_in_organization(
            loaders,
            credential_to_add.organization_id,
            credential_to_add.state.name,
        )
        await creds_model.add(credential=credential_to_add)
        return credential_to_add.id

    if credential_id is not None:
        await validations.validate_credential_in_organization(
            loaders,
            credential_id,
            group.organization_id,
        )
        return credential_id
    return None


@validation_deco_utils.validate_field_exist_deco("environment")
@validation_deco_utils.validate_sanitized_csv_input_deco(["environment"])
@validation_deco_utils.validate_fields_deco(["url"])
@validations.validate_url_branch_deco(url_field="url", branch_field="branch")
async def update_git_root(  # pylint: disable=too-many-locals # noqa: MC0001
    loaders: Dataloaders,
    user_email: str,
    **kwargs: Any,
) -> Root:
    root_id: str = kwargs["id"]
    group_name = str(kwargs["group_name"]).lower()
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    root: GitRoot = cast(
        GitRoot, await roots_utils.get_root(loaders, root_id, group_name)
    )
    url: str = kwargs["url"]
    branch: str = kwargs["branch"]

    nickname = domain.assign_nickname(
        nickname=root.state.nickname,
        new_nickname=roots_utils.format_root_nickname(
            kwargs.get("nickname", ""), url
        ),
        roots=await loaders.group_roots.load(group_name),
    )

    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    domain.check_repeated_root(
        url=roots_utils.quote_url(url),
        branch=branch,
        group_name=group_name,
        root=root,
        root_vulnerabilities=await loaders.root_vulnerabilities.load(root.id),
        organization_roots=await loaders.organization_roots.load(
            organization.name
        ),
    )

    if not validations.is_nickname_unique(
        nickname=nickname,
        roots=await loaders.group_roots.load(group_name),
        url=url,
        old_nickname=root.state.nickname,
    ):
        nickname = roots_utils.format_reapeted_nickname(
            nickname=nickname, url=url
        )

    health_check_changed: bool = (
        kwargs["includes_health_check"] != root.state.includes_health_check
    )
    if health_check_changed:
        service_enforcer = authz.get_group_service_attributes_enforcer(group)
        if kwargs["includes_health_check"] and not service_enforcer(
            "has_squad"
        ):
            raise PermissionDenied()
        await domain.notify_health_check(
            group_name=group_name,
            request=kwargs["includes_health_check"],
            root=root,
            user_email=user_email,
        )

    gitignore = kwargs["gitignore"]
    enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if gitignore != root.state.gitignore and not enforcer(
        group_name, "update_git_root_filter"
    ):
        raise PermissionDenied()
    validations.validate_git_root_url(root, gitignore)

    credentials: dict[str, str] | None = kwargs.get("credentials")
    credential_id = await _update_git_root_credentials(
        loaders=loaders,
        group=group,
        credentials=credentials,
        user_email=user_email,
    )

    new_state = GitRootState(
        branch=branch,
        credential_id=credential_id,
        environment=kwargs["environment"],
        gitignore=gitignore,
        includes_health_check=kwargs["includes_health_check"],
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        nickname=nickname,
        other=None,
        reason=None,
        status=root.state.status,
        url=url,
        use_vpn=kwargs.get("use_vpn", None)
        if kwargs.get("use_vpn") is not None
        else root.state.use_vpn,
    )
    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    await roots_utils.send_mail_updated_root(
        loaders=loaders,
        group_name=group_name,
        root=root,
        new_state=new_state,
        user_email=user_email,
    )

    return GitRoot(
        created_by=root.created_by,
        created_date=root.created_date,
        cloning=root.cloning,
        group_name=root.group_name,
        id=root.id,
        organization_name=root.organization_name,
        state=new_state,
        type=root.type,
        unreliable_indicators=root.unreliable_indicators,
    )


async def update_ip_root(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    root_id: str,
    nickname: str,
) -> None:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not (
        isinstance(root, IPRoot) and root.state.status == RootStatus.ACTIVE
    ):
        raise InvalidParameter()

    if nickname == root.state.nickname:
        return

    domain.assign_nickname(
        new_nickname=nickname,
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )
    new_state: IPRootState = IPRootState(
        address=root.state.address,
        modified_by=user_email,
        modified_date=datetime_utils.get_utc_now(),
        nickname=nickname,
        other=None,
        reason=None,
        status=root.state.status,
    )

    await roots_model.update_root_state(
        current_value=root.state,
        group_name=group_name,
        root_id=root_id,
        state=new_state,
    )

    schedule(
        roots_utils.send_mail_updated_root(
            loaders=loaders,
            group_name=group_name,
            root=root,
            new_state=new_state,
            user_email=user_email,
        )
    )


async def get_last_status_update(
    loaders: Dataloaders, root_id: str
) -> RootState:
    """
    Returns the state item where the status last changed

    ACTIVE, [ACTIVE], INACTIVE, ACTIVE
    """
    historic_state = await loaders.root_historic_states.load(root_id)
    status_changes = tuple(
        tuple(group)
        for _, group in groupby(historic_state, key=attrgetter("status"))
    )
    with_current_status = status_changes[-1]

    return with_current_status[0]


async def get_last_status_update_date(
    loaders: Dataloaders, root_id: str
) -> datetime:
    """Returns the date where the status last changed"""
    last_status_update = await get_last_status_update(loaders, root_id)

    return last_status_update.modified_date
