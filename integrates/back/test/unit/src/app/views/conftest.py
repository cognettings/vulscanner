from authlib.integrations.base_client.errors import (
    MismatchingStateError,
    OAuthError,
)
from custom_exceptions import (
    CredentialAlreadyExists,
    InvalidAuthorization,
)
from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderState,
    StakeholderTours,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import os
import pytest
from starlette.responses import (
    Response,
)
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


def mock_function(  # pylint: disable=unused-argument
    *args: tuple, **kwargs: dict[str, Any]
) -> str:
    return "0J1SkZPT1RiZ0xod"


def mocked_organization(  # pylint: disable=unused-argument
    *args: tuple, **kwargs: dict[str, Any]
) -> Organization:
    return Organization(
        created_by="testing",
        created_date=datetime.now(),
        name="testing",
        policies=Policies(
            modified_date=datetime.now(),
            modified_by="testing",
        ),
        id="1404973626",
        state=OrganizationState(
            modified_by="testing",
            modified_date=datetime.now(),
            status=OrganizationStateStatus.ACTIVE,
        ),
        country="Colombia",
    )


def mocked_jwt_content(  # pylint: disable=unused-argument
    *args: tuple, **kwargs: dict[str, Any]
) -> dict[str, str]:
    return {
        "user_email": "unitest@fluidattacks.com",
        "first_name": "unit",
        "last_name": "test",
    }


MOCKED_DATA: dict[str, dict[str, Any]] = {
    "app.views.auth.Dataloaders.stakeholder": {
        "integratesuser2@fluidattacks.com": Stakeholder(
            email="integratesuser2@fluidattacks.com",
            enrolled=True,
            first_name="Integrates",
            is_concurrent_session=False,
            is_registered=True,
            last_login_date=datetime.fromisoformat(
                "2020-12-31T18:40:37+00:00"
            ),
            last_name="Internal Manager",
            legal_remember=True,
            phone=None,
            registration_date=datetime.fromisoformat(
                "2018-02-28T16:54:12+00:00"
            ),
            role="user",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by=None,
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    available=[],
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("3.0")
                    ),
                ),
            ),
            tours=StakeholderTours(
                new_group=False,
                new_root=False,
                new_risk_exposure=False,
                welcome=False,
            ),
        )
    },
    "app.views.auth.stakeholders_domain.update_last_login": {
        "integratesuser2@fluidattacks.com": None,
    },
    "app.views.auth.utils.send_autoenroll_mixpanel_event": {
        "integratesuser2@fluidattacks.com": None,
    },
    "app.views.evidence.sessions_domain.get_jwt_content": {
        "user": {"user_email": "unitest@fluidattacks.com"},
        "organization": {"user_email": "unitest@fluidattacks.com"},
        "error_in_enforcer_group_level_role": {
            "user_email": "unitest@fluidattacks.com"
        },
        "wrong_evidence_type": {"user_email": "unitest@fluidattacks.com"},
        "file_id_is_none": {"user_email": "unitest@fluidattacks.com"},
        "no_evidences": {"user_email": "unitest@fluidattacks.com"},
        "happy_path": {"user_email": "unitest@fluidattacks.com"},
        "Invalid Authorization": InvalidAuthorization(),
        "test_enforce_group_level_role_catches_invalid_authorization": (
            InvalidAuthorization()
        ),
    },
    "app.views.evidence.authz.get_group_level_role": {
        "user": "invalid role",
        "organization": "user_manager",
    },
    "app.views.evidence.request": {
        "error_in_enforcer_group_level_role": {
            "group_name": "test",
            "finding_id": "463558592",
            "file_id": "1558048727999",
            "evidence_type": "findings",
        },
        "wrong_evidence_type": {
            "group_name": "test",
            "finding_id": "463558592",
            "file_id": "1558048727999",
            "evidence_type": "wrong_evidence_type",
        },
        "file_id_is_none": {
            "group_name": "test",
            "finding_id": "463558592",
            "file_id": None,
            "evidence_type": "findings",
        },
        "no_evidences": {
            "group_name": "test",
            "finding_id": "463558592",
            "file_id": "1558048727999",
            "evidence_type": "findings",
        },
        "happy_path": {
            "group_name": "test",
            "finding_id": "463558592",
            "file_id": "1558048727999",
            "evidence_type": "findings",
        },
    },
    "app.views.evidence.enforce_group_level_role": {
        "error_in_enforcer_group_level_role": Response(
            "Access denied", status_code=403
        ),
        "happy_path": None,
        "wrong_evidence_type": None,
        "file_id_is_none": None,
        "no_evidences": None,
    },
    "app.views.evidence.has_access_to_finding": {
        "happy_path": True,
        "error_in_enforcer_group_level_role": True,
        "wrong_evidence_type": True,
        "file_id_is_none": True,
        "no_evidences": True,
    },
    "app.views.evidence.list_s3_evidences": {
        "happy_path": [
            '"Key": test/463558592/1558048727999.png',
        ],
        "error_in_enforcer_group_level_role": [
            '"Key": test/463558592/1558048727999.png',
        ],
        "file_id_is_none": [
            '"Key": test/463558592/1558048727999.png',
        ],
        "wrong_evidence_type": [
            '"Key": test/463558592/1558048727999.png',
        ],
        "no_evidences": [],
    },
    "app.views.evidence.download_evidence_file": {
        "happy_path": None,
    },
    "app.views.evidence.utils.replace_all": {
        "happy_path": os.path.join(
            os.path.join(os.path.dirname(os.path.abspath(__file__))),
            "mock/resources/evidence-test-file.png",
        ),
    },
    "app.views.auth.OAUTH.azure.authorize_access_token": {
        "MismatchingStateError": MismatchingStateError(),
        "OAuthError": OAuthError(),
        "test_authz_azure": "mock_token",
    },
    "app.views.auth.utils.get_jwt_userinfo": {
        "test_authz_azure": {
            "email": "testing@fluidattacks.com",
            "name": "Test User",
        },
        "test_authz_google": {
            "email": "test@fluidattacks.com",
        },
    },
    "app.views.auth.OAUTH.bitbucket.authorize_access_token": {
        "MismatchingStateError": MismatchingStateError(),
        "OAuthErrorBaseClientError": OAuthError(),
        "test_authz_bitbucket": "mock_token",
        "test_authz_bitbucket_invalid_authorization_error": "mock_token",
    },
    "app.views.auth.handle_user": {
        "test_authz_azure": None,
        "test_authz_bitbucket": None,
        "test_authz_google": None,
        "test_authz_bitbucket_invalid_authorization_error": (
            InvalidAuthorization()
        ),
    },
    "app.views.auth.utils.get_bitbucket_oauth_userinfo": {
        "test_authz_bitbucket": {
            "email": "test@fluidattacks.com",
            "given_name": "unit",
            "family_name": "test",
        },
        "test_authz_bitbucket_invalid_authorization_error": {
            "email": "test",
            "given_name": "unit",
            "family_name": "test",
        },
    },
    "app.views.auth.OAUTH.google.authorize_access_token": {
        "MismatchingStateError": MismatchingStateError(),
        "OAuthErrorBaseClientError": OAuthError(),
        "test_authz_google": "mock_token",
    },
    "app.views.charts.sessions_domain.get_jwt_content": {
        "test_graphics_for_entity": {
            "user_email": "unitest@fluidattacks.com",
            "first_name": "unit",
            "last_name": "test",
        },
    },
    "app.views.charts.sessions_domain.create_session_token": {
        "test_graphics_for_entity": "0J1SkZPT1RiZ0xodUxtdk0iLCJlbmNyeXB0ZWRfa2"
    },
    "app.views.oauth._get_azure_secret": {
        # a function is used because the mock is set with side_effect
        "no_code_in_query_params": mock_function,
        "error_when_validating_credentials": mock_function,
        "no_subject_in_query_params": mock_function,
        "error_when_awaiting_get_secret": OAuthError(),
        "credentials_already_exist": mock_function,
    },
    "app.views.oauth._get_organization_id": {
        "no_subject_in_query_params": KeyError(),
        "no_code_in_query_params": mock_function,
        "error_when_validating_credentials": mock_function,
        "error_when_awaiting_get_secret": mock_function,
        "credentials_already_exist": mock_function,
    },
    "app.views.oauth.get_organization": {
        "no_subject_in_query_params": mocked_organization,
        "no_code_in_query_params": mocked_organization,
        "error_when_validating_credentials": mocked_organization,
        "error_when_awaiting_get_secret": mocked_organization,
        "credentials_already_exist": mocked_organization,
    },
    "app.views.oauth._get_fast_track_org": {
        "test_get_organization_id": mocked_organization,
    },
    "app.views.oauth.get_jwt_content": {
        "test_get_fast_track_org": {
            "user_email": "unitest@fluidattacks.com",
            "first_name": "unit",
            "last_name": "test",
        },
        "test_begin_repo_oauth": mocked_jwt_content,
        "PermissionError": mocked_jwt_content,
        "CredentialAlreadyExists": mocked_jwt_content,
    },
    "app.views.oauth.groups_domain.add_group": {
        "test_get_fast_track_org": None,
    },
    "app.views.oauth.stakeholders_domain.add_enrollment": {
        "test_get_fast_track_org": None,
    },
    "app.views.oauth.orgs_domain.add_organization": {
        "test_get_fast_track_org": Organization(
            created_by="unitest@fluidattacks.com",
            created_date=datetime(2020, 12, 31, 18, 40, 37),
            id="ORG#a19232d7-d843-4c5f-9e60-82e121a982da",
            name="unitfluidattacks",
            policies=Policies(
                modified_date=datetime(2020, 12, 31, 18, 40, 37),
                modified_by="unitest@fluidattacks.com",
                inactivity_period=90,
                max_acceptance_days=None,
                max_acceptance_severity=Decimal("10.0"),
                max_number_acceptances=None,
                min_acceptance_severity=Decimal("0.0"),
                min_breaking_severity=None,
                vulnerability_grace_period=None,
            ),
            state=OrganizationState(
                status=OrganizationStateStatus.ACTIVE,
                modified_by="unitest@fluidattacks.com",
                modified_date=datetime(2020, 12, 31, 18, 40, 37),
                pending_deletion_date=None,
            ),
            country="CO",
            payment_methods=None,
            billing_customer=None,
            vulnerabilities_url=None,
        )
    },
    "app.views.oauth.get_authorized_redirect": {
        "test_begin_repo_oauth": None,
        "PermissionError": None,
        "CredentialAlreadyExists": None,
    },
    "app.views.oauth._validate": {
        "test_begin_repo_oauth": None,
        "PermissionError": PermissionError(),
        "CredentialAlreadyExists": None,
    },
    "app.views.oauth.validate_credentials_oauth": {
        "test_begin_repo_oauth": None,
        "PermissionError": None,
        "CredentialAlreadyExists": CredentialAlreadyExists(),
    },
}


@pytest.fixture(scope="session")
def mocked_data_for_module() -> dict[str, dict[str, Any]]:
    return MOCKED_DATA
