from aioextensions import (
    collect,
)
from app.utils import (
    get_redirect_url,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from authz.enforcer import (
    get_organization_level_enforcer,
)
from batch.dal import (
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
    CredentialAlreadyExists,
    InvalidAuthorization,
)
from custom_utils.datetime import (
    get_minus_delta,
    get_plus_delta,
    get_utc_now,
)
from custom_utils.stakeholders import (
    get_full_name,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as credentials_model,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupSubscriptionType,
)
from db_model.organizations.types import (
    Organization,
)
from enum import (
    Enum,
)
from groups import (
    domain as groups_domain,
)
from httpx import (
    ConnectTimeout,
)
import json
import logging
import logging.config
from oauth import (
    OAUTH as ROAUTH,
)
from oauth.azure import (
    get_azure_refresh_token,
)
from oauth.bitbucket import (
    get_bitbucket_refresh_token,
)
from oauth.github import (
    get_access_token,
)
from oauth.gitlab import (
    get_refresh_token,
)
from organization_access import (
    domain as orgs_access,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.utils import (
    get_organization,
)
from organizations.validations import (
    validate_credentials_name_in_organization,
    validate_credentials_oauth,
)
from sessions.domain import (
    get_jwt_content,
)
from settings import (
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from starlette.datastructures import (
    QueryParams,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    RedirectResponse,
    Response,
)
from urllib3.util.url import (
    parse_url,
)
from urllib.parse import (
    urlencode,
)
import uuid

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)

AZURE_REDIRECT_URI = "azure_repository_authlib_redirect_uri"


class RepoProvider(Enum):
    AZURE = "azure"
    BITBUCKET = "bitbucket"
    GITHUB = "github"
    GITLAB = "gitlab"


async def _validate(
    *,
    loaders: Dataloaders,
    email: str,
    organization_id: str,
) -> None:
    enforcer = await get_organization_level_enforcer(loaders, email)
    if not enforcer(
        organization_id, "api_mutations_add_credentials_mutate"
    ) or not await orgs_access.has_access(
        loaders=loaders,
        email=email,
        organization_id=organization_id,
    ):
        raise PermissionError("Access denied")


async def _put_action(
    *,
    organization_id: str,
    credentials_id: str,
) -> None:
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


async def get_authorized_redirect(
    request: Request, provider: RepoProvider
) -> Response:
    redirect_uri = get_redirect_url(request, f"oauth_{provider.value}")
    url = f"{redirect_uri}?{urlencode(request.query_params)}"
    oauth_client = ROAUTH.create_client(provider.value)

    if provider == RepoProvider.AZURE:
        # Azure does not support propagating query params
        request.session[AZURE_REDIRECT_URI] = url
        return await oauth_client.authorize_redirect(request, redirect_uri)

    return await oauth_client.authorize_redirect(request, url)


async def _begin_repo_oauth(
    request: Request, provider: RepoProvider
) -> Response:
    if request.query_params.get("fast_track"):
        return await get_authorized_redirect(request, provider)

    loaders = get_new_context()
    organization_id: str = request.query_params["subject"]
    user_info = await get_jwt_content(request)
    email: str = user_info["user_email"]
    try:
        await _validate(
            loaders=loaders, email=email, organization_id=organization_id
        )
    except PermissionError:
        return RedirectResponse(url="/home")
    secret_type = {
        RepoProvider.AZURE: OauthAzureSecret,
        RepoProvider.BITBUCKET: OauthBitbucketSecret,
        RepoProvider.GITHUB: OauthGithubSecret,
        RepoProvider.GITLAB: OauthGitlabSecret,
    }[provider]
    with suppress(CredentialAlreadyExists):
        await validate_credentials_oauth(
            get_new_context(),
            organization_id,
            email,
            secret_type,
        )

        return await get_authorized_redirect(request, provider)

    return RedirectResponse(url="/home")


async def do_azure_oauth(request: Request) -> Response:
    return await _begin_repo_oauth(request, RepoProvider.AZURE)


async def do_bitbucket_oauth(request: Request) -> Response:
    return await _begin_repo_oauth(request, RepoProvider.BITBUCKET)


async def do_github_oauth(request: Request) -> Response:
    return await _begin_repo_oauth(request, RepoProvider.GITHUB)


async def do_gitlab_oauth(request: Request) -> Response:
    return await _begin_repo_oauth(request, RepoProvider.GITLAB)


async def _get_azure_secret(request: Request) -> OauthAzureSecret:
    code: str = request.query_params["code"]
    redirect = get_redirect_url(request, "oauth_azure")
    token_data = await get_azure_refresh_token(
        code=code, redirect_uri=redirect
    )

    if not token_data:
        raise OAuthError()

    return OauthAzureSecret(
        arefresh_token=token_data["refresh_token"],
        redirect_uri=redirect,
        access_token=token_data["access_token"],
        valid_until=get_plus_delta(
            get_minus_delta(get_utc_now(), seconds=60),
            seconds=int(token_data["expires_in"]),
        ),
    )


async def _get_bitbucket_secret(request: Request) -> OauthBitbucketSecret:
    code: str = request.query_params["code"]
    redirect = get_redirect_url(request, "oauth_bitbucket")
    params = {
        key: value
        for key, value in request.query_params.items()
        if key in {"fast_track", "subject"}
    }
    uri = f"{redirect}?{urlencode(params)}"
    token_data = await get_bitbucket_refresh_token(code=code, redirect_uri=uri)

    if not token_data:
        raise OAuthError()

    return OauthBitbucketSecret(
        brefresh_token=token_data["refresh_token"],
        access_token=token_data["access_token"],
        valid_until=get_plus_delta(
            get_minus_delta(get_utc_now(), seconds=60),
            seconds=int(token_data["expires_in"]),
        ),
    )


async def _get_github_secret(request: Request) -> OauthGithubSecret:
    code: str = request.query_params["code"]
    token = await get_access_token(code=code)

    if not token:
        raise OAuthError()

    return OauthGithubSecret(access_token=token)


async def _get_gitlab_secret(request: Request) -> OauthGitlabSecret:
    code: str = request.query_params["code"]
    redirect = get_redirect_url(request, "oauth_gitlab")
    params = {
        key: value
        for key, value in request.query_params.items()
        if key in {"fast_track", "subject"}
    }
    uri = f"{redirect}?{urlencode(params)}"
    token_data = await get_refresh_token(
        code=code,
        redirect_uri=uri,
        code_verifier=request.session.get(
            "_gitlab_authlib_code_verifier_", ""
        ),
    )

    if not token_data:
        raise OAuthError()

    return OauthGitlabSecret(
        refresh_token=token_data["refresh_token"],
        redirect_uri=uri,
        access_token=token_data["access_token"],
        valid_until=get_plus_delta(
            datetime.utcfromtimestamp(token_data["created_at"]),
            seconds=token_data["expires_in"],
        ),
    )


def _get_params_from_uri(uri: str) -> QueryParams:
    return QueryParams(str(parse_url(uri).query))


def _sanitize(name: str) -> str:
    return "".join([char for char in name if char.isalpha()])


def _generate_name(email: str) -> str:
    base_name = email.split("@")[0]
    domain_name = email.split("@")[1].split(".")[0]
    result = "".join([_sanitize(base_name)[:5], _sanitize(domain_name)[:10]])
    return result.lower()


async def _get_fast_track_org(request: Request) -> Organization:
    user_info = await get_jwt_content(request)
    email = user_info["user_email"]
    name = _generate_name(email)
    organization = await orgs_domain.add_organization(
        loaders=get_new_context(),
        organization_name=name,
        email=email,
        country=request.headers.get("cf-ipcountry", "Undefined"),
    )
    await groups_domain.add_group(
        loaders=get_new_context(),
        description="Trial group",
        email=email,
        granted_role="user_manager",
        group_name=name,
        has_machine=True,
        has_squad=False,
        language=GroupLanguage.EN,
        organization_name=organization.id,
        service=GroupService.WHITE,
        subscription=GroupSubscriptionType.CONTINUOUS,
    )
    await stakeholders_domain.add_enrollment(
        loaders=get_new_context(),
        user_email=email,
        full_name=get_full_name(user_info),
    )
    return organization


async def _get_organization_id(
    request: Request, provider: RepoProvider
) -> str:
    if request.query_params.get("fast_track"):
        org = await _get_fast_track_org(request)
        return org.id

    if provider == RepoProvider.AZURE:
        # Azure does not support propagating query params
        azure_uri = request.session.pop(AZURE_REDIRECT_URI)
        params_azure_uri = _get_params_from_uri(azure_uri)
        if "fast_track" in params_azure_uri and params_azure_uri["fast_track"]:
            return (await _get_fast_track_org(request)).id

        return params_azure_uri["subject"]

    return request.query_params["subject"]


async def _end_repo_oauth(
    request: Request, provider: RepoProvider
) -> RedirectResponse:
    # PART 1: Get params
    if "code" not in request.query_params:
        # User declined to consent to access the app
        return RedirectResponse(url="/home")

    try:
        organization_id = await _get_organization_id(request, provider)
    except (KeyError, InvalidAuthorization) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return RedirectResponse(url="/home")

    # PART 2: Validate Access
    loaders = get_new_context()
    user_info = await get_jwt_content(request)
    await _validate(
        loaders=loaders,
        email=user_info["user_email"],
        organization_id=organization_id,
    )

    # PART 3: Get secret
    provider_name = {
        RepoProvider.AZURE: "Azure OAuth",
        RepoProvider.BITBUCKET: "Bitbucket OAuth",
        RepoProvider.GITHUB: "GitHub OAuth",
        RepoProvider.GITLAB: "GitLab OAuth",
    }[provider]
    get_secret = {
        RepoProvider.AZURE: _get_azure_secret,
        RepoProvider.BITBUCKET: _get_bitbucket_secret,
        RepoProvider.GITHUB: _get_github_secret,
        RepoProvider.GITLAB: _get_gitlab_secret,
    }[provider]

    try:
        secret = await get_secret(request)
    except (ConnectTimeout, KeyError, OAuthError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return RedirectResponse(url="/home")

    # PART 4: Store credentials
    name = (
        f'{user_info["user_email"].split("@", maxsplit=1)[0]}'
        + f"({provider_name})"
    )
    credentials_id: str = str(uuid.uuid4())
    credential = Credentials(
        id=credentials_id,
        organization_id=organization_id,
        owner=user_info["user_email"],
        state=CredentialsState(
            modified_by=user_info["user_email"],
            modified_date=get_utc_now(),
            name=name,
            secret=secret,  # type: ignore
            type=CredentialType.OAUTH,
            is_pat=False,
            azure_organization=None,
        ),
    )
    await collect(
        (
            validate_credentials_name_in_organization(
                loaders, credential.organization_id, credential.state.name
            ),
            validate_credentials_oauth(
                loaders,
                credential.organization_id,
                credential.owner,
                type(secret),  # type: ignore
            ),
        )
    )
    await credentials_model.add(credential=credential)
    await _put_action(
        organization_id=credential.organization_id,
        credentials_id=credential.id,
    )

    if request.query_params.get("fast_track"):
        return RedirectResponse(url="/home?fast_track_end=true")

    organization = await get_organization(loaders, credential.organization_id)
    return RedirectResponse(url=f"/orgs/{organization.name}/credentials")


async def oauth_azure(request: Request) -> RedirectResponse:
    return await _end_repo_oauth(request, RepoProvider.AZURE)


async def oauth_bitbucket(request: Request) -> RedirectResponse:
    return await _end_repo_oauth(request, RepoProvider.BITBUCKET)


async def oauth_github(request: Request) -> RedirectResponse:
    return await _end_repo_oauth(request, RepoProvider.GITHUB)


async def oauth_gitlab(request: Request) -> RedirectResponse:
    return await _end_repo_oauth(request, RepoProvider.GITLAB)
