from asyncio.tasks import (
    sleep,
)
from botocore.exceptions import (
    ClientError,
)
from collections import (
    defaultdict,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_AWS_S3_CONTINUOUS_REPOSITORIES,
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidAuthorization,
    InvalidGitCredentials,
    InvalidParameter,
    RootNotFound,
)
from custom_utils import (
    datetime as datetime_utils,
    validations as validation_utils,
    validations_deco as validation_deco_utils,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    roots as roots_model,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRootState,
    Root,
    RootRequest,
    Secret,
    URLRoot,
    URLRootState,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from git_self import (
    InvalidParameter as GitInvalidParameter,
    ls_remote,
)
import hashlib
from itertools import (
    groupby,
)
import json
import logging
import logging.config
from mailer import (
    groups as groups_mail,
    utils as mailer_utils,
)
from operator import (
    attrgetter,
)
from organizations import (
    utils as orgs_utils,
)
import re
from roots import (
    validations,
)
from s3 import (
    operations as s3_operations,
)
from settings.logger import (
    LOGGING,
)
from sqs.resources import (
    get_sqs_resource,
)
from typing import (
    Any,
    cast,
)
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    unquote,
    urlparse,
)
from uuid import (
    uuid4,
)

RESTRICTED_REPO_URLS = ["https://gitlab.com/fluidattacks/universe"]

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


def format_git_repo_url(raw_url: str) -> str:
    is_ssh: bool = raw_url.startswith("ssh://") or bool(
        re.match(r"^\w+@.*", raw_url)
    )
    if not is_ssh:
        raw_url = str(parse_url(raw_url)._replace(auth=None))
    url = (
        f"ssh://{raw_url}"
        if is_ssh and not raw_url.startswith("ssh://")
        else raw_url
    )
    return unquote(url).rstrip(" /")


def quote_url(raw_url: str) -> str:
    return raw_url.replace(" ", "%20")


def unquote_url(raw_url: str) -> str:
    return unquote(raw_url)


def get_oauth_type(
    credential: Credentials,
) -> str:
    if isinstance(credential.state.secret, OauthGithubSecret):
        return "GITHUB"

    if isinstance(credential.state.secret, OauthGitlabSecret):
        return "GITLAB"

    if isinstance(credential.state.secret, OauthAzureSecret):
        return "AZURE"

    if isinstance(credential.state.secret, OauthBitbucketSecret):
        return "BITBUCKET"

    return ""


def format_root_nickname(nickname: str, url: str) -> str:
    nick: str = nickname if nickname else _get_nickname_from_url(url)
    # Return the repo name as nickname
    if nick.endswith("_git"):
        return nick[:-4]
    return nick


def format_reapeted_nickname(nickname: str, url: str) -> str:
    host_name = urlparse(url).netloc
    return f"{nickname}_{host_name[:-4]}"


def is_allowed(url: str) -> bool:
    if FI_ENVIRONMENT == "development":
        return True
    return url not in RESTRICTED_REPO_URLS


async def is_in_s3(group_name: str, root_nickname: str) -> bool:
    return bool(
        await s3_operations.list_files(
            f"{group_name}/{root_nickname}.tar.gz",
            bucket=FI_AWS_S3_CONTINUOUS_REPOSITORIES,
        )
    )


@validation_deco_utils.validate_sanitized_csv_input_deco(["url"])
def format_git_url(url: str) -> str:
    return format_git_repo_url(url)


def _get_nickname_from_url(url: str) -> str:
    url_attributes = urlparse(url)
    if not url_attributes.path:
        last_path: str = urlparse(url).netloc.split(":")[-1]
    else:
        last_path = urlparse(url).path.split("/")[-1]

    return re.sub(r"(?![a-zA-Z_0-9-]).", "_", last_path[:128])


def format_root_credential_new(
    credentials: dict[str, str], organization_id: str, user_email: str
) -> Credentials:
    credential_name = credentials["name"]
    credential_type = CredentialType(credentials["type"])
    is_pat: bool = bool(credentials.get("is_pat", False))

    if not credential_name:
        raise InvalidParameter()
    if is_pat:
        if "azure_organization" not in credentials:
            raise InvalidParameter("azure_organization")
        validation_utils.validate_space_field(
            credentials["azure_organization"]
        )
    if not is_pat and "azure_organization" in credentials:
        raise InvalidParameter("azure_organization")

    secret = orgs_utils.format_credentials_secret_type(credentials)

    return Credentials(
        id=str(uuid4()),
        organization_id=organization_id,
        owner=user_email,
        state=CredentialsState(
            modified_by=user_email,
            modified_date=datetime_utils.get_utc_now(),
            name=credentials["name"],
            secret=secret,
            type=credential_type,
            is_pat=is_pat,
            azure_organization=credentials["azure_organization"]
            if is_pat
            else None,
        ),
    )


async def add_secret(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    key: str,
    value: str,
    description: str | None = None,
) -> bool:
    await loaders.root.load(RootRequest(group_name, root_id))
    secret = Secret(key=key, value=value, description=description)
    return await roots_model.add_secret(root_id, secret)


async def add_secrets_aws(group_name: str, environment_id: str) -> None:
    await add_root_environment_secret(
        group_name,
        environment_id,
        key="AWS_ACCESS_KEY_ID",
        value="",
        description="AWS access keys to make programmatic calls to AWS",
    )
    await add_root_environment_secret(
        group_name,
        environment_id,
        key="AWS_SECRET_ACCESS_KEY",
        value="",
        description="AWS secret access keys to make programmatic calls to AWS",
    )


async def add_root_environment_secret(
    group_name: str,
    url_id: str,
    key: str,
    value: str,
    description: str | None = None,
) -> bool:
    secret = Secret(
        key=key,
        value=value,
        description=description,
        created_at=datetime.now(),
    )
    return await roots_model.add_root_environment_secret(
        group_name, url_id, secret
    )


async def remove_environment_url(root_id: str, url: str) -> None:
    await roots_model.remove_environment_url(
        root_id, url_id=hashlib.sha1(url.encode()).hexdigest()  # nosec
    )


async def is_failed_cloning(loaders: Dataloaders, root_id: str) -> bool:
    """
    Returns if last historic cloning has failed two times

    OK, FAILED, FAILED
    """
    status_changes = await historic_cloning_grouped(loaders, root_id)
    has_failed: bool = False

    if len(status_changes) > 1:
        last_cloning_failed = status_changes[-1]
        last_cloning: GitRootCloning = last_cloning_failed[-1]
        has_failed = (
            last_cloning.status == GitCloningStatus.FAILED
            and len(last_cloning_failed) == 2
        )

    return has_failed


async def get_last_cloning_successful(
    loaders: Dataloaders, root_id: str
) -> GitRootCloning | None:
    """
    Returns last cloning item with "ok" state before failure

    [OK], FAILED, OK <-
    """

    status_changes = await historic_cloning_grouped(loaders, root_id)

    if len(status_changes) > 2:
        last_cloning_ok = status_changes[-3]
        last_cloning: GitRootCloning = last_cloning_ok[-1]
        if last_cloning.status == "OK":
            return last_cloning

    return None


async def send_mail_root_cloning_status(
    *,
    loaders: Dataloaders,
    group_name: str,
    root_nickname: str,
    root_id: str,
    modified_by: str,
    modified_date: datetime,
    is_failed: bool,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="root_cloning_status",
    )

    creation_date = await get_first_cloning_date(loaders, root_id)
    last_cloning_successful = await get_last_cloning_successful(
        loaders, root_id
    )

    await groups_mail.send_mail_root_cloning_status(
        loaders=loaders,
        email_to=users_email,
        group_name=group_name,
        last_successful_clone=last_cloning_successful,
        root_creation_date=creation_date,
        root_nickname=root_nickname,
        root_id=root_id,
        report_date=modified_date,
        modified_by=modified_by,
        is_failed=is_failed,
    )


async def send_mail_root_cloning_failed(
    *,
    loaders: Dataloaders,
    group_name: str,
    modified_date: datetime,
    root: Root,
    status: GitCloningStatus,
) -> None:
    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    loaders.group.clear(group_name)
    group = await loaders.group.load(group_name)
    is_failed_status_cloning: bool = await is_failed_cloning(loaders, root.id)
    is_failed: bool = (
        status == GitCloningStatus.FAILED and is_failed_status_cloning
    )
    is_cloning: bool = (
        status == GitCloningStatus.OK
        and root.cloning.status == GitCloningStatus.FAILED
    )
    if (
        group
        and not root.state.use_vpn
        and group.state.status == GroupStateStatus.ACTIVE
        and (is_cloning or is_failed)
    ):
        await send_mail_root_cloning_status(
            loaders=loaders,
            group_name=group_name,
            root_nickname=root.state.nickname,
            root_id=root.id,
            modified_by=root.state.modified_by,
            modified_date=modified_date,
            is_failed=is_failed,
        )


async def send_mail_environment(
    *,
    loaders: Dataloaders,
    modified_date: datetime,
    group_name: str,
    git_root: str,
    git_root_url: str,
    urls_added: list[str],
    urls_deleted: list[str],
    user_email: str,
    other: str | None = None,
    reason: str | None = None,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="environment_report",
    )

    await groups_mail.send_mail_environment_report(
        loaders=loaders,
        email_to=users_email,
        group_name=group_name,
        responsible=user_email,
        git_root=git_root,
        git_root_url=git_root_url,
        urls_added=urls_added,
        urls_deleted=urls_deleted,
        modified_date=modified_date,
        other=other,
        reason=reason,
    )


async def send_mail_updated_root(
    *,
    loaders: Dataloaders,
    group_name: str,
    root: Root,
    new_state: GitRootState | IPRootState | URLRootState,
    user_email: str,
) -> None:
    users_email = await mailer_utils.get_group_emails_by_notification(
        loaders=loaders,
        group_name=group_name,
        notification="updated_root",
    )

    old_state: dict[str, Any] = root.state._asdict()
    new_root_content: dict[str, Any] = {
        key: value
        for key, value in new_state._asdict().items()
        if old_state[key] != value
        and key not in ["modified_by", "modified_date", "credential_id"]
    }

    if new_root_content:
        await groups_mail.send_mail_updated_root(
            loaders=loaders,
            email_to=users_email,
            group_name=group_name,
            responsible=user_email,
            root_nickname=new_state.nickname,
            new_root_content=new_root_content,
            old_state=old_state,
            modified_date=new_state.modified_date,
        )


def get_root_ids_by_nicknames(
    group_roots: Iterable[Root], only_git_roots: bool = False
) -> dict[str, str]:
    # Get a dict that have the relation between nickname and id for roots
    # There are roots with the same nickname
    # then It is going to take the active root first
    sorted_active_roots = sorted(
        [
            root
            for root in group_roots
            if root.state.status == RootStatus.ACTIVE
        ],
        key=lambda root: root.state.modified_date,
        reverse=False,
    )
    sorted_inactive_roots = sorted(
        [
            root
            for root in group_roots
            if root.state.status == RootStatus.INACTIVE
        ],
        key=lambda root: root.state.modified_date,
        reverse=False,
    )
    root_ids: dict[str, str] = {}
    for root in sorted_inactive_roots + sorted_active_roots:
        if not only_git_roots or isinstance(root, GitRoot):
            root_ids[root.state.nickname] = root.id

    return root_ids


def get_query(root: URLRoot) -> str:
    return "" if root.state.query is None else f"?{root.state.query}"


def get_path(root: URLRoot) -> str:
    return "" if root.state.path == "/" else root.state.path


async def get_root(
    loaders: Dataloaders, root_id: str, group_name: str
) -> Root:
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if not root:
        raise RootNotFound()

    return root


async def get_first_cloning_date(
    loaders: Dataloaders, root_id: str
) -> datetime:
    historic_cloning = await loaders.root_historic_cloning.load(root_id)
    first_root: GitRootCloning = historic_cloning[0]

    return first_root.modified_date


async def historic_cloning_grouped(
    loaders: Dataloaders, root_id: str
) -> tuple[tuple[GitRootCloning, ...], ...]:
    """Returns the history of cloning failures and successes grouped"""
    loaders.root_historic_cloning.clear(root_id)
    historic_cloning = await loaders.root_historic_cloning.load(root_id)
    filtered_historic_cloning: tuple[GitRootCloning, ...] = tuple(
        filter(
            lambda cloning: cloning.status
            in [GitCloningStatus.OK, GitCloningStatus.FAILED],
            historic_cloning,
        )
    )
    grouped_historic_cloning = tuple(
        tuple(group)
        for _, group in groupby(
            filtered_historic_cloning, key=attrgetter("status")
        )
    )

    return grouped_historic_cloning


async def ls_remote_root(
    root: GitRoot, cred: Credentials | None, loaders: Dataloaders
) -> str | None:
    last_commit: str | None = None
    repo_url = root.state.url
    repo_branch = root.state.branch
    if cred is None:
        if repo_url.startswith("http"):
            last_commit = await ls_remote(
                repo_url=repo_url,
                repo_branch=repo_branch,
            )
    elif isinstance(cred.state.secret, SshSecret):
        last_commit = await ls_remote(
            repo_url=repo_url,
            credential_key=cred.state.secret.key,
            repo_branch=repo_branch,
        )
    elif isinstance(cred.state.secret, HttpsSecret):
        last_commit = await ls_remote(
            repo_url=repo_url,
            user=cred.state.secret.user,
            password=cred.state.secret.password,
            repo_branch=repo_branch,
        )
    elif isinstance(cred.state.secret, HttpsPatSecret):
        last_commit = await ls_remote(
            repo_url=repo_url,
            token=cred.state.secret.token,
            repo_branch=repo_branch,
        )
    elif isinstance(
        cred.state.secret,
        (
            OauthGithubSecret,
            OauthAzureSecret,
            OauthGitlabSecret,
            OauthBitbucketSecret,
        ),
    ):
        last_commit = await get_last_commit_oauth_provider_instance(
            root=root, cred=cred, loaders=loaders
        )
    else:
        raise InvalidParameter()

    return last_commit


async def queue_sync_root_async(group_name: str, git_root_id: str) -> None:
    with suppress(ClientError):
        await (await get_sqs_resource()).send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_clone"
            ),
            MessageBody=json.dumps(
                {
                    "id": f"{group_name}_{git_root_id}",
                    "task": "clone",
                    "args": [
                        group_name,
                        git_root_id,
                        True,
                    ],
                }
            ),
        )


@validation_deco_utils.validate_length_deco("message", max_length=400)
async def update_root_cloning_status(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    status: GitCloningStatus,
    message: str,
    commit: str | None = None,
    commit_date: datetime | None = None,
) -> None:
    root = await get_root(loaders, root_id, group_name)
    modified_date = datetime_utils.get_utc_now()

    if not isinstance(root, GitRoot):
        raise InvalidParameter()

    # As this operation can fail due to optimistic locking to avoid concurrency
    # issues (esp. the modified date being slightly different in fractions of
    # a second) a retry backup is needed
    try:
        await roots_model.update_git_root_cloning(
            current_value=root.cloning,
            cloning=GitRootCloning(
                modified_date=modified_date,
                reason=message,
                status=status,
                commit=commit,
                commit_date=commit_date,
            ),
            repo_nickname=root.state.nickname,
            group_name=group_name,
            root_id=root_id,
        )
    except ConditionalCheckFailedException:
        await sleep(1.0)
        loaders.root.clear(RootRequest(group_name, root_id))
        git_root = cast(
            GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
        )
        await roots_model.update_git_root_cloning(
            current_value=git_root.cloning,
            cloning=GitRootCloning(
                modified_date=modified_date,
                reason=message,
                status=status,
                commit=commit,
                commit_date=commit_date,
            ),
            repo_nickname=root.state.nickname,
            group_name=group_name,
            root_id=root_id,
        )

    if validations.validate_error_message(message):
        await send_mail_root_cloning_failed(
            loaders=loaders,
            group_name=group_name,
            modified_date=modified_date,
            root=root,
            status=status,
        )


async def get_unsolved_events_by_root(
    loaders: Dataloaders, group_name: str
) -> dict[str, tuple[Event, ...]]:
    unsolved_events_by_root: defaultdict[
        str | None, list[Event]
    ] = defaultdict(list[Event])
    unsolved_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name, is_solved=False)
    )
    for event in unsolved_events:
        unsolved_events_by_root[event.root_id].append(event)
    return {
        root_id: tuple(events)
        for root_id, events in unsolved_events_by_root.items()
        if root_id
    }


async def get_last_commit_oauth_provider_instance(
    *, root: GitRoot, cred: Credentials, loaders: Dataloaders
) -> str | None:
    try:
        token = await validations.get_cred_token(
            loaders=loaders,
            organization_id=cred.organization_id,
            credential_id=cred.id,
        )
    except (InvalidAuthorization, InvalidGitCredentials) as exc:
        LOGGER.error(
            "Invalid Authorization",
            extra=dict(
                exc=exc, root=root, owner=cred.owner, org=cred.organization_id
            ),
        )
        return None
    last_commit: str | None = None
    try:
        last_commit = await ls_remote(
            repo_url=root.state.url,
            token=token,
            provider=get_oauth_type(cred),
            repo_branch=root.state.branch,
        )
    except GitInvalidParameter:
        LOGGER.warning(
            "Failed oauth https ls-remote",
            extra={
                "extra": {
                    "group": root.group_name,
                    "root_id": root.id,
                    "root_nickname": root.state.nickname,
                }
            },
        )

    return last_commit


async def get_commit_last_sucessful_clone(
    loaders: Dataloaders, root: GitRoot
) -> str | None:
    commit = root.cloning.commit
    if commit is None:
        clone_history: list[
            GitRootCloning
        ] = await loaders.root_historic_cloning.load(root.id)
        for clone_state in reversed(clone_history):
            if clone_state.status == GitCloningStatus.OK:
                commit = clone_state.commit
                break

    return commit
