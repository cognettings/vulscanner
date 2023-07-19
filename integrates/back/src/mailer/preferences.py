from collections.abc import (
    Iterable,
)
from custom_utils import (
    datetime as datetime_utils,
)
from db_model.enums import (
    Notification,
)
from typing import (
    NamedTuple,
)


class PreferenceRole(NamedTuple):
    group: Iterable[str]
    org: Iterable[str]


class NotificationPreferences(NamedTuple):
    email_preferences: Notification | None
    exclude_trial: bool
    only_fluid_staff: bool
    roles: PreferenceRole


MAIL_PREFERENCES: dict[str, NotificationPreferences] = dict(
    abandoned_trial=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    access_granted=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    add_members=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    add_repositories=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    confirm_deletion=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    consulting_digest=NotificationPreferences(
        email_preferences=Notification.NEW_COMMENT,
        exclude_trial=False,
        only_fluid_staff=datetime_utils.get_now().hour > 12,
        roles=PreferenceRole(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    contact_sales=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    credit_card_added=NotificationPreferences(
        email_preferences=None,
        exclude_trial=False,
        only_fluid_staff=True,
        roles=PreferenceRole(group={}, org={}),
    ),
    define_treatments=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    delete_finding=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    deprecation_notice=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    devsecops_agent=NotificationPreferences(
        email_preferences=Notification.AGENT_TOKEN,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={"user_manager"}, org={}),
    ),
    devsecops_agent_token=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    environment_report=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    event_report=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    events_digest=NotificationPreferences(
        email_preferences=Notification.EVENT_REPORT,
        exclude_trial=False,
        only_fluid_staff=True,
        roles=PreferenceRole(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    file_report=NotificationPreferences(
        email_preferences=Notification.FILE_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={
                "customer_manager",
                "hacker",
                "resourcer",
                "user_manager",
            },
            org={},
        ),
    ),
    free_trial=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    free_trial_over=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    group_alert=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "user_manager"}, org={}
        ),
    ),
    group_report=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    how_improve=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    missing_environment=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    new_comment=NotificationPreferences(
        email_preferences=Notification.NEW_COMMENT,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    new_enrolled=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    newsletter=NotificationPreferences(
        email_preferences=None,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    numerator_digest=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    portfolio_report=NotificationPreferences(
        email_preferences=Notification.PORTFOLIO_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    remediate_finding=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    reminder=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    reviewer_progress_report=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=True,
        roles=PreferenceRole(group={}, org={}),
    ),
    root_added=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_cloning_status=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_credential_report=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    root_deactivated=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    root_moved=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "user_manager"}, org={}
        ),
    ),
    support_channels=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    treatment_report=NotificationPreferences(
        email_preferences=Notification.UPDATED_TREATMENT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={
                "customer_manager",
                "resourcer",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    trial_corporate_email=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    trial_ended=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    trial_ending=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    trial_first_scanning=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    trial_reports=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    trial_repository=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    updated_credentials_owner=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={}, org={"customer_manager", "user_manager"}
        ),
    ),
    updated_group_info=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_policies=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    updated_root=NotificationPreferences(
        email_preferences=Notification.ROOT_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_services=NotificationPreferences(
        email_preferences=Notification.SERVICE_UPDATE,
        exclude_trial=True,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    updated_treatment=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    upgrade_squad=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    user_unsubscribed=NotificationPreferences(
        email_preferences=Notification.UNSUBSCRIPTION_ALERT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={"customer_manager", "resourcer", "user_manager"}, org={}
        ),
    ),
    users_weekly_report=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    vulnerabilities_expiring=NotificationPreferences(
        email_preferences=Notification.UPDATED_TREATMENT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={
                "customer_manager",
                "resourcer",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    vulnerability_assigned=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(group={}, org={}),
    ),
    vulnerability_rejection=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=True,
        roles=PreferenceRole(group={}, org={}),
    ),
    vulnerability_report=NotificationPreferences(
        email_preferences=Notification.VULNERABILITY_REPORT,
        exclude_trial=False,
        only_fluid_staff=False,
        roles=PreferenceRole(
            group={
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user_manager",
                "vulnerability_manager",
            },
            org={},
        ),
    ),
    vulnerability_submission=NotificationPreferences(
        email_preferences=Notification.GROUP_INFORMATION,
        exclude_trial=True,
        only_fluid_staff=True,
        roles=PreferenceRole(group={}, org={}),
    ),
)
