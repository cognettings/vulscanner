# Starlette charts views
from analytics import (
    domain as analytics_domain,
)
from custom_exceptions import (
    InvalidAuthorization,
)
from custom_utils import (
    templates,
)
from sessions import (
    domain as sessions_domain,
)
from sessions.types import (
    UserAccessInfo,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)


async def graphic(request: Request) -> Response:
    return await analytics_domain.handle_graphic_request(request)


async def graphic_csv(request: Request) -> Response:
    return await analytics_domain.handle_graphic_csv_request(request)


async def graphics_for_entity(entity: str, request: Request) -> Response:
    try:
        request_data = await sessions_domain.get_jwt_content(request)
    except InvalidAuthorization:
        return templates.unauthorized(request)
    response = await analytics_domain.handle_graphics_for_entity_request(
        entity=entity,
        request=request,
    )
    jwt_token = await sessions_domain.create_session_token(
        UserAccessInfo(
            first_name=request_data["first_name"],
            last_name=request_data["last_name"],
            user_email=request_data["user_email"],
        )
    )
    sessions_domain.set_token_in_response(response, jwt_token)  # type: ignore
    return response


async def graphics_for_group(request: Request) -> Response:
    return await graphics_for_entity("group", request)


async def graphics_for_organization(request: Request) -> Response:
    return await graphics_for_entity("organization", request)


async def graphics_for_portfolio(request: Request) -> Response:
    return await graphics_for_entity("portfolio", request)


async def graphics_report(request: Request) -> Response:
    return await analytics_domain.handle_graphics_report_request(request)
