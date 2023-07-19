from aioextensions import (
    collect,
    schedule,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAuthorization,
    UnableToSendMail,
)
from custom_utils import (
    datetime as datetime_utils,
)
from custom_utils.datetime import (
    get_as_epoch,
    get_now_plus_delta,
)
from custom_utils.validations_deco import (
    validate_email_address_deco,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    group_access as group_access_model,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessRequest,
    GroupAccessState,
    GroupConfirmDeletion,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
)
from jwcrypto.jwe import (
    JWException,
)
from jwcrypto.jwt import (
    JWTExpired,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.common import (
    send_mail_confirm_deletion,
)
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)

mail_confirm_deletion = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_confirm_deletion)


async def remove_stakeholder_all_organizations(
    *, email: str, modified_by: str
) -> None:
    loaders: Dataloaders = get_new_context()
    active, inactive = await collect(
        [
            group_access_domain.get_stakeholder_groups_names(
                loaders, email, active=True
            ),
            group_access_domain.get_stakeholder_groups_names(
                loaders, email, active=False
            ),
        ]
    )
    stakeholder_groups = set(active + inactive)
    await collect(
        tuple(
            group_access_domain.remove_access(loaders, email, group)
            for group in stakeholder_groups
        )
    )

    loaders = get_new_context()
    organizations_access = await loaders.stakeholder_organizations_access.load(
        email
    )
    organizations_ids: list[str] = [
        org.organization_id for org in organizations_access
    ]
    await collect(
        tuple(
            orgs_domain.remove_access(
                organization_id=organization_id,
                email=email,
                modified_by=modified_by,
                send_reassignment_email=True,
            )
            for organization_id in organizations_ids
        )
    )

    await stakeholders_domain.remove(email)


async def complete_deletion(*, email: str) -> None:
    await group_access_model.remove(email=email, group_name="confirm_deletion")
    await remove_stakeholder_all_organizations(
        email=email,
        modified_by=email,
    )


async def get_email_from_url_token(
    *,
    loaders: Dataloaders,
    url_token: str,
) -> str:
    try:
        token_content = sessions_domain.decode_token(url_token)
    except (JWException, JWTExpired) as ex:
        raise InvalidAuthorization() from ex

    email: str = token_content["user_email"]
    if not await group_access_domain.exists(
        loaders=loaders, group_name="confirm_deletion", email=email
    ):
        return ""

    access_with_deletion = await loaders.group_access.load(
        GroupAccessRequest(group_name="confirm_deletion", email=email)
    )
    if access_with_deletion and (
        access_with_deletion.confirm_deletion
        and access_with_deletion.confirm_deletion.url_token == url_token
    ):
        return email

    return ""


async def get_confirm_deletion(
    *,
    loaders: Dataloaders,
    email: str,
) -> GroupAccess | None:
    if await group_access_domain.exists(loaders, "confirm_deletion", email):
        confirm_deletion = await loaders.group_access.load(
            GroupAccessRequest(group_name="confirm_deletion", email=email)
        )

        return confirm_deletion
    return None


@validate_email_address_deco("email")
async def confirm_deletion_mail(
    *,
    loaders: Dataloaders,
    email: str,
) -> None:
    expiration_time = get_as_epoch(get_now_plus_delta(weeks=1))
    url_token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload={
            "user_email": email,
        },
        subject="starlette_session",
    )
    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name="confirm_deletion",
        metadata=GroupAccessMetadataToUpdate(
            expiration_time=expiration_time,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
            confirm_deletion=GroupConfirmDeletion(
                is_used=False,
                url_token=url_token,
            ),
        ),
    )
    confirm_access_url = f"{BASE_URL}/confirm_deletion/{url_token}"
    mail_to = [email]
    email_context: dict[str, str | bool] = {
        "email": email,
        "confirm_deletion_url": confirm_access_url,
        "empty_notification_notice": True,
    }
    schedule(mail_confirm_deletion(loaders, mail_to, email_context))
