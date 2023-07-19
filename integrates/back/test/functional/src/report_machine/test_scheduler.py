from .conftest import (
    CRITERIA_VULNERABILITIES,
)
from custom_exceptions import (
    InvalidRootComponent,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    GroupState,
)
from db_model.groups.update import (
    update_state,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from finding_comments import (
    domain as comments_domain,
)
import json
import pytest
from server_async.report_machine import (
    process_execution,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_persist_result(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/persist_result.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": ["back/src/"], "exclude": []},
                "sca": {"include": ["back/src/"], "exclude": []},
                "apk": {"include": [], "exclude": []},
            }
        ),
    ):
        with mock.patch(
            "server_async.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(return_value=sarif_report),
        ), mock.patch(
            "server_async.report_machine.get_vulns_file",
            side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
        ):
            loaders = get_new_context()
            requested_verification_vuln = await loaders.vulnerability.load(
                "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz"
            )
            assert requested_verification_vuln
            assert (
                requested_verification_vuln.verification is not None
                and requested_verification_vuln.verification.status
                is VulnerabilityVerificationStatus.REQUESTED
            )
            closed_vuln = await loaders.vulnerability.load(
                "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
            )
            assert closed_vuln
            assert (
                closed_vuln.verification is not None
                and closed_vuln.verification.status
                is VulnerabilityVerificationStatus.REQUESTED
            )

            await process_execution("group1_1234345")

            loaders = get_new_context()
            group_findings = await loaders.group_findings.load("group1")
            finding_001: Finding | None = next(
                (
                    finding
                    for finding in group_findings
                    if "001" in finding.title
                ),
                None,
            )
            assert finding_001 is not None

            open_vulnerabilities: tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_001.id
                )
                if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
                and vuln.state.source == Source.MACHINE
                and vuln.root_id == "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
            submitted_vulnerabilities: tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_001.id
                )
                if vuln.state.status == VulnerabilityStateStatus.SUBMITTED
                and vuln.state.source == Source.MACHINE
                and vuln.root_id == "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
            requested_verification_vuln = await loaders.vulnerability.load(
                "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz"
            )
            assert requested_verification_vuln
            assert (
                requested_verification_vuln.verification is not None
                and requested_verification_vuln.verification.status
                is VulnerabilityVerificationStatus.VERIFIED
            )
            # The execution must close vulnerabilities in the scope
            closed_vuln = await loaders.vulnerability.load(
                "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
            )
            assert closed_vuln
            assert (
                closed_vuln.verification is not None
                and closed_vuln.verification.status
                is VulnerabilityVerificationStatus.VERIFIED
            )
            closed_vuln_historic = (
                await loaders.vulnerability_historic_state.load(
                    "4dbc01e0-4cfc-4b77-9b71-bb7566c60bg"
                )
            )
            assert len(open_vulnerabilities) == 2
            assert len(submitted_vulnerabilities) == 1
            assert closed_vuln.state.status == VulnerabilityStateStatus.SAFE
            assert (
                closed_vuln_historic[-1].commit
                == "7fd232de194916018c4ba68f5cb6dc595e99df7e"
            )
            assert finding_001.evidences.evidence5 is not None
            assert finding_001.evidences.evidence1 is None
            assert (
                "sql injection in"
                in finding_001.evidences.evidence5.description
            )

            comments = await comments_domain.get_comments(
                loaders=loaders,
                group_name="group1",
                finding_id=finding_001.id,
                user_email="machine@fludidattacks.com",
            )
            assert len(comments) == 1

            for comment in comments:
                if "still open" in comment.content:
                    assert "back/src/index.js" in comment.content
                elif "were solved" in comment.content:
                    assert (
                        "back/src/controller/user/index.js" in comment.content
                    )
                    assert "back/src/model/user/index.js" in comment.content


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_report_f120(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/report_f120.sarif", "rb"
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": [], "exclude": []},
                "sca": {
                    "include": [
                        "skims/test/data/lib_path/f011/requirements.txt"
                    ],
                    "exclude": [],
                },
                "apk": {"include": [], "exclude": []},
            }
        ),
    ):
        with mock.patch(
            "server_async.report_machine.get_sarif_log",
            side_effect=mock.AsyncMock(return_value=sarif_report),
        ), mock.patch(
            "server_async.report_machine.get_vulns_file",
            side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
        ):
            loaders = get_new_context()
            group_findings = await loaders.group_findings.load("group1")
            finding_f120: Finding | None = next(
                (
                    finding
                    for finding in group_findings
                    if finding.title.startswith("120")
                ),
                None,
            )
            assert finding_f120 is None

            await process_execution("group1_1234345")

            loaders.group_findings.clear("group1")
            group_findings = await loaders.group_findings.load("group1")
            finding_f120 = next(
                (
                    finding
                    for finding in group_findings
                    if finding.title.startswith("120")
                ),
                None,
            )
            assert finding_f120 is not None

            integrates_vulnerabilities: tuple[Vulnerability, ...] = tuple(
                vuln
                for vuln in await loaders.finding_vulnerabilities.load(
                    finding_f120.id
                )
                if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
                and vuln.state.source == Source.MACHINE
            )

            assert len(integrates_vulnerabilities) == 2

            status_1 = integrates_vulnerabilities[0].state.status
            where_1 = integrates_vulnerabilities[0].state.where

            assert status_1 == VulnerabilityStateStatus.VULNERABLE
            location_1 = (
                "skims/test/data/lib_path/f011/requirements.txt"
                " (missing dependency: urllib3)"
            )
            location_2 = (
                "skims/test/data/lib_path/f011/requirements.txt"
                " (missing dependency: botocore)"
            )
            assert where_1 in {location_1, location_2}


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_duplicated_reports(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/"
        "duplicated_report_1.sarif",
        "rb",
    ) as sarif_1:
        with open(
            "back/test/functional/src/report_machine/sarif/"
            "duplicated_report_2.sarif",
            "rb",
        ) as sarif_2:
            sarif_report_1 = json.load(sarif_1)
            sarif_report_2 = json.load(sarif_2)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": [], "exclude": []},
                "sca": {
                    "include": ["skims/test/data/lib_path/f011/build.gradle"],
                    "exclude": [],
                },
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server_async.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report_1, sarif_report_2],
        ),
    ), mock.patch(
        "server_async.report_machine.get_vulns_file",
        side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
    ):
        await process_execution("group1_")

        loaders = get_new_context()
        group_findings = await loaders.group_findings.load("group1")
        finding_011: Finding | None = next(
            (finding for finding in group_findings if "011" in finding.title),
            None,
        )
        assert finding_011 is not None

        integrates_vulnerabilities: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities) == 1

        id_1 = integrates_vulnerabilities[0].id
        where_1 = integrates_vulnerabilities[0].state.where
        await process_execution("group1_")
        loaders.finding_vulnerabilities.clear(finding_011.id)
        integrates_vulnerabilities_2: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities_2) == 1

        id_2 = integrates_vulnerabilities_2[0].id
        where_2 = integrates_vulnerabilities_2[0].state.where
        assert where_1 == where_2
        assert id_1 == id_2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_updated_advisory_report(  # pylint: disable=too-many-locals
    populate: bool,
) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/advisorie_report.sarif",
        "rb",
    ) as sarif_1:
        with open(
            "back/test/functional/src/report_machine/sarif/"
            "advisorie_change_report.sarif",
            "rb",
        ) as sarif_2:
            sarif_report_1 = json.load(sarif_1)
            sarif_report_2 = json.load(sarif_2)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": [], "exclude": []},
                "sca": {
                    "include": ["skims/test/data/lib_path/f011/build.gradle"],
                    "exclude": [],
                },
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server_async.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report_1, sarif_report_2],
        ),
    ), mock.patch(
        "server_async.report_machine.get_vulns_file",
        side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
    ):
        await process_execution("group1_")

        loaders = get_new_context()
        group_findings = await loaders.group_findings.load("group1")
        finding_011: Finding | None = next(
            (finding for finding in group_findings if "011" in finding.title),
            None,
        )
        assert finding_011 is not None

        integrates_vulnerabilities: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities) == 1
        assert (
            integrates_vulnerabilities[0].state.status
            == VulnerabilityStateStatus.VULNERABLE
        )
        id_1 = integrates_vulnerabilities[0].id
        where_1 = integrates_vulnerabilities[0].state.where
        await process_execution("group1_")
        loaders.finding_vulnerabilities.clear(finding_011.id)
        integrates_vulnerabilities_2: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_011.id
            )
            if vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities_2) == 1

        id_2 = integrates_vulnerabilities_2[0].id
        where_2 = integrates_vulnerabilities_2[0].state.where
        status_2 = integrates_vulnerabilities_2[0].state.status

        assert id_2 == id_1
        assert status_2 == VulnerabilityStateStatus.VULNERABLE
        assert where_1 == where_2
        if (
            advisories_1 := (
                integrates_vulnerabilities[0].state.advisories.cve
                if integrates_vulnerabilities[0].state.advisories
                and integrates_vulnerabilities[0].state.advisories.cve
                else None
            )
        ) and (
            advisories_2 := (
                integrates_vulnerabilities_2[0].state.advisories.cve
                if integrates_vulnerabilities_2[0].state.advisories
                and integrates_vulnerabilities_2[0].state.advisories.cve
                else None
            )
        ):
            assert advisories_1 != advisories_2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_approval(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/approval.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": ["."], "exclude": []},
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server_async.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(return_value=sarif_report),
    ), mock.patch(
        "server_async.report_machine.get_vulns_file",
        side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
    ):
        loaders = get_new_context()
        findings = await loaders.group_findings.load("group1")
        f_117: Finding | None = next(
            (fin for fin in findings if fin.title.startswith("117")), None
        )
        f_011: Finding | None = next(
            (fin for fin in findings if fin.title.startswith("011")), None
        )
        f_237: Finding | None = next(
            (fin for fin in findings if fin.title.startswith("237")), None
        )
        assert f_117 is not None
        assert f_117.severity.confidentiality_impact == Decimal("0.00")
        assert f_237 is None

        f_117_vulns = await loaders.finding_vulnerabilities.load(f_117.id)
        assert len(f_117_vulns) == 1
        assert (f_117_vulns[0].state.where, f_117_vulns[0].state.specific) == (
            ".project",
            "0",
        )

        await process_execution("group1_")
        loaders.group_findings.clear("group1")
        loaders.finding_vulnerabilities.clear(f_117.id)

        findings = await loaders.group_findings.load("group1")
        f_117 = next(
            (fin for fin in findings if fin.title.startswith("117")), None
        )
        f_237 = next(
            (fin for fin in findings if fin.title.startswith("237")), None
        )
        assert f_117 is not None
        assert f_117.severity.confidentiality_impact == Decimal("0.00")
        assert f_011 is not None
        assert f_237 is not None

        f_117_vulns = await loaders.finding_vulnerabilities.load(f_117.id)
        f_011_vulns = await loaders.finding_vulnerabilities.load(f_011.id)
        f_237_vulns = await loaders.finding_vulnerabilities.load(f_237.id)
        assert len(f_117_vulns) == 3
        assert len(f_237_vulns) == 3
        assert len(f_011_vulns) == 2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_report_inputs(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/report_inputs.sarif",
        "rb",
    ) as sarif:
        sarif_report = json.load(sarif)
    with open(
        "back/test/functional/src/report_machine/sarif/"
        "invalid_component.sarif",
        "rb",
    ) as sarif:
        invalid_sarif_report = json.load(sarif)

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "dast": {"urls": ["http://localhost:48000/"]},
                "sast": {"include": [], "exclude": []},
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server_async.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report, invalid_sarif_report]
        ),
    ), mock.patch(
        "server_async.report_machine.get_vulns_file",
        side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
    ):
        loaders = get_new_context()
        findings = await loaders.group_findings.load("group1")
        f_128: Finding | None = next(
            (fin for fin in findings if fin.title.startswith("128")), None
        )
        assert f_128 is None

        await process_execution("group1_")
        loaders.group_findings.clear("group1")

        findings = await loaders.group_findings.load("group1")
        f_128 = next(
            (fin for fin in findings if fin.title.startswith("128")), None
        )
        assert f_128 is not None

        f_128_vulns = await loaders.finding_vulnerabilities.load(f_128.id)
        assert len(f_128_vulns) == 3

        with pytest.raises(InvalidRootComponent):
            await process_execution("group1_")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_has_redirect_url_report(populate: bool) -> None:
    assert populate
    with open(
        "back/test/functional/src/report_machine/sarif/report_f043.sarif",
        "rb",
    ) as sarif_1:
        sarif_report_1 = json.load(sarif_1)

    sarif_report_2 = sarif_report_1

    with mock.patch(
        "server_async.report_machine.get_config",
        side_effect=mock.AsyncMock(
            return_value={
                "namespace": "back",
                "language": "EN",
                "sast": {"include": [], "exclude": []},
                "dast": {
                    "urls": ["https://myoriginalurl.com"],
                },
                "apk": {"include": [], "exclude": []},
            },
        ),
    ), mock.patch(
        "server_async.report_machine.get_sarif_log",
        side_effect=mock.AsyncMock(
            side_effect=[sarif_report_1, sarif_report_2],
        ),
    ), mock.patch(
        "server_async.report_machine.get_vulns_file",
        side_effect=mock.AsyncMock(return_value=CRITERIA_VULNERABILITIES),
    ):
        await process_execution("group1_")

        loaders = get_new_context()
        group_findings = await loaders.group_findings.load("group1")
        finding_043: Finding | None = next(
            (finding for finding in group_findings if "043" in finding.title),
            None,
        )
        assert finding_043 is not None

        integrates_vulnerabilities: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_043.id
            )
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            and vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities) == 1
        id_1 = integrates_vulnerabilities[0].id

        status_1 = integrates_vulnerabilities[0].state.status
        where_1 = integrates_vulnerabilities[0].state.where

        assert status_1 == VulnerabilityStateStatus.VULNERABLE
        assert where_1 == "http://localhost:48000 (back)"

        await process_execution("group1_")
        loaders.finding_vulnerabilities.clear(finding_043.id)
        integrates_vulnerabilities_2: tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(
                finding_043.id
            )
            if vuln.state.source == Source.MACHINE
        )
        assert len(integrates_vulnerabilities_2) == 1

        id_2 = integrates_vulnerabilities_2[0].id
        status_2 = integrates_vulnerabilities_2[0].state.status

        assert id_2 == id_1
        assert status_2 == VulnerabilityStateStatus.VULNERABLE


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
async def test_process_execution_fail(populate: bool) -> None:
    assert populate

    # Show logger warning when machine service is not included.
    await update_state(
        group_name="group1",
        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
        state=GroupState(
            has_machine=False,
            has_squad=True,
            managed=GroupManaged["MANAGED"],
            modified_by="unknown",
            modified_date=datetime.fromisoformat("2020-05-20T22:00:00+00:00"),
            service=GroupService.WHITE,
            status=GroupStateStatus.ACTIVE,
            tier=GroupTier.OTHER,
            type=GroupSubscriptionType.CONTINUOUS,
        ),
    )

    assert not await process_execution("group1_1234345")
