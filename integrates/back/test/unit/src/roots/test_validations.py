from custom_exceptions import (
    InactiveRoot,
    InvalidChar,
    InvalidGitCredentials,
    InvalidGitRoot,
    InvalidParameter,
    InvalidRootComponent,
    InvalidRootType,
    InvalidUrl,
    RepeatedRootNickname,
    RequiredCredentials,
)
from custom_utils.datetime import (
    get_now_minus_delta,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    SshSecret,
)
from db_model.enums import (
    GitCloningStatus,
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
    RootUnreliableIndicators,
    URLRoot,
    URLRootState,
)
from organizations.utils import (
    get_organization,
)
import pytest
from roots import (
    utils as roots_utils,
)
from roots.validations import (
    is_exclude_valid,
    is_git_unique,
    is_valid_git_branch,
    is_valid_ip,
    is_valid_url,
    validate_active_root,
    validate_active_root_deco,
    validate_component,
    validate_credential_in_organization,
    validate_git_access,
    validate_git_credentials_oauth,
    validate_git_root,
    validate_git_root_deco,
    validate_nickname,
    validate_nickname_deco,
    validate_nickname_is_unique_deco,
    validate_root_type_deco,
    validate_url_branch_deco,
    working_credentials,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["active_root", "inactive_root"],
    [
        [
            URLRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
                group_name="oneshottest",
                id="8493c82f-2860-4902-86fa-75b0fef76034",
                organization_name="okada",
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:45:55+00:00"
                    ),
                    nickname="url_root_1",
                    other=None,
                    path="/",
                    port="443",
                    protocol="HTTPS",
                    reason=None,
                    status=RootStatus.ACTIVE,
                    query=None,
                ),
                type=RootType.URL,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
            IPRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-12-19T13:44:37+00:00"
                ),
                group_name="asgard",
                id="814addf0-316c-4415-850d-21bd3783b011",
                organization_name="okada",
                state=IPRootState(
                    address="127.0.0.1",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-12-19T13:44:37+00:00"
                    ),
                    nickname="ip_root_2",
                    other=None,
                    reason=None,
                    status=RootStatus.INACTIVE,
                ),
                type=RootType.IP,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
        ],
    ],
)
async def test_validate_active_root(
    active_root: Root,
    inactive_root: Root,
) -> None:
    validate_active_root(active_root)
    with pytest.raises(InactiveRoot):
        validate_active_root(inactive_root)


@pytest.mark.parametrize(
    ["active_root", "inactive_root"],
    [
        [
            URLRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
                group_name="oneshottest",
                id="8493c82f-2860-4902-86fa-75b0fef76034",
                organization_name="okada",
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:45:55+00:00"
                    ),
                    nickname="url_root_1",
                    other=None,
                    path="/",
                    port="443",
                    protocol="HTTPS",
                    reason=None,
                    status=RootStatus.ACTIVE,
                    query=None,
                ),
                type=RootType.URL,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
            IPRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-12-19T13:44:37+00:00"
                ),
                group_name="asgard",
                id="814addf0-316c-4415-850d-21bd3783b011",
                organization_name="okada",
                state=IPRootState(
                    address="127.0.0.1",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-12-19T13:44:37+00:00"
                    ),
                    nickname="ip_root_2",
                    other=None,
                    reason=None,
                    status=RootStatus.INACTIVE,
                ),
                type=RootType.IP,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
        ],
    ],
)
async def test_validate_active_root_deco(
    active_root: Root,
    inactive_root: Root,
) -> None:
    @validate_active_root_deco("root")
    def decorated_func(root: Root) -> Root:
        return root

    assert decorated_func(root=active_root)

    with pytest.raises(InactiveRoot):
        decorated_func(root=inactive_root)


async def test_validate_component() -> None:
    loaders = get_new_context()
    git_root = await roots_utils.get_root(
        loaders, "4039d098-ffc5-4984-8ed3-eb17bca98e19", "unittesting"
    )
    await validate_component(
        loaders=loaders,
        root=git_root,
        component="https://app.fluidattacks.com/test",
    )
    url_root = await roots_utils.get_root(
        loaders, "8493c82f-2860-4902-86fa-75b0fef76034", "oneshottest"
    )
    await validate_component(
        loaders=loaders,
        root=url_root,
        component="https://app.fluidattacks.com:443/test",
    )
    ip_root = await roots_utils.get_root(
        loaders, "d312f0b9-da49-4d2b-a881-bed438875e99", "oneshottest"
    )
    await validate_component(
        loaders=loaders, root=ip_root, component="127.0.0.1:8080/test"
    )
    with pytest.raises(InvalidRootComponent):
        await validate_component(
            loaders=loaders,
            root=git_root,
            component="https://app.invalid.com/test",
        )
    with pytest.raises(InvalidRootComponent):
        await validate_component(
            loaders=loaders,
            root=url_root,
            component="https://app.fluidattacks.com:440",
        )
    with pytest.raises(InvalidUrl):
        await validate_component(
            loaders=loaders,
            root=git_root,
            component="://app.invalid.com:66000/test",
        )
    with pytest.raises(InvalidUrl):
        await validate_component(
            loaders=loaders,
            root=url_root,
            component="://app.invalid.com:66000/test",
        )


def test_is_valid_url() -> None:
    assert is_valid_url("https://fluidattacks.com/")
    assert is_valid_url("ssh://git@ssh.dev.azure.com:v3/company/project/")
    assert not is_valid_url("randomstring")


def test_is_valid_git_branch() -> None:
    assert is_valid_git_branch("master")
    assert not is_valid_git_branch("( ͡° ͜ʖ ͡°)")


def test_is_valid_ip() -> None:
    # FP: local testing
    assert is_valid_ip("8.8.8.8")  # NOSONAR
    assert not is_valid_ip("randomstring")


def test_is_exclude_valid() -> None:
    repo_url: str = "https://fluidattacks.com/universe"
    repo_git: str = "git@gitlab.com:fluidattacks/universe.git"
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/universe/test.py"], repo_url
    )
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/universe/test.py"], repo_git
    )
    assert not is_exclude_valid(["Universe/test.py"], repo_url)
    assert not is_exclude_valid(["universe/**/test.py"], repo_url)


@pytest.mark.parametrize(
    ["git_root", "ip_root"],
    [
        [
            GitRoot(
                cloning=GitRootCloning(
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:39:10+00:00"
                    ),
                    reason="root OK",
                    status=GitCloningStatus.OK,
                    commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
                    commit_date=datetime.fromisoformat(
                        "2022-02-15T18:45:06.493253+00:00"
                    ),
                ),
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-11-19T13:37:10+00:00"
                ),
                group_name="unittesting",
                id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                organization_name="okada",
                state=GitRootState(
                    branch="master",
                    environment="production",
                    includes_health_check=True,
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    nickname="universe",
                    status=RootStatus.ACTIVE,
                    url="https://gitlab.com/fluidattacks/universe",
                    credential_id=None,
                    gitignore=["bower_components/*", "node_modules/*"],
                    other=None,
                    reason=None,
                    use_vpn=False,
                ),
                type=RootType.GIT,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                ),
            ),
            IPRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-12-19T13:44:37+00:00"
                ),
                group_name="asgard",
                id="814addf0-316c-4415-850d-21bd3783b011",
                organization_name="okada",
                state=IPRootState(
                    address="127.0.0.1",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-12-19T13:44:37+00:00"
                    ),
                    nickname="ip_root_2",
                    other=None,
                    reason=None,
                    status=RootStatus.INACTIVE,
                ),
                type=RootType.IP,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
        ],
    ],
)
async def test_valid_git_root(
    git_root: Root,
    ip_root: Root,
) -> None:
    validate_git_root(git_root)
    with pytest.raises(InvalidGitRoot):
        validate_git_root(ip_root)


async def test_valid_git_root_deco() -> None:
    @validate_git_root_deco("root")
    def decorated_func(root: Root) -> Root:
        return root

    loaders = get_new_context()
    root = await roots_utils.get_root(
        loaders, "4039d098-ffc5-4984-8ed3-eb17bca98e19", "unittesting"
    )

    assert decorated_func(root=root)

    ip_root = await roots_utils.get_root(
        loaders, "d312f0b9-da49-4d2b-a881-bed438875e99", "oneshottest"
    )
    with pytest.raises(InvalidGitRoot):
        decorated_func(root=ip_root)


@pytest.mark.parametrize(
    ["git_root", "url_root", "ip_root"],
    [
        [
            GitRoot(
                cloning=GitRootCloning(
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:39:10+00:00"
                    ),
                    reason="root OK",
                    status=GitCloningStatus.OK,
                    commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
                    commit_date=datetime.fromisoformat(
                        "2022-02-15T18:45:06.493253+00:00"
                    ),
                ),
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-11-19T13:37:10+00:00"
                ),
                group_name="unittesting",
                id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                organization_name="okada",
                state=GitRootState(
                    branch="master",
                    environment="production",
                    includes_health_check=True,
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    nickname="universe",
                    status=RootStatus.ACTIVE,
                    url="https://gitlab.com/fluidattacks/universe",
                    credential_id=None,
                    gitignore=["bower_components/*", "node_modules/*"],
                    other=None,
                    reason=None,
                    use_vpn=False,
                ),
                type=RootType.GIT,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                ),
            ),
            URLRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
                group_name="oneshottest",
                id="8493c82f-2860-4902-86fa-75b0fef76034",
                organization_name="okada",
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:45:55+00:00"
                    ),
                    nickname="url_root_1",
                    other=None,
                    path="/",
                    port="443",
                    protocol="HTTPS",
                    reason=None,
                    status=RootStatus.ACTIVE,
                    query=None,
                ),
                type=RootType.URL,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
            IPRoot(
                created_by="jdoe@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-12-19T13:44:37+00:00"
                ),
                group_name="asgard",
                id="814addf0-316c-4415-850d-21bd3783b011",
                organization_name="okada",
                state=IPRootState(
                    address="127.0.0.1",
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-12-19T13:44:37+00:00"
                    ),
                    nickname="ip_root_2",
                    other=None,
                    reason=None,
                    status=RootStatus.INACTIVE,
                ),
                type=RootType.IP,
                unreliable_indicators=RootUnreliableIndicators(
                    unreliable_code_languages=[],
                    unreliable_last_status_update=None,
                ),
            ),
        ],
    ],
)
async def test_validate_root_type_deco(
    git_root: Root,
    ip_root: Root,
    url_root: Root,
) -> None:
    @validate_root_type_deco("root", (GitRoot,))
    def git_func(root: Root) -> Root:
        return root

    assert git_func(root=git_root)

    with pytest.raises(InvalidRootType):
        git_func(root=ip_root)
    with pytest.raises(InvalidRootType):
        git_func(root=url_root)

    @validate_root_type_deco("root", (URLRoot,))
    def url_func(root: Root) -> Root:
        return root

    assert url_func(root=url_root)

    with pytest.raises(InvalidRootType):
        url_func(root=ip_root)
    with pytest.raises(InvalidRootType):
        url_func(root=git_root)

    @validate_root_type_deco("root", (IPRoot,))
    def ip_func(root: Root) -> Root:
        return root

    assert ip_func(root=ip_root)

    with pytest.raises(InvalidRootType):
        ip_func(root=url_root)
    with pytest.raises(InvalidRootType):
        ip_func(root=git_root)


async def test_validate_git_access() -> None:
    await validate_git_access(
        url="https://app.fluidattacks.com",
        branch="trunk1",
        secret=OauthBitbucketSecret(
            brefresh_token="token",
            access_token="access_token",
            valid_until=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        ),
        loaders=get_new_context(),
    )
    with pytest.raises(InvalidUrl):
        await validate_git_access(
            url="https://app.fluidattacks.com:67000",
            branch="trunk",
            secret=SshSecret(key="test_key"),
            loaders=get_new_context(),
        )
    with pytest.raises(InvalidGitCredentials):
        await validate_git_access(
            url="https://app.fluidattacks.com",
            branch="trunk2",
            secret=OauthAzureSecret(
                arefresh_token="CFCzdCBTU0gK",
                redirect_uri="",
                access_token="DEDzdCBTU0gK",
                valid_until=get_now_minus_delta(hours=1),
            ),
            loaders=get_new_context(),
            organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            credential_id="5990e0ec-dc8f-4c9a-82cc-9da9fbb35c11",
        )
    with pytest.raises(InvalidGitCredentials):
        await validate_git_access(
            url="https://app.fluidattacks.com",
            branch="trunk1",
            secret=HttpsSecret(
                user="user",
                password="password",
            ),
            loaders=get_new_context(),
        )


async def test_validate_credential_in_organization() -> None:
    with pytest.raises(InvalidGitCredentials):
        await validate_credential_in_organization(
            loaders=get_new_context(),
            credential_id="test_id",
            organization_id="test_org",
        )


async def test_working_credentials() -> None:
    with pytest.raises(RequiredCredentials):
        await working_credentials(
            url="https://app.fluidattacks.com",
            branch="trunk",
            credentials=None,
            loaders=get_new_context(),
        )


async def test_is_git_unique() -> None:
    loaders = get_new_context()
    organization = await get_organization(loaders, "okada")
    roots = tuple(await loaders.organization_roots.load(organization.name))
    assert not is_git_unique(
        url="https://gitlab.com/fluidattacks/universe",
        branch="master",
        group_name="unittesting2",
        roots=roots,
    )
    assert not is_git_unique(
        url="https://gitlab.com/fluidattacks/universe",
        branch="main",
        group_name="unittesting",
        roots=roots,
    )


def test_validate_nickname() -> None:
    validate_nickname(nickname="valid-username_1")
    with pytest.raises(InvalidChar):
        validate_nickname(nickname="invalidusername!")


def test_validate_nickname_deco() -> None:
    @validate_nickname_deco("nickname")
    def decorated_func(nickname: str) -> str:
        return nickname

    assert decorated_func(nickname="valid-username_1")
    with pytest.raises(InvalidChar):
        decorated_func(nickname="invalidusername!")


async def test_validate_git_credentials_oauth() -> None:
    with pytest.raises(InvalidGitCredentials):
        await validate_git_credentials_oauth(
            repo_url="https://fluidattacks.com/universe",
            branch="trunk",
            loaders=get_new_context(),
            credential_id="158d1f7f-65c5-4c79-85e3-de3acfe03774",
            organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
        )


async def test_validate_nickname_is_unique_deco() -> None:
    @validate_nickname_is_unique_deco(
        nickname_field="nickname",
        roots_fields="roots",
        old_nickname_field="old_nickname",
    )
    def decorated_func(
        nickname: str, roots: tuple[Root, ...], old_nickname: str
    ) -> tuple:
        return (nickname, roots, old_nickname)

    loaders = get_new_context()
    root = await roots_utils.get_root(
        loaders, "d312f0b9-da49-4d2b-a881-bed438875e99", "oneshottest"
    )
    assert decorated_func(
        nickname="valid-username_1",
        roots=(root,),
        old_nickname="valid-username_2",
    )
    with pytest.raises(RepeatedRootNickname):
        decorated_func(
            nickname="ip_root_1",
            roots=(root,),
            old_nickname="valid-username_2",
        )


def test_validate_url_branch() -> None:
    @validate_url_branch_deco(url_field="url", branch_field="branch")
    def decorated_func(url: str, branch: str) -> str:
        return url + branch

    decorated_func(
        url="ssh://git@ssh.dev.azure.com:v3/company/project/",
        branch="master",
    )

    with pytest.raises(InvalidParameter):
        decorated_func(
            url="ssh://git@ssh.dev.azure.com:v3/company/project/",
            branch="( ͡° ͜ʖ ͡°)",
        )

    with pytest.raises(InvalidParameter):
        decorated_func(
            url="randomstring",
            branch="master",
        )
