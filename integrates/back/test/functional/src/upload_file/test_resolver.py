# pylint: disable=import-error,too-many-lines
from . import (
    get_group_vulnerabilities,
    get_result,
    update_services,
)
import asyncio
from back.test.functional.src.confirm_vulnerabilities import (
    get_result as confirm_vulnerabilities,
)
from back.test.functional.src.finding import (
    get_result as get_finding,
)
from back.test.functional.src.organization_finding_policy_acceptance import (
    get_result as accept_policy,
)
from back.test.functional.src.remove_vulnerability import (
    get_result as remove_vulnerability,
)
from custom_exceptions import (
    InvalidFileType,
    RootNotFound,
    VulnerabilityUrlFieldDoNotExistInToeInputs,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerificationSummary,
)
from db_model.groups.enums import (
    GroupSubscriptionType,
)
from db_model.types import (
    SeverityScore,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
    Vulnerability,
    VulnerabilityEdge,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
import pytest
import simplejson as json
from typing import (
    Any,
)


def _get_key(item: dict) -> str:
    return item["node"]["where"]


async def _get_vulns(
    loaders: Dataloaders,
    finding_id: str,
    group_name: str,
) -> list[dict[str, Any]]:
    finding_vulns = await loaders.finding_vulnerabilities.load(finding_id)
    roots = await loaders.group_roots.load(group_name)
    roots_nickname: dict[str, str] = {
        root.id: root.state.nickname for root in roots
    }
    return sorted(
        (
            dict(
                commit_hash=vuln.state.commit,
                repo_nickname=roots_nickname[vuln.root_id or ""],
                specific=vuln.state.specific,
                state_status=vuln.state.status.value,
                stream=vuln.stream,
                treatment_status=vuln.treatment.status.value
                if vuln.treatment
                else None,
                type=vuln.type.value,
                verification_status=vuln.verification.status.value
                if vuln.verification
                else None,
                where=vuln.state.where,
                technique=vuln.technique,
            )
            for vuln in finding_vulns
            if vuln.zero_risk is None
        ),
        key=str,
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_upload_file(
    # pylint: disable=too-many-locals
    populate: bool,
    email: str,
) -> None:
    assert populate
    loaders = get_new_context()
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    with freeze_time("2022-02-09"):
        result: dict[str, Any] = await get_result(
            user=email,
            finding=finding_id,
            yaml_file_name=file_name,
        )
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]
    assert await _get_vulns(loaders, finding_id, "group1") == [
        {
            "commit_hash": "111111111111111111111111111111111111111f",
            "repo_nickname": "universe",
            "specific": "1",
            "state_status": "SUBMITTED",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "test/1",
            "technique": "SCR",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "universe",
            "specific": "123",
            "state_status": "SUBMITTED",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "path/to/file1.ext",
            "technique": "SCR",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "universe",
            "specific": "45",
            "state_status": "SUBMITTED",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "path/to/file1.ext",
            "technique": "SCR",
        },
        {
            "commit_hash": "5b5c92105b5c92105b5c92105b5c92105b5c9210",
            "repo_nickname": "universe",
            "specific": "88",
            "state_status": "SUBMITTED",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "LINES",
            "verification_status": None,
            "where": "path/to/file1.ext",
            "technique": "SCR",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe",
            "specific": "phone",
            "state_status": "SUBMITTED",
            "stream": ["home", "blog", "articulo"],
            "treatment_status": "UNTREATED",
            "type": "INPUTS",
            "verification_status": None,
            "where": "https://example.com",
            "technique": "MPT",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe44",
            "specific": "4444",
            "state_status": "VULNERABLE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.44",
            "technique": "MPT",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe45",
            "specific": "4545",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.45",
            "technique": "MPT",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe45",
            "specific": "4848",
            "state_status": "VULNERABLE",
            "stream": None,
            "technique": "MPT",
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.45",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe46",
            "specific": "4646",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": "VERIFIED",
            "where": "192.168.1.46",
            "technique": "MPT",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe46",
            "specific": "4646",
            "state_status": "SUBMITTED",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": None,
            "where": "192.168.1.46",
            "technique": "MPT",
        },
        {
            "commit_hash": None,
            "repo_nickname": "universe47",
            "specific": "4747",
            "state_status": "SAFE",
            "stream": None,
            "treatment_status": "UNTREATED",
            "type": "PORTS",
            "verification_status": None,
            "where": "192.168.1.47",
            "technique": "DAST",
        },
    ]
    expected_group_vulns = sorted(
        [
            {
                "node": {
                    "state": "VULNERABLE",
                    "treatmentStatus": "UNTREATED",
                    "verification": "Verified",
                    "where": "192.168.1.44",
                }
            },
            {
                "node": {
                    "state": "VULNERABLE",
                    "treatmentStatus": "UNTREATED",
                    "verification": "Verified",
                    "where": "192.168.1.45",
                }
            },
        ],
        key=_get_key,
    )
    await asyncio.sleep(8)
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1",
        state_status="VULNERABLE",
    )
    assert "errors" not in group_vulns
    assert (
        sorted(
            group_vulns["data"]["group"]["vulnerabilities"]["edges"],
            key=_get_key,
        )
        == expected_group_vulns
    )

    escaper_vuln: Vulnerability = next(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "4646"
        and vuln.state.where == "192.168.1.46"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )
    assert escaper_vuln.state.source == Source.ESCAPE

    vuln_loader = loaders.vulnerability
    open_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    vuln_open_verified = await vuln_loader.load(open_verified_id)
    assert vuln_open_verified
    assert (
        vuln_open_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_efficacy=Decimal("0"),
            unreliable_last_reattack_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date=(
                datetime.fromisoformat("2018-04-08T01:45:11+00:00")
            ),
            unreliable_reattack_cycles=None,
            unreliable_report_date=datetime.fromisoformat(
                "2018-04-08T00:43:11+00:00"
            ),
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )
    closed_verified_id = "be09edb7-cd5c-47ed-bee4-97c645acdce9"
    vuln_closed_verified = await vuln_loader.load(closed_verified_id)
    assert vuln_closed_verified
    assert (
        vuln_closed_verified.unreliable_indicators
        == VulnerabilityUnreliableIndicators(
            unreliable_closing_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_efficacy=Decimal("100"),
            unreliable_last_reattack_date=datetime.fromisoformat(
                "2022-02-09T00:00:00+00:00"
            ),
            unreliable_last_reattack_requester="requester@gmail.com",
            unreliable_last_requested_reattack_date=(
                datetime.fromisoformat("2018-04-08T01:45:11+00:00")
            ),
            unreliable_reattack_cycles=None,
            unreliable_report_date=datetime.fromisoformat(
                "2018-04-08T00:44:11+00:00"
            ),
            unreliable_source=Source.ASM,
            unreliable_treatment_changes=0,
        )
    )

    vuln_changed_source_id = "be09edb7-cd5c-47ed-bee4-97c645acdceb"
    vuln_changed_source = await vuln_loader.load(vuln_changed_source_id)
    assert vuln_changed_source
    assert vuln_changed_source.state.source == Source.ANALYST
    assert vuln_changed_source.severity_score == SeverityScore(
        base_score=Decimal("5.7"),
        temporal_score=Decimal("5.7"),
        cvss_v3="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C",
        cvssf=Decimal("10.556"),
    )
    assert vuln_changed_source.cwe_ids == ["CWE-122", "CWE-787"]

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.unreliable_indicators == FindingUnreliableIndicators(
        unreliable_newest_vulnerability_report_date=(
            datetime.fromisoformat("2020-04-08T00:44:11+00:00")
        ),
        unreliable_oldest_open_vulnerability_report_date=(
            datetime.fromisoformat("2018-04-08T00:43:11+00:00")
        ),
        unreliable_oldest_vulnerability_report_date=(
            datetime.fromisoformat("2018-04-08T00:43:11+00:00")
        ),
        unreliable_status=FindingStatus.VULNERABLE,
        unreliable_total_open_cvssf=Decimal("21.112"),
        unreliable_treatment_summary=FindingTreatmentSummary(
            accepted=0, accepted_undefined=0, in_progress=0, untreated=2
        ),
        unreliable_verification_summary=FindingVerificationSummary(
            requested=0, on_hold=0, verified=2
        ),
        unreliable_where="192.168.1.44, 192.168.1.45",
        open_vulnerabilities=2,
        closed_vulnerabilities=3,
        submitted_vulnerabilities=6,
        rejected_vulnerabilities=0,
        max_open_severity_score=Decimal("5.7"),
        newest_vulnerability_report_date=(
            datetime.fromisoformat("2020-04-08T00:44:11+00:00")
        ),
        oldest_vulnerability_report_date=(
            datetime.fromisoformat("2018-04-08T00:43:11+00:00")
        ),
        treatment_summary=FindingTreatmentSummary(
            accepted=0, accepted_undefined=0, in_progress=0, untreated=2
        ),
    )

    # Severity values are given explicitly in the vuln yaml file
    vuln_severity_explicit: Vulnerability = next(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "123"
        and vuln.state.where == "path/to/file1.ext"
        and vuln.type == VulnerabilityType.LINES
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )
    assert vuln_severity_explicit.severity_score == SeverityScore(
        base_score=Decimal("8.0"),
        temporal_score=Decimal("8.0"),
        cvss_v3="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H",
        cvssf=Decimal("256.0"),
    )
    assert vuln_severity_explicit.cwe_ids == ["CWE-1035", "CWE-770", "CWE-937"]

    # Severity values still not given, vuln without severity
    vuln_severity_empty: Vulnerability = next(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "1"
        and vuln.state.where == "test/1"
        and vuln.type == VulnerabilityType.LINES
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )
    assert vuln_severity_empty.severity_score is None
    assert vuln_severity_empty.cwe_ids is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_upload_file_access_denied_error(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_upload_new_closed(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulns-new-closed-error.yaml"
    loaders: Dataloaders = get_new_context()
    current_number = len(
        await loaders.finding_vulnerabilities_all.load(finding_id)
    )
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result
    assert not result["data"]["uploadFile"]["success"]
    loaders.finding_vulnerabilities_all.clear_all()
    assert (
        len(await loaders.finding_vulnerabilities_all.load(finding_id))
        == current_number
    )

    loaders.finding_vulnerabilities_all.clear_all()
    all_vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    vulnerability = next(
        (
            vuln
            for vuln in all_vulnerabilities
            if vuln.state.specific == "4848"
            and vuln.state.where == "192.168.1.45"
            and vuln.type == VulnerabilityType.PORTS
        ),
        None,
    )
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name="test-vuln-safe-different-root.yaml",
    )
    assert "errors" not in result
    assert not result["data"]["uploadFile"]["success"]

    loaders.finding_vulnerabilities_all.clear_all()
    all_vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    assert len(all_vulnerabilities) == current_number
    assert (
        next(
            (
                vuln
                for vuln in all_vulnerabilities
                if vuln.state.specific == "4848"
                and vuln.state.where == "192.168.1.45"
                and vuln.type == VulnerabilityType.PORTS
                and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            ),
            None,
        )
        is not None
    )
    assert (
        next(
            (
                vuln
                for vuln in all_vulnerabilities
                if vuln.state.specific == "4848"
                and vuln.state.where == "192.168.1.45"
                and vuln.type == VulnerabilityType.PORTS
                and vuln.state.status == VulnerabilityStateStatus.SAFE
            ),
            None,
        )
        is None
    )

    file_name = "test-vulns-new-vulnerable-error.yaml"
    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert (
        len(await loaders.finding_vulnerabilities_all.load(finding_id))
        == current_number
    )
    assert (
        "Exception - New vulnerabilities require the submitted status"
        in result["errors"][0]["message"]
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_invalid_schema(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vuln-invalid-schema.yaml"

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert (
        json.loads(result["errors"][0]["message"])["msg"]
        == "Exception - Invalid Schema"
    )
    assert json.loads(result["errors"][0]["message"])["keys"] == [
        "repo_nickname, /ports/0"
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_upload_error_root(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vuln-error-root.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(RootNotFound())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_continuous_not_able(
    populate: bool, email: str
) -> None:
    """if type is continuous should have either squad or machine active"""
    assert populate
    finding_id: str = "918fbc15-2121-4c2a-83a8-dfa8748bcb2e"
    file_name: str = "test-vulns.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_input(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name: str = "test-vuln-input.yaml"

    vulns_data = await _get_vulns(get_new_context(), finding_id, "group1")
    assert all(
        item["specific"] != "pphone (en) [CVE-0000-1111]"
        for item in vulns_data
    )
    assert all(item["specific"] != "pphone (en)" for item in vulns_data)

    result_1: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    vulns_data = await _get_vulns(get_new_context(), finding_id, "group1")
    assert any(
        item["specific"] == "pphone (en) [CVE-0000-1111]"
        for item in vulns_data
    )
    assert any(item["specific"] == "pphone (en)" for item in vulns_data)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_finding_indicators(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "475041531"
    file_name: str = "test-vuln-input.yaml"

    vulns_data = await _get_vulns(get_new_context(), finding_id, "group1")
    assert len(vulns_data) == 0

    finding_data = await get_finding(user=email, finding_id=finding_id)
    assert "errors" not in finding_data
    assert finding_data["data"]["finding"]["status"] == "DRAFT"

    result_1: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    vulns_data = await _get_vulns(get_new_context(), finding_id, "group1")
    all_submitted = [
        item["state_status"] == "SUBMITTED" for item in vulns_data
    ]
    assert len(vulns_data) == 2
    assert all(all_submitted)

    finding_data = await get_finding(user=email, finding_id=finding_id)
    assert "errors" not in finding_data
    assert finding_data["data"]["finding"]["status"] == "DRAFT"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_input_error(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vuln-input-error.yaml"
    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(
        VulnerabilityUrlFieldDoNotExistInToeInputs(index="0")
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_already_vulnerable(
    populate: bool, email: str
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name: str = "test-vulnerability.yaml"
    result_1: dict = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    loaders: Dataloaders = get_new_context()

    vuln_id = next(
        vuln.id
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "8001"
        and vuln.state.where == "192.168.1.57"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )

    result_2: dict = await confirm_vulnerabilities(
        user=email,
        finding=finding_id,
        vulnerability=vuln_id,
    )

    assert "errors" not in result_2
    assert result_2["data"]["confirmVulnerabilities"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.treatment
    assert (
        vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.UNTREATED
    )

    result_3: dict = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_3
    assert (
        result_3["data"]["uploadFile"]["message"]
        == "Some uploaded locations are already vulnerable"
    )
    assert result_3["data"]["uploadFile"]["success"]

    loaders.vulnerability.clear(vuln_id)
    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.treatment
    assert (
        vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.UNTREATED
    )

    result_4 = await remove_vulnerability(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result_4
    assert result_4["data"]["removeVulnerability"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_invalid_specific(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulnerability-invalid-port.yaml"

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result
    assert "Exception - Error in port value" in result["errors"][0]["message"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_already_zerorisk_confirmed(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulnerability-zerorisk-confirmed.yaml"

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result
    assert (
        "Uploaded vulnerability is a confirmed Zero Risk"
        in result["errors"][0]["message"]
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_input_closed(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id = "333d9984-17b0-434a-a8e0-a464c74f0212"
    file_name = "test-vulnerability-input.yaml"

    await asyncio.sleep(2)
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1234",
        state_status="VULNERABLE",
    )
    assert len(group_vulns["data"]["group"]["vulnerabilities"]["edges"]) == 1
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1234",
        state_status="SAFE",
    )
    assert len(group_vulns["data"]["group"]["vulnerabilities"]["edges"]) == 0

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]

    await asyncio.sleep(2)
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1234",
        state_status="VULNERABLE",
    )
    assert len(group_vulns["data"]["group"]["vulnerabilities"]["edges"]) == 0
    group_vulns = await get_group_vulnerabilities(
        user=email,
        group_name="group1234",
        state_status="SAFE",
    )
    assert len(group_vulns["data"]["group"]["vulnerabilities"]["edges"]) == 1


async def _get_group_vuln_status(
    status: VulnerabilityStateStatus,
) -> tuple[VulnerabilityEdge, ...]:
    loaders = get_new_context()
    return (
        await loaders.group_vulnerabilities.load(
            GroupVulnerabilitiesRequest(
                group_name="group1234",
                state_status=status,
                paginate=False,
            )
        )
    ).edges


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_input_rejected(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id = "333d9984-17b0-434a-a8e0-a464c74f0212"

    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.REJECTED))
        == 1
    )
    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.SUBMITTED))
        == 0
    )

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name="test-vulnerability-input-open.yaml",
    )
    assert "errors" in result
    assert (
        "Exception - Uploaded vulnerability can not change the status"
        in result["errors"][0]["message"]
    )

    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.REJECTED))
        == 1
    )
    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.SUBMITTED))
        == 0
    )

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name="test-vulnerability-input-rejected.yaml",
    )
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]

    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.REJECTED))
        == 0
    )
    assert (
        len(await _get_group_vuln_status(VulnerabilityStateStatus.SUBMITTED))
        == 1
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_invalid_new_status(populate: bool) -> None:
    assert populate
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    email = "admin@gmail.com"
    loaders = get_new_context()

    result_1 = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name="test-vulnerability.yaml",
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    vuln_id = next(
        vuln.id
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "8001"
        and vuln.state.where == "192.168.1.57"
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )

    result_3 = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name="test-vulnerability-invalid-state.yaml",
    )
    assert "errors" in result_3
    assert (
        "Exception - Uploaded vulnerability can not change the status"
        in result_3["errors"][0]["message"]
    )

    loaders.finding_vulnerabilities.clear_all()
    assert next(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "8001"
        and vuln.state.where == "192.168.1.57"
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )
    assert (
        next(
            (
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_id
                )
                if vuln.state.specific == "8001"
                and vuln.state.where == "192.168.1.57"
                and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            ),
            None,
        )
        is None
    )

    result_4 = await remove_vulnerability(
        user=email, finding=finding_id, vulnerability=vuln_id
    )
    assert "errors" not in result_4
    assert result_4["data"]["removeVulnerability"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
async def test_upload_file_invalid_commithash(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name = "test-vulnerability-invalid-commithash.yaml"

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The commit hash is invalid"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["file_name"],
    [
        ["test-anim.gif"],
    ],
)
async def test_upload_file_invalid_file_type(
    populate: bool, file_name: str
) -> None:
    assert populate
    email = "admin@gmail.com"
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    result = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidFileType())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_upload_file_continuous_able(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    file_name: str = "test-vulnerability.yaml"

    result = await accept_policy(
        email="user_manager@fluidattacks.com",
        organization_name="orgtest",
        finding_policy_id="92551721-c8da-4452-b9a0-00b2a784f8e4",
        status="APPROVED",
    )
    assert "errors" not in result
    assert result["data"]["handleOrganizationFindingPolicyAcceptance"][
        "success"
    ]

    result_1: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )
    assert "errors" not in result_1
    assert result_1["data"]["uploadFile"]["success"]

    loaders: Dataloaders = get_new_context()
    vuln_id = next(
        vuln.id
        for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        if vuln.state.specific == "8001"
        and vuln.state.where == "192.168.1.57"
        and vuln.type == VulnerabilityType.PORTS
        and vuln.state.status == VulnerabilityStateStatus.SUBMITTED
    )

    vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.SUBMITTED
    assert vulnerability.treatment
    assert (
        vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
    )
    assert (
        vulnerability.treatment.acceptance_status
        == VulnerabilityAcceptanceStatus.APPROVED
    )

    mutation_2 = await update_services(
        user=email,
        group="group1",
        has_squad="false",
        has_machine="false",
        subscription=GroupSubscriptionType.CONTINUOUS.value,
    )
    assert "errors" not in mutation_2
    assert mutation_2["data"]["updateGroup"]["success"]

    result_2: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        yaml_file_name=file_name,
    )

    assert "errors" in result_2
    assert result_2["errors"][0]["message"] == "Access denied"
