from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import datetime
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingCommentsRequest,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    GroupVulnerabilitiesRequest,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    vulns_properties,
)
import pytest
import pytz
from settings import (
    TIME_ZONE,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vulns_id", "new_status", "properties"),
    (
        (
            "hacker@gmail.com",
            [
                "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            ],
            VulnerabilityStateStatus.VULNERABLE,
            {
                "Vulnerabilities": {
                    "192.168.1.208888": {
                        "location": "192.168.1.20",
                        "source": "ASM",
                        "specific": "8888",
                    },
                    "192.168.1.209999": {
                        "location": "192.168.1.20",
                        "source": "ASM",
                        "specific": "9999",
                    },
                },
            },
        ),
        (
            "reattacker@gmail.com",
            ["be09edb7-cd5c-47ed-bee4-97c645acdcea"],
            VulnerabilityStateStatus.SAFE,
            {
                "nickname/master": {
                    "back/src/model/user/index.js52": {
                        "assigned": None,
                        "location": "back/src/model/user/index.js",
                        "reattack requester": None,
                        "reduction in exposure": Decimal("1.1"),
                        "report date": datetime.date(2018, 4, 8),
                        "source": "ASM",
                        "specific": "52",
                    }
                }
            },
        ),
    ),
)
async def test_request_vulnerabilities_verification(
    populate: bool,
    email: str,
    vulns_id: list[str],
    new_status: VulnerabilityStateStatus,
    properties: dict,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(vulns_id[0])
    assert vulnerability
    assert vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    )
    vulnerable_locations = await loaders.group_vulnerabilities.load(
        GroupVulnerabilitiesRequest(
            group_name="group1",
            state_status=VulnerabilityStateStatus.VULNERABLE,
            paginate=False,
        )
    )
    assert vulnerability in {edge.node for edge in vulnerable_locations.edges}

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerabilities_id=vulns_id,
        status_after_verification=new_status,
    )
    assert "errors" not in result
    assert "success" in result["data"]["verifyVulnerabilitiesRequest"]
    assert result["data"]["verifyVulnerabilitiesRequest"]["success"]

    _vulns_properties = await vulns_properties(
        loaders,
        finding_id,
        [
            vuln
            for vuln in await loaders.vulnerability.load_many(vulns_id)
            if vuln is not None
        ],
        is_closed=new_status == VulnerabilityStateStatus.SAFE,
    )
    if "nickname/master" in _vulns_properties:
        del _vulns_properties["nickname/master"][
            "back/src/model/user/index.js52"
        ]["time to remediate"]
    assert _vulns_properties == properties

    finding = await loaders.finding.load(finding_id)
    assert finding
    assert finding.verification
    assert finding.verification.status == FindingVerificationStatus.VERIFIED
    assert finding.verification.vulnerability_ids
    assert vulns_id[0] in finding.verification.vulnerability_ids
    assert finding.verification.modified_by == email

    finding_comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.VERIFICATION, finding_id=finding_id
        )
    )
    new_vulnerable_locations = (
        await loaders.group_vulnerabilities.clear_all().load(
            GroupVulnerabilitiesRequest(
                group_name="group1",
                state_status=VulnerabilityStateStatus.VULNERABLE,
                paginate=False,
            )
        )
    )

    comment_date = (
        finding_comments[-1]
        .creation_date.astimezone(tz=pytz.timezone(TIME_ZONE))
        .strftime("%Y/%m/%d %H:%M")
    ).replace(" ", " at ")
    vulnerability = await loaders.vulnerability.clear_all().load(vulns_id[0])
    assert vulnerability
    if new_status == VulnerabilityStateStatus.SAFE:
        assert vulnerability not in {
            edge.node for edge in new_vulnerable_locations.edges
        }
        assert finding_comments[-1].content == (
            f"A reattack request was executed on {comment_date}."
            "\n\nClosed vulnerabilities:\n  -  "
            "nickname/back/src/model/user/index.js (52)"
            "\n\nObservations:\n  Vuln verified"
        )
    else:
        assert vulnerability in {
            edge.node for edge in new_vulnerable_locations.edges
        }
        assert finding_comments[-1].content == (
            f"A reattack request was executed on {comment_date}."
            "\n\nOpen vulnerabilities:\n  - 192.168.1.20 (9999)"
            "\n  - 192.168.1.20 (8888)\n\nObservations:\n  Vuln verified"
        )

    assert vulnerability.state.status == new_status
    assert vulnerability.verification
    assert (
        vulnerability.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id", "new_status"),
    (
        (
            "admin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.VULNERABLE,
        ),
    ),
)
async def test_request_vulnerabilities_verification_fail_1(
    populate: bool,
    email: str,
    vuln_id: str,
    new_status: VulnerabilityStateStatus,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerabilities_id=[vuln_id],
        status_after_verification=new_status,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Error verification not requested"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_vulnerabilities_request")
@pytest.mark.parametrize(
    ("email", "vuln_id", "new_status"),
    (
        (
            "user@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            VulnerabilityStateStatus.VULNERABLE,
        ),
        (
            "vulnerability_manager@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            VulnerabilityStateStatus.SAFE,
        ),
    ),
)
async def test_request_vulnerabilities_verification_fail_2(
    populate: bool,
    email: str,
    vuln_id: str,
    new_status: VulnerabilityStateStatus,
) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"

    result: dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerabilities_id=[vuln_id],
        status_after_verification=new_status,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
