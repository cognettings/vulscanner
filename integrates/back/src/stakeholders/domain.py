from aioextensions import (
    collect,
    schedule,
)
from authz.validations import (
    validate_fluidattacks_staff_on_group_deco,
    validate_role_fluid_reqs_deco,
)
from context import (
    FI_MAIL_CXO,
)
from custom_exceptions import (
    InvalidExpirationTime,
    InvalidField,
    InvalidFieldLength,
    InvalidParameter,
    OrganizationNotFound,
    RequiredNewPhoneNumber,
    RequiredVerificationCode,
    SamePhoneNumber,
    StakeholderNotFound,
    TokenCouldNotBeAdded,
    TokenNotFound,
    UnableToSendMail,
)
from custom_utils import (
    analytics as analytics_utils,
    datetime as datetime_utils,
    logs as logs_utils,
    validations,
)
from custom_utils.validations_deco import (
    validate_alphanumeric_field_deco,
    validate_email_address_deco,
    validate_fields_deco,
    validate_fields_length_deco,
    validate_length_deco,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    stakeholders as stakeholders_model,
    trials as trials_model,
    vulnerabilities as vulns_model,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupInvitation,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    AccessTokens,
    NotificationsPreferences,
    Stakeholder,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderState,
    StakeholderTours,
)
from db_model.trials.types import (
    Trial,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.trial import (
    send_mail_free_trial_start,
)
from organization_access import (
    domain as org_access_domain,
)
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from settings import (
    LOGGING,
)
from stakeholders.utils import (
    get_international_format_phone_number,
)
from stakeholders.validations import (
    validate_phone_deco,
)
from typing import (
    Any,
)
import uuid
from verify import (
    operations as verify_operations,
)
from verify.enums import (
    Channel,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def get_stakeholder(
    loaders: Dataloaders,
    email: str,
    user_email: str | None = None,
) -> Stakeholder:
    if user_email and not validations.is_fluid_staff(user_email):
        if validations.is_fluid_staff(email):
            raise StakeholderNotFound()

    stakeholder = await loaders.stakeholder.load(email)

    if stakeholder:
        return stakeholder

    raise StakeholderNotFound()


async def acknowledge_concurrent_session(email: str) -> None:
    """Acknowledge termination of concurrent session."""
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            is_concurrent_session=False,
        ),
        email=email,
    )


async def remove(email: str) -> None:
    loaders: Dataloaders = get_new_context()
    me_vulnerabilities = await loaders.me_vulnerabilities.load(email)
    await collect(
        tuple(
            vulns_model.update_assigned_index(
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=None,
            )
            for vulnerability in me_vulnerabilities
        ),
        workers=8,
    )
    await stakeholders_model.remove(email=email)
    LOGGER.info(
        "Stakeholder removed from db",
        extra={"extra": {"email": email}},
    )


@validate_length_deco("responsibility", max_length=50)
@validate_alphanumeric_field_deco("responsibility")
async def _update_information(
    *,
    context: Any,
    email: str,
    group_name: str,
    responsibility: str,
    role: str,
) -> None:
    await group_access_domain.update(
        loaders=context.loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            responsibility=responsibility,
            role=role,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )


async def update_information(
    context: Any, modified_data: dict[str, str], group_name: str
) -> None:
    email = modified_data["email"]
    responsibility = modified_data["responsibility"]
    role = modified_data["role"]
    if responsibility:
        try:
            await _update_information(
                context=context,
                email=email,
                group_name=group_name,
                responsibility=responsibility,
                role=role,
            )
        except InvalidFieldLength as exc:
            logs_utils.cloudwatch_log(
                context,
                f"Security: {email} Attempted to add responsibility to "
                f"group {group_name} bypassing validation",
            )
            raise exc
        except InvalidField as exc:
            logs_utils.cloudwatch_log(
                context,
                f"Security: {email} Attempted to add responsibility to "
                f"group {group_name} bypassing validation",
            )
            raise exc


async def register(email: str) -> None:
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(is_registered=True),
        email=email,
    )


async def remove_access_token(
    email: str, loaders: Dataloaders, token_id: str | None = None
) -> None:
    """Remove access token attribute"""
    if token_id:
        loaders.stakeholder.clear(email)
        stakeholder = await get_stakeholder(loaders, email)
        if next(
            (
                token
                for token in stakeholder.access_tokens
                if token.id == token_id
            ),
            None,
        ):
            await stakeholders_model.update_metadata(
                metadata=StakeholderMetadataToUpdate(
                    access_tokens=[
                        token
                        for token in stakeholder.access_tokens
                        if token.id != token_id
                    ],
                ),
                email=email,
            )
            return

        raise TokenNotFound()

    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            access_tokens=[],
        ),
        email=email,
    )


async def _get_access_tokens(
    *,
    email: str,
    loaders: Dataloaders,
    iat: int,
    name: str,
    token_data: dict[str, str],
    many_tokens: bool,
) -> list[AccessTokens]:
    new_token = [
        AccessTokens(
            id=str(uuid.uuid4()),
            issued_at=iat,
            name=name,
            jti_hashed=token_data["jti_hashed"],
            salt=token_data["salt"],
        )
    ]
    if not many_tokens:
        return new_token

    loaders.stakeholder.clear(email)
    stakeholder = await get_stakeholder(loaders, email)
    if len(stakeholder.access_tokens) >= 2:
        raise TokenCouldNotBeAdded()

    return stakeholder.access_tokens + new_token


@validate_fields_deco(["name"])
@validate_fields_length_deco(
    ["name"],
    min_length=1,
    max_length=20,
)
async def update_access_token(
    *,
    email: str,
    expiration_time: int,
    loaders: Dataloaders,
    name: str,
    many_tokens: bool = False,
    **kwargs_token: Any,
) -> str:
    """Update access token"""
    token_data = sessions_utils.calculate_hash_token()
    session_jwt = ""

    if sessions_utils.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = sessions_domain.encode_token(
            expiration_time=expiration_time,
            payload={
                "user_email": email,
                "jti": token_data["jti"],
                "iat": iat,
                **kwargs_token,
            },
            subject="api_token",
            api=True,
        )
        await stakeholders_model.update_metadata(
            metadata=StakeholderMetadataToUpdate(
                access_tokens=await _get_access_tokens(
                    email=email,
                    loaders=loaders,
                    iat=iat,
                    name=name,
                    token_data=token_data,
                    many_tokens=many_tokens,
                ),
            ),
            email=email,
        )
    else:
        raise InvalidExpirationTime()

    return session_jwt


async def update_legal_remember(email: str, remember: bool) -> None:
    """Remember legal notice acceptance."""
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            legal_remember=remember,
        ),
        email=email,
    )


async def update_last_login(email: str) -> None:
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            last_login_date=datetime_utils.get_utc_now(),
        ),
        email=email,
    )


async def update_notification_preferences(
    email: str, preferences: NotificationsPreferences
) -> None:
    await stakeholders_model.update_state(
        user_email=email,
        state=StakeholderState(
            notifications_preferences=preferences,
            modified_date=datetime_utils.get_utc_now(),
            modified_by=email.lower().strip(),
        ),
    )


@validate_length_deco("responsibility", max_length=50)
@validate_alphanumeric_field_deco("responsibility")
@validate_email_address_deco("email")
@validate_role_fluid_reqs_deco("email", "role")
@validate_fluidattacks_staff_on_group_deco("group", "email", "role")
async def update_invited_stakeholder(
    *,
    loaders: Dataloaders,
    email: str,
    responsibility: str,
    role: str,
    invitation: GroupInvitation,
    group: Group,
) -> None:
    new_invitation = invitation._replace(
        responsibility=responsibility, role=role
    )
    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name=group.name,
        metadata=GroupAccessMetadataToUpdate(
            invitation=new_invitation,
            responsibility=responsibility,
            role=role,
            state=GroupAccessState(modified_date=datetime_utils.get_utc_now()),
        ),
    )


async def update(*, email: str, metadata: StakeholderMetadataToUpdate) -> None:
    return await stakeholders_model.update_metadata(
        email=email, metadata=metadata
    )


mail_free_trial_start = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_free_trial_start)


async def add_experience_manager(
    loaders: Dataloaders, organization_id: str, group_name: str
) -> None:
    role = "customer_manager"
    await org_access_domain.add_access(
        loaders, organization_id, FI_MAIL_CXO, role
    )
    await group_access_domain.add_access(
        loaders, FI_MAIL_CXO, group_name, role
    )


@validate_email_address_deco("user_email")
async def add_enrollment(
    *,
    loaders: Dataloaders,
    user_email: str,
    full_name: str,
) -> None:
    if not user_email:
        raise InvalidParameter()

    await trials_model.add(
        trial=Trial(
            completed=False,
            email=user_email,
            extension_date=None,
            extension_days=0,
            start_date=datetime_utils.get_utc_now(),
        )
    )
    await update(
        email=user_email, metadata=StakeholderMetadataToUpdate(enrolled=True)
    )

    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        user_email
    )
    organization_id = stakeholder_orgs[0].organization_id
    organization = await loaders.organization.load(organization_id)
    if not organization:
        raise OrganizationNotFound()

    group_name = (
        await group_access_domain.get_stakeholder_groups_names(
            loaders, user_email, True
        )
    )[0]

    schedule(mail_free_trial_start(loaders, user_email, full_name, group_name))
    schedule(add_experience_manager(loaders, organization_id, group_name))
    # Fallback event
    await analytics_utils.mixpanel_track(
        user_email,
        "AutoenrollSubmit",
        group=group_name,
        mp_country_code=organization.country,
        organization=organization.name,
        User=full_name,
    )


@validate_phone_deco("new_phone")
async def update_mobile(
    *, email: str, new_phone: StakeholderPhone, verification_code: str
) -> None:
    """Update the stakeholder's phone number."""
    await verify_operations.validate_mobile(
        phone_number=get_international_format_phone_number(new_phone)
    )
    country_code = await verify_operations.get_country_code(
        get_international_format_phone_number(new_phone)
    )
    await verify_operations.check_verification(
        recipient=get_international_format_phone_number(new_phone),
        code=verification_code,
    )
    stakeholder_phone = StakeholderPhone(
        calling_country_code=new_phone.calling_country_code,
        country_code=country_code,
        national_number=new_phone.national_number,
    )
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            phone=stakeholder_phone,
        ),
        email=email,
    )


async def update_tours(email: str, tours: dict[str, bool]) -> None:
    """New stakeholder workflow acknowledgment."""
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            tours=StakeholderTours(
                new_group=tours["new_group"],
                new_root=tours["new_root"],
                new_risk_exposure=tours["new_risk_exposure"],
                welcome=tours["welcome"],
            ),
        ),
        email=email,
    )


@validate_phone_deco("new_phone")
async def verify(
    *,
    loaders: Dataloaders,
    email: str,
    new_phone: StakeholderPhone | None,
    verification_code: str | None,
) -> None:
    """Start a verification process using OTP"""
    stakeholder = await get_stakeholder(loaders, email)
    stakeholder_phone: StakeholderPhone | None = stakeholder.phone
    phone_to_verify = stakeholder_phone if new_phone is None else new_phone

    if not phone_to_verify:
        raise RequiredNewPhoneNumber()

    if (
        stakeholder_phone is not None
        and new_phone is not None
        and get_international_format_phone_number(stakeholder_phone)
        == get_international_format_phone_number(new_phone)
    ):
        raise SamePhoneNumber()

    if new_phone and phone_to_verify is new_phone:
        await verify_operations.validate_mobile(
            phone_number=get_international_format_phone_number(new_phone)
        )

    if phone_to_verify is new_phone and stakeholder_phone is not None:
        if verification_code is None:
            raise RequiredVerificationCode()

        await verify_operations.check_verification(
            recipient=get_international_format_phone_number(stakeholder_phone),
            code=verification_code,
        )

    await verify_operations.start_verification(
        phone_number=get_international_format_phone_number(phone_to_verify),
        channel=Channel.SMS,
    )


async def exists(loaders: Dataloaders, email: str) -> bool:
    if await loaders.stakeholder.load(email):
        return True
    return False
