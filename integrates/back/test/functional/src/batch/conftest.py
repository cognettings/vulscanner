# pylint: disable=import-error
from back.test import (
    db,
)
from collections.abc import (
    Iterator,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesState,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
from git.repo import (
    Repo,
)
import os
import pytest
import pytest_asyncio
from shutil import (
    rmtree,
)
import tempfile
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("batch")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "credentials": (
            Credentials(
                id="3912827d-2b35-4e08-bd35-1bb24457951d",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key="VGVzdCBTU0gK"),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key="VGVzdCBTU0gK"),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="4a5dacda-1d52-365c-5158-f6fd5dfe0999",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key="VGVzdCBTU0gK"),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="5a6dacda-2d63-76c-6269-f6fd6dfe1000",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(
                        key=os.environ["TEST_GITHUB_SSH_PRIVATE_KEY"]
                    ),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="6a7dacda-3d64-87c-7370-f7fd7dfe2111",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.HTTPS,
                    secret=HttpsPatSecret(
                        token=os.environ["TEST_GITHUB_API_TOKEN"]
                    ),
                    is_pat=False,
                ),
            ),
        ),
        "findings": [
            {
                "finding": Finding(
                    id="4c475384-834c-47b0-ac71-a41a066e475f",
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
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L/"
                        "E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/"
                        "MA:L",
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
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "group1-3c475384-834c-47b0"
                                "-ac71-a41a022e401c-evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "group1-3c475384-834c-47b0-"
                                "ac71-a41a022e401c-records"
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
                            "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
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
                    # FP: local testing
                    unreliable_where="192.168.1.2",  # NOSONAR
                ),
            },
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="unittesting",
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
                        cvss_v3="CVSS:3.1/AV:P/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:L/"
                        "E:P/RL:O/CR:L/AR:H/MAV:N/MAC:H/MPR:H/MUI:R/MS:U/MC:L/"
                        "MA:L",
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
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "unittesting-3c475384-834c-47b0"
                                "-ac71-a41a022e401c-evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "unittesting-3c475384-834c-47b0-"
                                "ac71-a41a022e401c-records"
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
                            "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
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
                    # FP: local testing
                    unreliable_where="192.168.1.2",  # NOSONAR
                ),
            },
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.UNKNOWN,
                        commit="6d4519f5d5b4223feb65fcbc5af68e8ef9964b62",
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="3912827d-2b35-4e08-bd35-1bb24457951d",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname1",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.UNKNOWN,
                        commit="6d4519f5d5b4223feb65fcbc5af68e8ef9964b62",
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="unittesting",
                    id="77637717-41d4-4242-854a-db8ff7fe5ed0",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="3912827d-2b35-4e08-bd35-1bb24457951d",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname1",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Failed to clone",
                        status=GitCloningStatus.FAILED,
                        commit="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="2159f8cb-3b55-404b-8fc5-627171f424ax",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="4a5dacda-1d52-365c-5158-f6fd5dfe0999",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname2",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname2",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.FAILED,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="9059f0cb-3b55-404b-8fc5-627171f424ad",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname3",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
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
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="5059f0cb-4b55-404b-3fc5-627171f424af",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname4",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname4",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        credential_id="3912827d-2b35-4e08-bd35-1bb24457951d",
                        environment="production",
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="nickname5",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="6160f0cb-4b66-515b-4fc6-738282f535af",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="main",
                        credential_id="5a6dacda-2d63-76c-6269-f6fd6dfe1000",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname6",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="git@github.com:fluidattacks/test_git_roots.git",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.UNKNOWN,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="7271f1cb-5b77-626b-5fc7-849393f646az",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="main",
                        credential_id="6a7dacda-3d64-87c-7370-f7fd7dfe2111",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname8",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url=(
                            "https://github.com/fluidattacks/"
                            "test_git_roots.git"
                        ),
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-01T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="unittesting",
                    organization_name="okada",
                    hacker_email="test1@gmail.com",
                    id="4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                    state=VulnerabilityState(
                        commit="15ab18899a617e5b18c5c0ad1e7ad7352615d5a3",
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="5",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="README.md",
                    ),
                    hash=8278473475482913498,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="77637717-41d4-4242-854a-db8ff7fe5ed0",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-01T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="unittesting",
                    organization_name="okada",
                    hacker_email="test1@gmail.com",
                    id="4dbc01e0-4cfc-4b77-9b71-bb7566c60bg",
                    state=VulnerabilityState(
                        commit="15ab18899a617e5b18c5c0ad1e7ad7352615d5a3",
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="3",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="README.md",
                    ),
                    hash=17495626552588794164,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="77637717-41d4-4242-854a-db8ff7fe5ed0",
                ),
            },
        ],
        "toe_lines": (
            ToeLines(
                filename="README.md",
                group_name="unittesting",
                root_id="77637717-41d4-4242-854a-db8ff7fe5ed0",
                state=ToeLinesState(
                    attacked_at=None,
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=5,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=None,
                    loc=10,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-09-05T00:45:11+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer1@gmail.com",
                    last_commit="be8d00f5fe64d59dc463adb34f9fabdf262e1ed9",
                    last_commit_date=datetime.fromisoformat(
                        "2022-09-05T00:45:11+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=0,
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})


@pytest.fixture(autouse=False, scope="session")
def mock_tmp_repository() -> Iterator[str]:
    repo_path = tempfile.mkdtemp()
    files = {
        f"{repo_path}/back/test/conftest.py",
        f"{repo_path}/back/test/test_utils.py",
        f"{repo_path}/back/test/test_generic.py",
        f"{repo_path}/back/test/controlles/test_user.py",
        f"{repo_path}/back/test/controlles/test_client.py",
        f"{repo_path}/back/test/controlles/test_admin.py",
        f"{repo_path}/back/test/conftest.py",
        f"{repo_path}/back/src/controlles/user.py",
        f"{repo_path}/back/src/controlles/client.py",
        f"{repo_path}/back/src/controlles/admin.py",
        f"{repo_path}/back/src/controlles/admin.py",
        f"{repo_path}/back/src/statics/key.ssh",
        f"{repo_path}/back/src/statics/log.img",
        f"{repo_path}/README.md",
        f"{repo_path}/front/node_modules/colors/index.js",
        f"{repo_path}/front/node_modules/babel/index.js",
        f"{repo_path}/front/index.js",
        f"{repo_path}/front/www.html",
        f"{repo_path}/front/components/user/index.js",
        f"{repo_path}/front/components/user/index.spec.js",
        f"{repo_path}/front/components/admin/index.js",
        f"{repo_path}/front/components/admin/index.spec.js",
    }
    try:
        os.makedirs(repo_path, exist_ok=True)
        repo = Repo.init(repo_path)
        for file in files:
            os.makedirs(os.path.split(file)[0], exist_ok=True)
            with open(file, "w", encoding="utf-8") as handler:
                handler.write(f"# {file.split('/')[-1]}")
            repo.index.add(file)
        repo.index.commit("Initial commit")
        yield repo_path
    finally:
        rmtree(repo_path)
