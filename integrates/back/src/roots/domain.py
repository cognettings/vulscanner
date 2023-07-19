# pylint: disable=too-many-lines
from aioextensions import (
    collect,
    schedule,
)
import authz
from batch.types import (
    PutActionResult,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    CredentialNotFound,
    FileNotFound,
    GroupNotFound,
    HasVulns,
    InvalidField,
    InvalidParameter,
    InvalidRootExclusion,
    InvalidRootType,
    PermissionDenied,
    RepeatedRoot,
    RequiredCredentials,
    RootEnvironmentUrlNotFound,
    RootNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    filter_vulnerabilities as filter_vulns_utils,
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
    CredentialsRequest,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.groups.enums import (
    GroupSubscriptionType,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    Root,
    RootEnvironmentCloud,
    RootEnvironmentUrl,
    RootEnvironmentUrlType,
    RootRequest,
    RootUnreliableIndicators,
    URLRoot,
    URLRootState,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import hashlib
import logging
import logging.config
from notifications import (
    domain as notifications_domain,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
    validations as orgs_validations,
)
from roots import (
    filter as roots_filter,
    utils as roots_utils,
    validations,
)
from settings.logger import (
    LOGGING,
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
from uuid import (
    uuid4,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def notify_health_check(
    *, group_name: str, request: bool, root: GitRoot, user_email: str
) -> None:
    if request:
        await notifications_domain.request_health_check(
            branch=root.state.branch,
            group_name=group_name,
            repo_url=root.state.url,
            requester_email=user_email,
        )
    else:
        await notifications_domain.cancel_health_check(
            branch=root.state.branch,
            group_name=group_name,
            repo_url=root.state.url,
            requester_email=user_email,
        )


async def _get_credentials_type_to_add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    organization: Organization,
    group: Group,
    url: str,
    branch: str,
    credentials: dict[str, str] | None,
    required_credentials: bool,
    user_email: str,
    use_vpn: bool,
) -> Credentials | None:
    organization_credential: Credentials | None = None
    if required_credentials and not credentials:
        raise RequiredCredentials()

    if credentials:
        if (credential_id := credentials.get("id")) and credential_id:
            await validations.validate_credential_in_organization(
                loaders,
                credential_id,
                group.organization_id,
            )
            organization_credential = await loaders.credentials.load(
                CredentialsRequest(
                    id=credential_id,
                    organization_id=group.organization_id,
                )
            )
            if not use_vpn and required_credentials:
                await validations.working_credentials(
                    url, branch, organization_credential, loaders
                )
        else:
            organization_credential = roots_utils.format_root_credential_new(
                credentials, organization.id, user_email
            )
            await orgs_validations.validate_credentials_name_in_organization(
                loaders,
                organization_credential.organization_id,
                organization_credential.state.name,
            )
            if not use_vpn and required_credentials:
                await validations.working_credentials(
                    url, branch, organization_credential, loaders
                )
            await creds_model.add(credential=organization_credential)

    return organization_credential


@validation_deco_utils.validate_field_exist_deco("environment")
@validation_deco_utils.validate_fields_deco(["url"])
@validation_deco_utils.validate_sanitized_csv_input_deco(
    ["nickname", "environment"]
)
@validations.validate_nickname_deco("nickname")
async def add_git_root(  # pylint: disable=too-many-locals
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    required_credentials: bool = False,
    **kwargs: Any,
) -> GitRoot:
    group_name = str(kwargs["group_name"]).lower()
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    url: str = roots_utils.format_git_url(
        url=roots_utils.quote_url(kwargs["url"])
    )
    branch: str = kwargs["branch"].rstrip()
    loaders.group_roots.clear(group_name)
    nickname: str = assign_nickname(
        nickname="",
        new_nickname=roots_utils.format_root_nickname(
            kwargs.get("nickname", ""), url
        ),
        roots=await loaders.group_roots.load(group_name),
    )
    use_vpn: bool = kwargs.get("use_vpn", False)

    if not (
        validations.is_valid_url(url)
        and roots_utils.is_allowed(url)
        and validations.is_valid_git_branch(branch)
    ):
        raise InvalidParameter()
    includes_health_check = kwargs["includes_health_check"]
    service_enforcer = authz.get_group_service_attributes_enforcer(group)
    if includes_health_check and not service_enforcer("has_squad"):
        raise PermissionDenied()

    gitignore = kwargs["gitignore"]
    group_enforcer = await authz.get_group_level_enforcer(loaders, user_email)
    if gitignore and not group_enforcer(group_name, "update_git_root_filter"):
        raise PermissionDenied()
    if not validations.is_exclude_valid(gitignore, url):
        raise InvalidRootExclusion()
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    if (
        ensure_org_uniqueness
        and group.state.type != GroupSubscriptionType.ONESHOT
        and not validations.is_git_unique(
            url,
            branch,
            group_name,
            await loaders.organization_roots.load(organization.name),
            include_inactive=True,
        )
    ):
        raise RepeatedRoot()

    if not validations.is_nickname_unique(
        nickname=nickname,
        roots=await loaders.group_roots.load(group_name),
        url=url,
    ):
        nickname = roots_utils.format_reapeted_nickname(
            nickname=nickname, url=url
        )

    root_id = str(uuid4())
    credentials: dict[str, str] | None = kwargs.get("credentials")

    organization_credential = await _get_credentials_type_to_add(
        loaders=loaders,
        organization=organization,
        group=group,
        branch=branch,
        url=url,
        credentials=credentials,
        required_credentials=required_credentials,
        user_email=user_email,
        use_vpn=use_vpn,
    )
    modified_date = datetime_utils.get_utc_now()
    root = GitRoot(
        cloning=GitRootCloning(
            modified_date=modified_date,
            reason="root created",
            status=GitCloningStatus("UNKNOWN"),
        ),
        created_by=user_email,
        created_date=modified_date,
        group_name=group_name,
        id=root_id,
        organization_name=organization.name,
        state=GitRootState(
            branch=branch,
            credential_id=organization_credential.id
            if organization_credential
            else None,
            environment=kwargs["environment"],
            gitignore=gitignore,
            includes_health_check=includes_health_check,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            reason=None,
            status=RootStatus.ACTIVE,
            url=url,
            use_vpn=use_vpn,
        ),
        type=RootType.GIT,
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
    )
    await roots_model.add(root=root)

    if includes_health_check:
        await notify_health_check(
            group_name=group_name,
            request=True,
            root=root,
            user_email=user_email,
        )

    return root


async def add_ip_root(
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    address: str = kwargs["address"]
    if not validations.is_valid_ip(address):
        raise InvalidParameter()

    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    organization_name = organization.name
    if (
        ensure_org_uniqueness
        and (
            group.state.type != GroupSubscriptionType.ONESHOT
            and not validations.is_ip_unique(
                address,
                await loaders.organization_roots.load(organization_name),
                include_inactive=True,
            )
        )
        or (
            group.state.type != GroupSubscriptionType.CONTINUOUS
            and not validations.is_ip_group_unique(
                address,
                group_name,
                await loaders.organization_roots.load(organization_name),
                include_inactive=True,
            )
        )
    ):
        raise RepeatedRoot()

    loaders.group_roots.clear(group_name)
    nickname = assign_nickname(
        new_nickname=kwargs["nickname"],
        nickname="",
        roots=await loaders.group_roots.load(group_name),
    )

    modified_date = datetime_utils.get_utc_now()
    root = IPRoot(
        created_by=user_email,
        created_date=modified_date,
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
        state=IPRootState(
            address=address,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            reason=None,
            status=RootStatus.ACTIVE,
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type=RootType.IP,
    )
    await roots_model.add(root=root)

    return root.id


async def queue_sync_git_roots(  # NOSONAR
    *,
    loaders: Dataloaders,
    group_name: str,
    roots: tuple[GitRoot, ...] | None = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool | None = None,
) -> PutActionResult | None:
    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    if roots is None:
        roots = tuple(
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
        )

    valid_roots = tuple(
        root
        for root in roots
        if root.state.status == RootStatus.ACTIVE
        and (
            True
            if queue_with_vpn is None
            else root.state.use_vpn == queue_with_vpn
        )
    )
    if not valid_roots:
        LOGGER.warning(
            "The group does not have valid roots to be cloned",
            extra={"extra": {"group_name": group_name}},
        )
    try:
        valid_roots = roots_filter.filter_active_roots_with_credentials(
            valid_roots
        )
    except CredentialNotFound as exc:
        LOGGER.exception(
            exc,
            extra={"extra": {"group_name": group_name}},
        )
        raise
    if not group.state.has_squad and not force:
        valid_roots = await roots_filter.filter_roots_unsolved_events(
            valid_roots, loaders, group_name
        )

    if check_existing_jobs:
        valid_roots = await roots_filter.filter_roots_already_in_queue(
            valid_roots
        )

    valid_roots = await roots_filter.filter_roots_working_creds(
        valid_roots,
        loaders,
        group_name,
        group.organization_id,
        force,
        queue_with_vpn,
    )

    if valid_roots:
        await collect(
            [
                roots_utils.queue_sync_root_async(group_name, root.id)
                for root in valid_roots
            ]
        )
        result_clone = PutActionResult(
            success=True,
        )

        await collect(
            tuple(
                roots_utils.update_root_cloning_status(
                    loaders=loaders,
                    group_name=group_name,
                    root_id=root.id,
                    status=GitCloningStatus.QUEUED,
                    message="Cloning queued...",
                )
                for root in valid_roots
            )
        )
        LOGGER.info("Queueing %s roots for %s", len(valid_roots), group_name)

        return result_clone
    return None


@validation_deco_utils.validate_fields_deco(["url"])
@validation_deco_utils.validate_sanitized_csv_input_deco(["url", "nickname"])
@validation_deco_utils.validate_url_deco("url")
async def add_url_root(  # NOSONAR # pylint: disable=too-many-locals
    loaders: Dataloaders,
    user_email: str,
    ensure_org_uniqueness: bool = True,
    **kwargs: Any,
) -> str:
    group_name = str(kwargs["group_name"]).lower()
    loaders.group_roots.clear(group_name)
    nickname: str = assign_nickname(
        nickname="",
        new_nickname=kwargs["nickname"],
        roots=await loaders.group_roots.load(group_name),
    )
    url: str = str(kwargs["url"])

    try:
        url_attributes = parse_url(url)
    except LocationParseError as ex:
        raise InvalidParameter() from ex

    if not url_attributes.host or url_attributes.scheme not in {
        "http",
        "https",
        "file",
    }:
        raise InvalidParameter()

    host: str = url_attributes.host
    fragment: str | None = url_attributes.fragment
    path: str = url_attributes.path or "/"
    query: str | None = url_attributes.query
    default_port = "443" if url_attributes.scheme == "https" else "80"
    port = str(url_attributes.port) if url_attributes.port else default_port
    protocol: str = url_attributes.scheme.upper()

    group = await loaders.group.load(group_name)
    if not group:
        raise GroupNotFound()
    if protocol == "FILE":
        fragment = None
        query = None
        port = "0"
        if host not in {file.file_name for file in group.files or []}:
            raise FileNotFound()

    organization = await orgs_utils.get_organization(
        loaders, group.organization_id
    )
    organization_name = organization.name
    if fragment:
        path = f"{path}#{fragment}"

    if (
        ensure_org_uniqueness
        and (
            group.state.type != GroupSubscriptionType.ONESHOT
            and not validations.is_url_unique(
                host,
                path,
                port,
                protocol,
                query,
                tuple(
                    await loaders.organization_roots.load(organization_name)
                ),
                include_inactive=True,
            )
        )
        or (
            group.state.type != GroupSubscriptionType.CONTINUOUS
            and not validations.is_url_group_unique(
                group_name,
                host,
                path,
                port,
                protocol,
                query,
                tuple(
                    await loaders.organization_roots.load(organization_name)
                ),
                include_inactive=True,
            )
        )
    ):
        raise RepeatedRoot()

    modified_date = datetime_utils.get_utc_now()
    root = URLRoot(
        created_by=user_email,
        created_date=modified_date,
        group_name=group_name,
        id=str(uuid4()),
        organization_name=organization_name,
        state=URLRootState(
            host=host,
            modified_by=user_email,
            modified_date=modified_date,
            nickname=nickname,
            other=None,
            path=path,
            port=port,
            protocol=protocol,
            query=query,
            reason=None,
            status=RootStatus.ACTIVE,
        ),
        unreliable_indicators=RootUnreliableIndicators(
            unreliable_last_status_update=modified_date,
        ),
        type=RootType.URL,
    )
    await roots_model.add(root=root)

    return root.id


@validation_deco_utils.validate_sanitized_csv_input_deco(["new_nickname"])
@validations.validate_nickname_deco("new_nickname")
@validations.validate_nickname_is_unique_deco(
    nickname_field="new_nickname",
    roots_fields="roots",
    old_nickname_field="nickname",
)
def assign_nickname(  # pylint: disable=unused-argument
    nickname: str, new_nickname: str, roots: Iterable[Root]
) -> str:
    if new_nickname and new_nickname != nickname:
        return new_nickname
    return nickname


@validations.validate_git_root_deco("root")
@validations.validate_active_root_deco("root")
@validation_deco_utils.validate_sanitized_csv_input_deco(["url"])
def check_repeated_root(
    *,
    url: str,
    branch: str,
    group_name: str,
    root: GitRoot,
    root_vulnerabilities: Iterable[Vulnerability],
    organization_roots: Iterable[Root],
) -> None:
    url = roots_utils.unquote_url(url)
    root_state_url = roots_utils.unquote_url(root.state.url)
    if url != root_state_url:
        if filter_vulns_utils.filter_released_vulns(root_vulnerabilities):
            raise HasVulns()
        if not validations.is_git_unique(
            url,
            branch,
            group_name,
            organization_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()


async def activate_root(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    root: Root,
) -> None:
    new_status = RootStatus.ACTIVE

    if root.state.status != new_status:
        group = await loaders.group.load(group_name)
        if not group:
            raise GroupNotFound()
        organization = await orgs_utils.get_organization(
            loaders, group.organization_id
        )
        organization_name = organization.name
        org_roots = await loaders.organization_roots.load(organization_name)

        await validations.validate_root_and_update(
            email, group_name, new_status, org_roots, root
        )


async def deactivate_root(
    *,
    email: str,
    group_name: str,
    other: str | None,
    reason: str,
    root: Root,
) -> None:
    new_status = RootStatus.INACTIVE

    if root.state.status != new_status:
        if isinstance(root, GitRoot):
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=GitRootState(
                    branch=root.state.branch,
                    credential_id=root.state.credential_id,
                    environment=root.state.environment,
                    gitignore=root.state.gitignore,
                    includes_health_check=root.state.includes_health_check,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=other,
                    reason=reason,
                    status=new_status,
                    url=root.state.url,
                    use_vpn=root.state.use_vpn,
                ),
            )

            if root.state.includes_health_check:
                await notifications_domain.cancel_health_check(
                    branch=root.state.branch,
                    group_name=group_name,
                    repo_url=root.state.url,
                    requester_email=email,
                )

        elif isinstance(root, IPRoot):
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=IPRootState(
                    address=root.state.address,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=other,
                    reason=reason,
                    status=new_status,
                ),
            )

        else:
            await roots_model.update_root_state(
                current_value=root.state,
                group_name=group_name,
                root_id=root.id,
                state=URLRootState(
                    host=root.state.host,
                    modified_by=email,
                    modified_date=datetime_utils.get_utc_now(),
                    nickname=root.state.nickname,
                    other=other,
                    path=root.state.path,
                    port=root.state.port,
                    protocol=root.state.protocol,
                    reason=reason,
                    status=new_status,
                ),
            )


def get_root_id_by_nickname(
    nickname: str,
    group_roots: Iterable[Root],
    only_git_roots: bool = False,
) -> str:
    root_ids_by_nicknames = roots_utils.get_root_ids_by_nicknames(
        group_roots=group_roots, only_git_roots=only_git_roots
    )
    return get_root_id_by_nicknames(
        nickname=nickname, root_ids_by_nicknames=root_ids_by_nicknames
    )


def get_root_id_by_nicknames(
    nickname: str,
    root_ids_by_nicknames: dict[str, str],
) -> str:
    try:
        root_id = root_ids_by_nicknames[nickname]
    except KeyError as exc:
        LOGGER.error(
            "root no found",
            extra=dict(
                extra=dict(nickname=nickname, roots=root_ids_by_nicknames)
            ),
        )

        raise RootNotFound() from exc

    return root_id


async def get_root_id(
    loaders: Dataloaders, group_name: str, nickname: str
) -> str:
    group_roots = await loaders.group_roots.load(group_name)
    root_id = get_root_id_by_nickname(nickname, group_roots)
    return root_id


async def move_root(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    root_id: str,
    target_group_name: str,
) -> str:
    root = await roots_utils.get_root(loaders, root_id, group_name)
    source_group = await loaders.group.load(group_name)
    target_group = await loaders.group.load(target_group_name)
    if not source_group or not target_group:
        raise GroupNotFound()
    source_org_id = source_group.organization_id

    if (
        root.state.status != RootStatus.ACTIVE
        or target_group_name == root.group_name
        or target_group_name
        not in await orgs_domain.get_group_names(loaders, source_org_id)
        or source_group.state.service != target_group.state.service
    ):
        raise InvalidParameter()

    target_group_roots = await loaders.group_roots.load(target_group_name)

    if isinstance(root, GitRoot):
        if not validations.is_git_unique(
            root.state.url,
            root.state.branch,
            target_group_name,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        new_root = await add_git_root(
            loaders,
            email,
            ensure_org_uniqueness=False,
            branch=root.state.branch,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            group_name=target_group_name,
            includes_health_check=root.state.includes_health_check,
            nickname=root.state.nickname,
            url=root.state.url,
            credentials=(
                {"id": root.state.credential_id}
                if root.state.credential_id
                else None
            ),
        )
        new_root_id = new_root.id
    elif isinstance(root, IPRoot):
        if not validations.is_ip_unique(
            root.state.address,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        new_root_id = await add_ip_root(
            loaders,
            email,
            ensure_org_uniqueness=False,
            address=root.state.address,
            group_name=target_group_name,
            nickname=root.state.nickname,
        )
    else:
        if not validations.is_url_unique(
            root.state.host,
            root.state.path,
            root.state.port,
            root.state.protocol,
            root.state.query,
            target_group_roots,
            include_inactive=True,
        ):
            raise RepeatedRoot()

        query = roots_utils.get_query(root)
        path = roots_utils.get_path(root)
        new_root_id = await add_url_root(
            loaders=loaders,
            user_email=email,
            ensure_org_uniqueness=False,
            group_name=target_group_name,
            nickname=root.state.nickname,
            url=(
                f"{root.state.protocol}://{root.state.host}:{root.state.port}"
                f"{path}{query}"
            ),
        )

    await deactivate_root(
        group_name=group_name,
        other=target_group_name,
        reason="MOVED_TO_ANOTHER_GROUP",
        root=root,
        email=email,
    )

    return new_root_id


async def add_root_environment_url(
    *,
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    url: str,
    url_type: str,
    user_email: str,
    should_notified: bool = False,
    cloud_type: str | None = None,
) -> bool:
    _cloud_type: RootEnvironmentCloud | None = None
    try:
        _url_type = RootEnvironmentUrlType[url_type]
        if cloud_type:
            _cloud_type = RootEnvironmentCloud[cloud_type]
    except KeyError as exc:
        raise InvalidField("urlType") from exc

    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not isinstance(root, GitRoot):
        raise InvalidRootType()

    environment = RootEnvironmentUrl(
        id=hashlib.sha1(url.encode()).hexdigest(),  # nosec
        created_at=datetime.now(),
        created_by=user_email,
        url=url,
        url_type=_url_type,
        cloud_name=_cloud_type,
    )
    result_environment = await roots_model.add_root_environment_url(
        root_id, url=environment
    )
    if not result_environment:
        return False

    if cloud_type and cloud_type == RootEnvironmentCloud.AWS:
        await roots_utils.add_secrets_aws(group_name, environment.id)

    if should_notified:
        schedule(
            roots_utils.send_mail_environment(
                loaders=loaders,
                modified_date=datetime_utils.get_utc_now(),
                group_name=group_name,
                git_root=root.state.nickname,
                git_root_url=root.state.url,
                urls_added=[url],
                urls_deleted=[],
                user_email=user_email,
                other=None,
                reason=None,
            )
        )
    return True


async def remove_environment_url_id(
    *,
    loaders: Dataloaders,
    root_id: str,
    url_id: str,
    user_email: str,
    group_name: str,
) -> str:
    urls = await loaders.root_environment_urls.load(root_id)
    url: str | None = next(
        (env_url.url for env_url in urls if env_url.id == url_id),
        None,
    )
    if url is None:
        raise RootEnvironmentUrlNotFound()

    await roots_model.remove_environment_url(root_id, url_id=url_id)

    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not isinstance(root, GitRoot):
        raise InvalidRootType()

    schedule(
        roots_utils.send_mail_environment(
            loaders=loaders,
            modified_date=datetime_utils.get_utc_now(),
            group_name=group_name,
            git_root=root.state.nickname,
            git_root_url=root.state.url,
            urls_added=[],
            urls_deleted=[url],
            user_email=user_email,
            other=None,
            reason=None,
        )
    )

    return url


async def remove_secret(root_id: str, secret_key: str) -> None:
    await roots_model.remove_secret(root_id, secret_key)


async def remove_environment_url_secret(
    group_name: str, url_id: str, secret_key: str
) -> None:
    await roots_model.remove_environment_url_secret(
        group_name, url_id, secret_key
    )


async def remove_root(
    *,
    email: str,
    group_name: str,
    reason: str,
    root: Root,
) -> None:
    await deactivate_root(
        group_name=group_name,
        other="",
        reason=reason,
        root=root,
        email=email,
    )
    await roots_model.remove(group_name=group_name, root_id=root.id)
    LOGGER.info(
        "Root removed",
        extra={
            "extra": {
                "root_id": root.id,
                "group_name": root.group_name,
            }
        },
    )
