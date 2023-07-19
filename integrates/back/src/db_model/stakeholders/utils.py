from ..enums import (
    Notification,
)
from .types import (
    AccessTokens,
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderSessionToken,
    StakeholderState,
    StakeholderTours,
    StateSessionType,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    serialize,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


def format_access_tokens(items: list[Item]) -> list[AccessTokens]:
    return [
        AccessTokens(
            id=item["id"],
            issued_at=int(item["issued_at"]),
            jti_hashed=item["jti_hashed"],
            salt=item["salt"],
            name=item.get("name", "Token"),
            last_use=datetime.fromisoformat(item["last_use"])
            if item.get("last_use")
            else None,
        )
        for item in items
    ]


def format_session_token(item: Item) -> StakeholderSessionToken:
    return StakeholderSessionToken(
        jti=item["jti"],
        state=StateSessionType[item["state"]],
    )


def format_metadata_item(metadata: StakeholderMetadataToUpdate) -> Item:
    item: Item = {
        **json.loads(json.dumps(metadata, default=serialize)),
    }

    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }


def format_notifications_preferences(
    item: Item | None,
) -> NotificationsPreferences:
    if not item:
        return NotificationsPreferences(
            email=[], sms=[], parameters=NotificationsParameters()
        )
    email_preferences: list[str] = []
    sms_preferences: list[str] = []
    parameters_preferences = NotificationsParameters()
    if "email" in item:
        email_preferences = [
            item for item in item["email"] if item in Notification.__members__
        ]
    if "sms" in item:
        sms_preferences = [
            item for item in item["sms"] if item in Notification.__members__
        ]
    if "parameters" in item:
        parameters_preferences = NotificationsParameters(
            **{
                field: Decimal(item["parameters"][field])
                for field in NotificationsParameters._fields
            }
        )
    return NotificationsPreferences(
        email=email_preferences,
        sms=sms_preferences,
        parameters=parameters_preferences,
    )


def format_state(item: Item | None) -> StakeholderState:
    if item:
        return StakeholderState(
            modified_by=item["modified_by"],
            modified_date=datetime.fromisoformat(item["modified_date"]),
            notifications_preferences=format_notifications_preferences(
                item.get("notifications_preferences")
            ),
        )

    return StakeholderState(
        modified_by=None,
        modified_date=None,
        notifications_preferences=format_notifications_preferences(item),
    )


def format_phone(item: Item) -> StakeholderPhone:
    return StakeholderPhone(
        calling_country_code=item["calling_country_code"],
        country_code=item["country_code"],
        national_number=item["national_number"],
    )


def format_tours(item: Item) -> StakeholderTours:
    return StakeholderTours(
        new_group=bool(item["new_group"]),
        new_root=bool(item["new_root"]),
        new_risk_exposure=bool(item["new_risk_exposure"]),
        welcome=bool(item["welcome"]),
    )


def format_stakeholder(item: Item) -> Stakeholder:
    email: str = item.get("email") or str(item["pk"]).split("#")[1]
    return Stakeholder(
        access_tokens=format_access_tokens(item["access_tokens"])
        if item.get("access_tokens")
        else [],
        email=email.lower().strip(),
        enrolled=item.get("enrolled", False),
        first_name=item.get("first_name"),
        is_concurrent_session=item.get("is_concurrent_session", False),
        is_registered=item.get("is_registered", False),
        last_login_date=datetime.fromisoformat(item["last_login_date"])
        if item.get("last_login_date")
        else None,
        last_name=item.get("last_name"),
        legal_remember=item.get("legal_remember", False),
        phone=format_phone(item["phone"]) if item.get("phone") else None,
        state=format_state(item.get("state")),
        registration_date=datetime.fromisoformat(item["registration_date"])
        if item.get("registration_date")
        else None,
        role=item.get("role"),
        session_key=item.get("session_key"),
        session_token=format_session_token(item["session_token"])
        if item.get("session_token")
        else None,
        tours=format_tours(item["tours"])
        if item.get("tours")
        else StakeholderTours(),
    )
