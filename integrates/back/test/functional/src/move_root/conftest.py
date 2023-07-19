# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.enums import (
    EventSolutionReason,
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventState,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    RootEnvironmentUrl,
    Secret,
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
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityUnreliableIndicators,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("move_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate() -> bool:
    test_email = "admin@gmail.com"
    data = {
        "policies": (
            {
                "level": "user",
                "subject": "test@fluidattacks.com",
                "object": "self",
                "role": "admin",
            },
        ),
        "stakeholders": [
            Stakeholder(
                email="test@fluidattacks.com",
                first_name="",
                last_name="",
                phone=StakeholderPhone(
                    calling_country_code="1",
                    country_code="US",
                    national_number="1111111111",
                ),
                legal_remember=False,
                is_registered=True,
            ),
        ],
        "organizations": (
            {
                "organization": Organization(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="wano",
                    policies=Policies(
                        modified_by="test@fluidattacks.com",
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                    name="zou",
                    policies=Policies(
                        modified_by="test@fluidattacks.com",
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ),
        "organization_access": [
            OrganizationAccess(
                organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                email="test@fluidattacks.com",
            ),
            OrganizationAccess(
                organization_id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                email="test@fluidattacks.com",
            ),
        ],
        "groups": (
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="kibi",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
                "environment_secrets": {
                    "https://test-active.com": (
                        Secret(
                            key="Key1",
                            value="Value1",
                            description="description test",
                            created_at=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                        ),
                        Secret(
                            key="Key2",
                            value="Value2",
                            description="description test",
                            created_at=datetime.fromisoformat(
                                "2020-05-20T22:00:00+00:00"
                            ),
                        ),
                    )
                },
            },
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="kuri",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
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
                    name="udon",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
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
                    name="kurau",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                ),
            },
        ),
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="kibi",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="wano",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="test",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/test",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
                "git_environment_urls": [
                    RootEnvironmentUrl(
                        url="https://test-active.com",
                        id="5a0da7cb4056b4d383f682e7afe55f20a1479f91",
                        group_name="kibi",
                    )
                ],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="kibi",
                    id="8a62109b-316a-4a88-a1f1-767b80383864",
                    organization_name="wano",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="inactive",
                        other="",
                        reason="",
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/inactive",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
                "git_environment_urls": [
                    RootEnvironmentUrl(
                        url="https://test-inactive.com",
                        id="017bceab-1e61-4f2f-8076-3a106bfad6f4",
                        group_name="kibi",
                    )
                ],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="kibi",
                    id="44db9bee-c97d-4161-98c6-f124d7dc9a41",
                    organization_name="wano",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
        ],
        "findings": (
            {
                "finding": Finding(
                    id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="kibi",
                    severity_score=SeverityScore(),
                    state=FindingState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection",
                    hacker_email="test@fluidattacks.com",
                ),
                "historic_state": [],
                "historic_verification": [],
            },
        ),
        "vulnerabilities": (
            {
                "vulnerability": Vulnerability(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="kibi",
                    organization_name="orgtest",
                    hacker_email="test@fluidattacks.com",
                    id="64bf8e56-0b3c-432a-bff7-c3eef56c47b7",
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    state=VulnerabilityState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                    ),
                ),
            },
        ),
        "events": [
            {
                "event": Event(
                    id="418900971",
                    group_name="kibi",
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="Unsolved",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name="kibi_418900971_evidence_image_1.png",
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name="kibi_418900971_evidence_file_1.csv",
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
                "historic_state": [
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900972",
                    group_name="kibi",
                    hacker="unittest@fluidattacks.com",
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="Solved",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name="kibi_418900972_evidence_image_1.png",
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name="kibi_418900972_evidence_file_1.csv",
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
                "historic_state": [
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                    EventState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:41:05+00:00"
                        ),
                        status=EventStateStatus.SOLVED,
                        reason=EventSolutionReason.ACCESS_GRANTED,
                    ),
                ],
            },
        ],
        "event_comments": [
            {
                "event_comment": EventComment(
                    event_id="418900971",
                    id="43455343453",
                    group_name="kibi",
                    content="This is a test comment",
                    creation_date=datetime.fromisoformat(
                        "2019-05-28T20:09:37+00:00"
                    ),
                    email="admin@gmail.com",
                    full_name="test one",
                    parent_id="0",
                )
            },
            {
                "event_comment": EventComment(
                    event_id="418900972",
                    id="43455343453",
                    group_name="kibi",
                    content="This is a test comment",
                    creation_date=datetime.fromisoformat(
                        "2019-05-28T20:09:37+00:00"
                    ),
                    email="admin@gmail.com",
                    full_name="test one",
                    parent_id="0",
                )
            },
        ],
    }
    return await db.populate(data)
