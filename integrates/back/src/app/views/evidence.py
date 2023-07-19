# Starlette evidences-related methods


from aioextensions import (
    in_thread,
)
import aiohttp
import authz
from collections.abc import (
    Sequence,
)
from custom_exceptions import (
    EventNotFound,
    FindingNotFound,
    InvalidAuthorization,
)
from custom_utils import (
    files as files_utils,
    logs as logs_utils,
    templates,
    utils,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
from events.domain import (
    has_access_to_event,
)
from findings.domain import (
    has_access_to_finding,
)
import logging
import logging.config
from magic import (
    Magic,
)
from s3.operations import (
    download_file,
    list_files,
)
from sessions import (
    domain as sessions_domain,
)
from settings.logger import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
    Response,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


download_evidence_file = retry_on_exceptions(
    exceptions=(
        aiohttp.ClientError,
        aiohttp.ClientPayloadError,
    ),
    max_attempts=3,
    sleep_seconds=float("0.2"),
)(download_file)


async def enforce_group_level_role(
    loaders: Dataloaders,
    request: Request,
    group: str,
    *allowed_roles: Sequence[str],
) -> Response | None:
    response = None
    try:
        user_info = await sessions_domain.get_jwt_content(request)
    except InvalidAuthorization:
        return Response("Access denied", status_code=403)
    email = user_info["user_email"]
    requester_role = await authz.get_group_level_role(loaders, email, group)
    if requester_role not in allowed_roles:
        response = Response("Access denied", status_code=403)
    return response


async def _has_access_to_evidence(
    loaders: Dataloaders,
    email: str,
    finding_id: str,
    evidence_type: str,
    group_name: str,
) -> bool:
    try:
        return (
            evidence_type in ["drafts", "findings", "vulns"]
            and await has_access_to_finding(loaders, email, finding_id)
        ) or (
            evidence_type == "events"
            and await has_access_to_event(
                loaders, email, finding_id, group_name
            )
        )
    except (FindingNotFound, EventNotFound) as exc:
        LOGGER.exception(
            exc,
            extra={"evidence type": evidence_type, "finding_id": finding_id},
        )
        return False


async def get_evidence(  # pylint: disable=too-many-locals
    request: Request,
) -> Response:
    try:
        user_info = await sessions_domain.get_jwt_content(request)
    except InvalidAuthorization:
        return templates.unauthorized(request)
    email: str = user_info["user_email"]
    loaders: Dataloaders = get_new_context()
    group_name = request.path_params["group_name"]
    finding_id = request.path_params["finding_id"]
    file_id = request.path_params["file_id"]
    evidence_type = request.path_params["evidence_type"]

    allowed_roles = [
        "admin",
        "architect",
        "customer_manager",
        "hacker",
        "reattacker",
        "resourcer",
        "reviewer",
        "user",
        "user_manager",
        "vulnerability_manager",
    ]
    error = await enforce_group_level_role(
        loaders, request, group_name, *allowed_roles
    )
    if error is not None:
        return error
    if await _has_access_to_evidence(
        loaders, email, finding_id, evidence_type, group_name
    ):
        if file_id is None:
            return Response("Error - Unsent image ID", media_type="text/html")

        evidences_path: str = (
            f"evidences/{group_name.lower()}/{finding_id}/{file_id}"
        )
        evidences = await list_s3_evidences(evidences_path)
        if evidences:
            for evidence in evidences:
                start = evidence.find(finding_id) + len(finding_id)
                localfile = f"/tmp{evidence[start:]}"  # nosec
                localtmp = utils.replace_all(
                    localfile,
                    {".png": ".tmp", ".gif": ".tmp", ".webm": ".tmp"},
                )
                await download_evidence_file(evidence, localtmp)
                return await in_thread(retrieve_image, localtmp)
        else:
            return JSONResponse(
                {
                    "data": [],
                    "message": "Access denied or evidence not found",
                    "error": True,
                }
            )

    logs_utils.cloudwatch_log(
        request,
        "Security: Attempted to retrieve evidence without permission",
    )
    return JSONResponse(
        {"data": [], "message": "Evidence type not found", "error": True}
    )


async def list_s3_evidences(prefix: str) -> list[str]:
    return list(await list_files(prefix))


def retrieve_image(img_file: str) -> Response:
    if files_utils.assert_file_mime(
        img_file, ["image/png", "image/jpeg", "image/gif", "video/webm"]
    ):
        with open(img_file, "rb") as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return Response(file_obj.read(), media_type=mime_type)
    else:
        return Response(
            "Error: Invalid evidence image format", media_type="text/html"
        )
