# Starlette app init file

from .middleware import (
    CustomRequestMiddleware,
)
from .views import (
    auth,
    charts,
    evidence,
)
from aioextensions import (
    in_thread,
)
from api import (
    IntegratesAPI,
)
from app.views.oauth import (
    do_azure_oauth,
    do_bitbucket_oauth,
    do_github_oauth,
    do_gitlab_oauth,
    oauth_azure,
    oauth_bitbucket,
    oauth_github,
    oauth_gitlab,
)
from billing.domain import (
    webhook,
)
import bugsnag
from bugsnag.asgi import (
    BugsnagMiddleware,
)
from context import (
    FI_ENVIRONMENT,
    FI_STARLETTE_SESSION_KEY,
)
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
    SecureAccessException,
    StakeholderNotInGroup,
    StakeholderNotInOrganization,
)
from custom_utils import (
    analytics,
    templates,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from decorators import (
    authenticate_session,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from remove_stakeholder import (
    domain as remove_stakeholder_domain,
)
from s3.resource import (
    s3_shutdown,
    s3_startup,
)
from search.client import (
    search_shutdown,
    search_startup,
)
from sessions import (
    domain as sessions_domain,
)
from settings import (
    DEBUG,
    JWT_COOKIE_NAME,
    LOGGING,
    TEMPLATES_DIR,
)
from settings.session import (
    SESSION_COOKIE_SAME_SITE,
)
from sqs.resources import (
    sqs_shutdown,
    sqs_startup,
)
from starlette.applications import (
    Starlette,
)
from starlette.middleware import (
    Middleware,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
)
from starlette.routing import (
    Mount,
    Route,
)
from starlette.staticfiles import (
    StaticFiles,
)
from starlette_prometheus import (
    metrics,
    PrometheusMiddleware,
)
from telemetry import (
    instrumentation,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


@authenticate_session
async def app(request: Request) -> HTMLResponse:
    """View for authenticated users."""
    user_info = await sessions_domain.get_jwt_content(request)
    email = user_info["user_email"]
    try:
        if FI_ENVIRONMENT == "production":
            await sessions_domain.check_session_web_validity(request, email)
        response = templates.main_app(request)
    except SecureAccessException:
        response = await logout(request)
    return response


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            group_access = await group_access_domain.get_access_by_url_token(
                loaders, url_token
            )
            await groups_domain.complete_register_for_group_invitation(
                loaders, group_access
            )
            response = templates.valid_invitation(
                request, group_access.group_name
            )
        except (StakeholderNotInGroup, InvalidAuthorization):
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def confirm_deletion(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            user_email: str = (
                await remove_stakeholder_domain.get_email_from_url_token(
                    loaders=loaders, url_token=url_token
                )
            )
            if user_email:
                await remove_stakeholder_domain.complete_deletion(
                    email=user_email
                )
                response = templates.confirm_deletion(request=request)
            else:
                await in_thread(
                    bugsnag.notify,
                    Exception("Invalid token"),
                    severity="error",
                )
                response = templates.invalid_confirm_deletion(
                    request=request, error="Invalid or Expired"
                )
        except (StakeholderNotInGroup, InvalidAuthorization):
            response = templates.invalid_confirm_deletion(
                request=request, error="Invalid or Expired"
            )
    else:
        response = templates.invalid_confirm_deletion(
            request=request, error="Invalid or Expired"
        )

    return response


async def confirm_access_organization(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            organization_access: OrganizationAccess = (
                await orgs_domain.get_access_by_url_token(loaders, url_token)
            )
            await orgs_domain.complete_register_for_organization_invitation(
                loaders, organization_access
            )
            organization = await orgs_utils.get_organization(
                loaders, organization_access.organization_id
            )
            response = templates.valid_invitation(request, organization.name)
        except (StakeholderNotInOrganization, InvalidAuthorization):
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def reject_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            group_access = await group_access_domain.get_access_by_url_token(
                loaders, url_token
            )
            invitation = group_access.invitation
            if invitation and invitation.is_used:
                return templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access.group_name,
                )
            await groups_domain.reject_register_for_group_invitation(
                loaders, group_access
            )
            response = templates.reject_invitation(
                request, group_access.group_name
            )
        except (StakeholderNotInGroup, InvalidAuthorization):
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def reject_access_organization(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            organization_access: OrganizationAccess = (
                await orgs_domain.get_access_by_url_token(loaders, url_token)
            )
            await orgs_domain.reject_register_for_organization_invitation(
                organization_access
            )
            organization = await orgs_utils.get_organization(
                loaders, organization_access.organization_id
            )
            response = templates.reject_invitation(request, organization.name)
        except (StakeholderNotInOrganization, InvalidAuthorization):
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def logout(request: Request) -> HTMLResponse:
    """Close a user's active session."""
    try:
        user_info = await sessions_domain.get_jwt_content(request)
    except (ExpiredToken, InvalidAuthorization):
        return templates.unauthorized(request)

    user_email = user_info["user_email"]
    await sessions_domain.remove_session_token(user_info, user_email)
    await sessions_domain.remove_session_key(user_email)
    await analytics.mixpanel_track(user_email, "Logout")

    request.session.clear()
    response = RedirectResponse("/")
    response.delete_cookie(key=JWT_COOKIE_NAME)
    response.headers["Clear-Site-Data"] = '"executionContexts", "cache"'
    return response  # type: ignore


def not_found(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error401(request)


def server_error(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error500(request)


exception_handlers = {404: not_found, 500: server_error}

APP = Starlette(
    debug=DEBUG,
    on_startup=[
        dynamo_startup,
        instrumentation.initialize,
        s3_startup,
        sqs_startup,
        search_startup,
    ],
    on_shutdown=[
        dynamo_shutdown,
        search_shutdown,
        s3_shutdown,
        sqs_shutdown,
    ],
    routes=[
        Route("/", templates.login),
        Route("/api", IntegratesAPI()),
        Route("/authz_azure", auth.authz_azure),
        Route("/dgitlab", do_gitlab_oauth),
        Route("/oauth_gitlab", oauth_gitlab),
        Route("/dgithub", do_github_oauth),
        Route("/oauth_github", oauth_github),
        Route("/dbitbucket", do_bitbucket_oauth),
        Route("/dazure", do_azure_oauth),
        Route("/oauth_azure", oauth_azure),
        Route("/oauth_bitbucket", oauth_bitbucket),
        Route("/authz_bitbucket", auth.authz_bitbucket),
        Route("/authz_google", auth.authz_google),
        Route("/confirm_access/{url_token:path}", confirm_access),
        Route(
            "/confirm_access_organization/{url_token:path}",
            confirm_access_organization,
        ),
        Route("/confirm_deletion/{url_token:path}", confirm_deletion),
        Route("/dglogin", auth.do_google_login),
        Route("/dalogin", auth.do_azure_login),
        Route("/dblogin", auth.do_bitbucket_login),
        Route("/error401", templates.error401),
        Route("/error500", templates.error500),
        Route("/graphic", charts.graphic),
        Route("/graphic-csv", charts.graphic_csv),
        Route("/graphics-for-group", charts.graphics_for_group),
        Route("/graphics-for-organization", charts.graphics_for_organization),
        Route("/graphics-for-portfolio", charts.graphics_for_portfolio),
        Route("/graphics-report", charts.graphics_report),
        Route("/invalid_invitation", templates.invalid_invitation),
        Route("/metrics", metrics),
        Route("/logout", logout),
        Route(
            "/orgs/{org_name:str}/groups/"
            "{group_name:str}/{evidence_type:str}/"
            "{finding_id:str}/locations/{file_id:str}",
            templates.login,
        ),
        Route(
            "/orgs/{org_name:str}/groups/"
            "{group_name:str}/{evidence_type:str}/"
            "{finding_id:str}/{_:str}/{file_id:str}",
            evidence.get_evidence,
        ),
        Route("/reject_access/{url_token:path}", reject_access),
        Route(
            "/reject_access_organization/{url_token:path}",
            reject_access_organization,
        ),
        Route("/SignUp", templates.login),
        Mount(
            "/static",
            StaticFiles(directory=f"{TEMPLATES_DIR}/static"),
            name="static",
        ),
        Route("/billing", webhook, methods=["POST"]),
        Route("/{full_path:path}", app),
    ],
    middleware=[
        Middleware(BugsnagMiddleware),
        Middleware(
            SessionMiddleware,
            secret_key=FI_STARLETTE_SESSION_KEY,
            same_site=SESSION_COOKIE_SAME_SITE,
            https_only=True,
        ),
        Middleware(CustomRequestMiddleware),
        Middleware(PrometheusMiddleware, filter_unhandled_paths=True),
    ],
    exception_handlers=exception_handlers,
)

instrumentation.instrument_app(APP)
