# pylint:disable=too-many-lines
import asyncio
from asyncio import (
    AbstractEventLoop,
)
from collections.abc import (
    AsyncGenerator,
    Generator,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    CVSS31Severity,
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
)
from db_model.types import (
    Policies,
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators as VulUnreliableInd,
)
from decimal import (
    Decimal,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import os
import pytest
from typing import (
    Any,
)

# Constants
PATH = os.path.dirname(os.path.abspath(__file__))
TEST_GROUPS = {
    directory
    for directory in os.listdir(PATH)
    if os.path.isdir(os.path.join(PATH, directory))
    and not directory.startswith("__")
}


@pytest.fixture(autouse=True, scope="session")
def generic_data(  # pylint: disable=too-many-locals
    dynamo_resource: bool,  # pylint: disable=redefined-outer-name
) -> dict[str, Any]:
    assert dynamo_resource
    admin_email: str = "admin@gmail.com"
    admin_fluid_email: str = "admin@fluidattacks.com"
    architect_email: str = "architect@gmail.com"
    architect_fluid_email: str = "architect@fluidattacks.com"
    customer_manager_fluid_email: str = "customer_manager@fluidattacks.com"
    hacker_email: str = "hacker@gmail.com"
    hacker_fluid_email: str = "hacker@fluidattacks.com"
    reattacker_email: str = "reattacker@gmail.com"
    reattacker_fluid_email: str = "reattacker@fluidattacks.com"
    resourcer_email: str = "resourcer@gmail.com"
    resourcer_fluid_email: str = "resourcer@fluidattacks.com"
    reviewer_email: str = "reviewer@gmail.com"
    reviewer_fluid_email: str = "reviewer@fluidattacks.com"
    service_forces_email: str = "service_forces@gmail.com"
    service_forces_fluid_email: str = "service_forces@fluidattacks.com"
    user_email: str = "user@gmail.com"
    user_fluid_email: str = "user@fluidattacks.com"
    user_manager_email: str = "user_manager@gmail.com"
    user_manager_fluid_email: str = "user_manager@fluidattacks.com"
    vuln_manager_email: str = "vulnerability_manager@gmail.com"
    vuln_manager_fluid_email: str = "vulnerability_manager@fluidattacks.com"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    return {
        "global_vars": {
            "admin_email": admin_email,
            "admin_fluid_email": admin_fluid_email,
            "architect_email": architect_email,
            "architect_fluid_email": architect_fluid_email,
            "customer_manager_fluid_email": customer_manager_fluid_email,
            "hacker_email": hacker_email,
            "hacker_fluid_email": hacker_fluid_email,
            "reattacker_email": reattacker_email,
            "reattacker_fluid_email": reattacker_fluid_email,
            "resourcer_email": resourcer_email,
            "resourcer_fluid_email": resourcer_fluid_email,
            "reviewer_email": reviewer_email,
            "reviewer_fluid_email": reviewer_fluid_email,
            "service_forces_email": service_forces_email,
            "service_forces_fluid_email": service_forces_fluid_email,
            "user_email": user_email,
            "user_fluid_email": user_fluid_email,
            "user_manager_email": user_manager_email,
            "user_manager_fluid_email": user_manager_fluid_email,
            "vulnerability_manager_email": vuln_manager_email,
            "vulnerability_manager_fluid_email": vuln_manager_fluid_email,
            "FIN.H.060": (
                "060. Insecure service configuration - Host verification"
            ),
            "R359": "R359. Avoid using generic exceptions.",
        },
        "db_data": {
            "stakeholders": [
                Stakeholder(
                    email=admin_email,
                    enrolled=True,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        country_code="US",
                        calling_country_code="1",
                        national_number="1111111111",
                    ),
                ),
                Stakeholder(
                    email=admin_fluid_email,
                    enrolled=True,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="22222222222",
                    ),
                ),
                Stakeholder(
                    email=architect_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="33333333333",
                    ),
                ),
                Stakeholder(
                    email=architect_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="4444444444444",
                    ),
                ),
                Stakeholder(
                    email=user_email,
                    enrolled=True,
                    first_name="",
                    last_name="",
                    registration_date=None,
                    last_login_date=None,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="2029182132",
                    ),
                ),
                Stakeholder(
                    email=user_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="666666666666",
                    ),
                ),
                Stakeholder(
                    email=user_manager_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="77777777777777",
                    ),
                ),
                Stakeholder(
                    email=user_manager_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="88888888888",
                    ),
                ),
                Stakeholder(
                    email=hacker_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="2029182131",
                    ),
                ),
                Stakeholder(
                    email=hacker_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="222222222222",
                    ),
                ),
                Stakeholder(
                    email=resourcer_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="33333333333",
                    ),
                ),
                Stakeholder(
                    email=reattacker_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="4444444444444",
                    ),
                ),
                Stakeholder(
                    email=reattacker_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="55555555555",
                    ),
                ),
                Stakeholder(
                    email=resourcer_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="66666666666",
                    ),
                ),
                Stakeholder(
                    email=reviewer_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="7777777777",
                    ),
                ),
                Stakeholder(
                    email=reviewer_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="8888888888",
                    ),
                ),
                Stakeholder(
                    email=service_forces_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                ),
                Stakeholder(
                    email=service_forces_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                ),
                Stakeholder(
                    email=customer_manager_fluid_email,
                    enrolled=True,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="9999999999999",
                    ),
                ),
                Stakeholder(
                    email=vuln_manager_email,
                    enrolled=False,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="51",
                        country_code="PE",
                        national_number="1111111111111",
                    ),
                ),
                Stakeholder(
                    email=vuln_manager_fluid_email,
                    legal_remember=False,
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="51",
                        country_code="PE",
                        national_number="222222222222",
                    ),
                ),
            ],
            "organizations": [
                {
                    "organization": Organization(
                        created_by=admin_email,
                        created_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        country="Colombia",
                        id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        name="orgtest",
                        policies=Policies(
                            modified_by=admin_email,
                            max_acceptance_days=7,
                            modified_date=datetime.fromisoformat(
                                "2019-11-22T20:07:57+00:00"
                            ),
                            vulnerability_grace_period=5,
                        ),
                        state=OrganizationState(
                            modified_by=admin_email,
                            modified_date=datetime.fromisoformat(
                                "2019-11-22T20:07:57+00:00"
                            ),
                            status=OrganizationStateStatus.ACTIVE,
                        ),
                    ),
                },
            ],
            "organization_access": [
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=admin_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=admin_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=architect_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=architect_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=hacker_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=hacker_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reattacker_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reattacker_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_manager_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_manager_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=resourcer_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=resourcer_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reviewer_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reviewer_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=service_forces_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=service_forces_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=customer_manager_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=vuln_manager_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=vuln_manager_fluid_email,
                ),
            ],
            "groups": [
                {
                    "group": Group(
                        created_by="unknown",
                        created_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        description="-",
                        language=GroupLanguage.EN,
                        name="group1",
                        state=GroupState(
                            has_machine=False,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                            service=GroupService.WHITE,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.CONTINUOUS,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date=datetime.fromisoformat(
                            "2022-06-06T00:00:00+00:00"
                        ),
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        description="-",
                        language=GroupLanguage.EN,
                        name="unittesting",
                        state=GroupState(
                            has_machine=True,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                            service=GroupService.WHITE,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.CONTINUOUS,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date=datetime.fromisoformat(
                            "2022-06-06T00:00:00+00:00"
                        ),
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        description="-",
                        language=GroupLanguage.EN,
                        name="group2",
                        state=GroupState(
                            has_machine=False,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                            service=GroupService.BLACK,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.ONESHOT,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date=datetime.fromisoformat(
                            "2022-06-06T00:00:00+00:00"
                        ),
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        description="-",
                        language=GroupLanguage.EN,
                        name="group3",
                        state=GroupState(
                            has_machine=False,
                            has_squad=False,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                            service=GroupService.BLACK,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.ONESHOT,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date=datetime.fromisoformat(
                            "2022-06-06T00:00:00+00:00"
                        ),
                    ),
                },
            ],
            "policies": [
                {
                    "level": "user",
                    "subject": admin_email,
                    "object": "self",
                    "role": "admin",
                },
                {
                    "level": "user",
                    "subject": admin_fluid_email,
                    "object": "self",
                    "role": "admin",
                },
                {
                    "level": "user",
                    "subject": architect_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": architect_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": hacker_email,
                    "object": "self",
                    "role": "hacker",
                },
                {
                    "level": "user",
                    "subject": hacker_fluid_email,
                    "object": "self",
                    "role": "hacker",
                },
                {
                    "level": "user",
                    "subject": reattacker_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reattacker_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_manager_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": resourcer_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": resourcer_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reviewer_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reviewer_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": service_forces_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": customer_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": vuln_manager_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": vuln_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": architect_email,
                    "object": "group1",
                    "role": "architect",
                },
                {
                    "level": "group",
                    "subject": architect_fluid_email,
                    "object": "group1",
                    "role": "architect",
                },
                {
                    "level": "group",
                    "subject": hacker_email,
                    "object": "group1",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": hacker_email,
                    "object": "group3",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": hacker_fluid_email,
                    "object": "group1",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": reattacker_email,
                    "object": "group1",
                    "role": "reattacker",
                },
                {
                    "level": "group",
                    "subject": reviewer_email,
                    "object": "group3",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": reattacker_fluid_email,
                    "object": "group1",
                    "role": "reattacker",
                },
                {
                    "level": "group",
                    "subject": user_email,
                    "object": "group1",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": user_fluid_email,
                    "object": "group1",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": user_manager_email,
                    "object": "group1",
                    "role": "user_manager",
                },
                {
                    "level": "group",
                    "subject": user_manager_fluid_email,
                    "object": "group1",
                    "role": "user_manager",
                },
                {
                    "level": "group",
                    "subject": vuln_manager_email,
                    "object": "group1",
                    "role": "vulnerability_manager",
                },
                {
                    "level": "group",
                    "subject": vuln_manager_fluid_email,
                    "object": "group1",
                    "role": "vulnerability_manager",
                },
                {
                    "level": "group",
                    "subject": resourcer_email,
                    "object": "group1",
                    "role": "resourcer",
                },
                {
                    "level": "group",
                    "subject": resourcer_fluid_email,
                    "object": "group1",
                    "role": "resourcer",
                },
                {
                    "level": "group",
                    "subject": reviewer_email,
                    "object": "group1",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": reviewer_fluid_email,
                    "object": "group1",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": service_forces_email,
                    "object": "group1",
                    "role": "service_forces",
                },
                {
                    "level": "group",
                    "subject": service_forces_fluid_email,
                    "object": "group1",
                    "role": "service_forces",
                },
                {
                    "level": "group",
                    "subject": customer_manager_fluid_email,
                    "object": "group1",
                    "role": "customer_manager",
                },
                {
                    "level": "organization",
                    "subject": admin_email,
                    "object": org_id,
                    "role": "admin",
                },
                {
                    "level": "organization",
                    "subject": admin_fluid_email,
                    "object": org_id,
                    "role": "admin",
                },
                {
                    "level": "organization",
                    "subject": architect_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": architect_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": hacker_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": hacker_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reattacker_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reattacker_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_manager_email,
                    "object": org_id,
                    "role": "user_manager",
                },
                {
                    "level": "organization",
                    "subject": user_manager_fluid_email,
                    "object": org_id,
                    "role": "user_manager",
                },
                {
                    "level": "organization",
                    "subject": vuln_manager_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": vuln_manager_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": resourcer_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": resourcer_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reviewer_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reviewer_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": service_forces_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": customer_manager_fluid_email,
                    "object": org_id,
                    "role": "customer_manager",
                },
            ],
            "findings": [
                {
                    "finding": Finding(
                        id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        state=FindingState(
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2017-04-08T00:45:11+00:00"
                            ),
                            source=Source.ASM,
                            status=FindingStateStatus.CREATED,
                        ),
                        title="001. SQL injection - C Sharp SQL API",
                        recommendation="Updated recommendation",
                        description="I just have updated the description",
                        hacker_email="test1@gmail.com",
                        severity=CVSS31Severity(
                            attack_complexity=Decimal("0.44"),
                            attack_vector=Decimal("0.2"),
                            availability_impact=Decimal("0.22"),
                            availability_requirement=Decimal("1.5"),
                            confidentiality_impact=Decimal("0.22"),
                            confidentiality_requirement=Decimal("0.5"),
                            exploitability=Decimal("0.94"),
                            integrity_impact=Decimal("0.22"),
                            integrity_requirement=Decimal("1"),
                            modified_availability_impact=Decimal("0.22"),
                            modified_user_interaction=Decimal("0.62"),
                            modified_integrity_impact=Decimal("0"),
                            modified_attack_complexity=Decimal("0.44"),
                            modified_severity_scope=Decimal("0"),
                            modified_privileges_required=Decimal("0.27"),
                            modified_attack_vector=Decimal("0.85"),
                            modified_confidentiality_impact=Decimal("0.22"),
                            privileges_required=Decimal("0.62"),
                            severity_scope=Decimal("1.0"),
                            remediation_level=Decimal("0.95"),
                            report_confidence=Decimal("1"),
                            user_interaction=Decimal("0.85"),
                        ),
                        severity_score=SeverityScore(
                            base_score=Decimal("4.5"),
                            temporal_score=Decimal("4.1"),
                            cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/"
                            "I:L/A:L/E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/"
                            "MUI:R/MS:U/MC:L/MA:L",
                            cvssf=Decimal("1.149"),
                        ),
                        requirements=(
                            "REQ.0132. Passwords (phrase type) "
                            "must be at least 3 words long."
                        ),
                        threat="Updated threat",
                        attack_vector_description=(
                            "This is an updated attack vector"
                        ),
                        evidences=FindingEvidences(
                            evidence1=FindingEvidence(
                                description="evidence1",
                                url=(
                                    "group1-3c475384-834c-47b0-ac71-"
                                    "a41a022e401c-evidence1"
                                ),
                                modified_date=datetime.fromisoformat(
                                    "2020-11-19T13:37:10+00:00"
                                ),
                            ),
                            records=FindingEvidence(
                                description="records",
                                url=(
                                    "group1-3c475384-834c-47b0-ac71-"
                                    "a41a022e401c-records"
                                ),
                                modified_date=datetime.fromisoformat(
                                    "2111-11-19T13:37:10+00:00"
                                ),
                            ),
                        ),
                    ),
                    "historic_state": [
                        FindingState(
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2017-04-08T00:45:12+00:00"
                            ),
                            source=Source.ASM,
                            status=FindingStateStatus.SUBMITTED,
                        ),
                        FindingState(
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2017-04-08T00:45:13+00:00"
                            ),
                            source=Source.ASM,
                            status=FindingStateStatus.REJECTED,
                        ),
                        FindingState(
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2017-04-08T00:45:14+00:00"
                            ),
                            source=Source.ASM,
                            status=FindingStateStatus.SUBMITTED,
                        ),
                        FindingState(
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            status=FindingStateStatus.APPROVED,
                        ),
                    ],
                    "historic_verification": [
                        FindingVerification(
                            comment_id="42343434",
                            modified_by="test1@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2020-01-01T00:45:12+00:00"
                            ),
                            status=FindingVerificationStatus.REQUESTED,
                            vulnerability_ids={
                                "be09edb7-cd5c-47ed-bee4-97c645acdce10",
                            },
                        )
                    ],
                    "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(  # noqa: E501 pylint: disable=line-too-long
                        unreliable_closed_vulnerabilities=3,
                        unreliable_open_vulnerabilities=5,
                        unreliable_newest_vulnerability_report_date=(
                            datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                        ),
                        unreliable_oldest_open_vulnerability_report_date=(
                            datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                        ),
                        unreliable_oldest_vulnerability_report_date=(
                            datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                        ),
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_where="192.168.1.2",
                    ),
                },
            ],
            "vulnerabilities": [
                {
                    "vulnerability": Vulnerability(
                        created_by="hacker@gmail.com",
                        created_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        organization_name="orgtest",
                        hacker_email="hacker@gmail.com",
                        id="be09edb7-cd5c-47ed-bee4-97c645acdce10",
                        state=VulnerabilityState(
                            modified_by="hacker@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="9999",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.20",
                        ),
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:11+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                            assigned=user_email,
                        ),
                        type=VulnerabilityType.PORTS,
                        unreliable_indicators=VulUnreliableInd(
                            unreliable_report_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            unreliable_source=Source.ASM,
                            unreliable_treatment_changes=0,
                        ),
                    ),
                },
                {
                    "vulnerability": Vulnerability(
                        created_by="hacker@gmail.com",
                        created_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        organization_name="orgtest",
                        hacker_email="hacker@gmail.com",
                        id="be09edb7-cd5c-47ed-bee4-97c645acdce11",
                        state=VulnerabilityState(
                            modified_by="hacker@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="9999",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.20",
                        ),
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:11+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                            assigned=vuln_manager_email,
                        ),
                        type=VulnerabilityType.PORTS,
                        unreliable_indicators=VulUnreliableInd(
                            unreliable_report_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            unreliable_source=Source.ASM,
                            unreliable_treatment_changes=0,
                        ),
                    ),
                },
                {
                    "vulnerability": Vulnerability(
                        created_by="hacker@gmail.com",
                        created_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        organization_name="orgtest",
                        hacker_email="hacker@gmail.com",
                        id="be09edb7-cd5c-47ed-bee4-97c645acdce12",
                        state=VulnerabilityState(
                            modified_by="hacker@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="9999",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.20",
                        ),
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:11+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                            assigned=user_manager_email,
                        ),
                        type=VulnerabilityType.PORTS,
                        unreliable_indicators=VulUnreliableInd(
                            unreliable_report_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            unreliable_source=Source.ASM,
                            unreliable_treatment_changes=0,
                        ),
                    ),
                },
                {
                    "vulnerability": Vulnerability(
                        created_by="hacker@gmail.com",
                        created_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        organization_name="orgtest",
                        hacker_email="hacker@gmail.com",
                        id="be09edb7-cd5c-47ed-bee4-97c645acdce13",
                        state=VulnerabilityState(
                            modified_by="hacker@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="9999",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.20",
                        ),
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:11+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                        ),
                        type=VulnerabilityType.PORTS,
                        unreliable_indicators=VulUnreliableInd(
                            unreliable_report_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            unreliable_source=Source.ASM,
                            unreliable_treatment_changes=0,
                        ),
                    ),
                },
                {
                    "vulnerability": Vulnerability(
                        created_by="hacker@gmail.com",
                        created_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                        group_name="group1",
                        organization_name="orgtest",
                        hacker_email="hacker@gmail.com",
                        id="be09edb7-cd5c-47ed-bee4-97c645acdce14",
                        state=VulnerabilityState(
                            modified_by="hacker@gmail.com",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="9999",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where="192.168.1.20",
                        ),
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:45:11+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.UNTREATED,
                        ),
                        type=VulnerabilityType.PORTS,
                        unreliable_indicators=VulUnreliableInd(
                            unreliable_report_date=datetime.fromisoformat(
                                "2018-04-08T00:45:15+00:00"
                            ),
                            unreliable_source=Source.ASM,
                            unreliable_treatment_changes=0,
                        ),
                    ),
                },
            ],
        },
    }


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def dynamo_resource(
    event_loop: AbstractEventLoop,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator:
    assert event_loop
    await dynamo_startup()
    yield True
    await dynamo_shutdown()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--resolver-test-group",
        action="store",
        metavar="RESOLVER_TEST_GROUP",
    )


def pytest_runtest_setup(item: Any) -> None:
    resolver_test_group = item.config.getoption("--resolver-test-group")

    if not resolver_test_group:
        raise ValueError("resolver-test-group not specified")
    if resolver_test_group not in TEST_GROUPS:
        raise ValueError(
            f"resolver-test-group must be one of: {TEST_GROUPS}",
        )

    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name="resolver_test_group")
    }

    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f"resolver-test-group must be one of: {TEST_GROUPS}")

    if resolver_test_group not in runnable_groups:
        pytest.skip(f"Requires resolver test group in: {runnable_groups}")
