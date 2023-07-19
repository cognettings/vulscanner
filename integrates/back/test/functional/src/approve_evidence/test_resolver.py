from . import (
    get_result,
)
from custom_exceptions import (
    EvidenceNotFound,
)
from dataloaders import (
    get_new_context,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_evidence")
async def test_approve_evidence(populate: bool) -> None:
    assert populate
    finding_id = "c265b055-5f30-444f-ad88-1fefab65d59d"
    loaders = get_new_context()
    finding_before = await loaders.finding.load(finding_id)
    assert finding_before is not None
    assert finding_before.evidences.evidence1 is not None
    assert finding_before.evidences.evidence1.is_draft is True

    result = await get_result(
        email="reviewer@fluidattacks.com",
        evidence_id="EVIDENCE1",
        finding_id=finding_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["approveEvidence"]
    assert result["data"]["approveEvidence"]["success"]

    loaders.finding.clear_all()
    finding_after = await loaders.finding.load(finding_id)
    assert finding_after is not None
    assert finding_after.evidences.evidence1 is not None
    assert finding_after.evidences.evidence1.is_draft is False


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_evidence")
async def test_approve_evidence_non_existent(populate: bool) -> None:
    assert populate
    finding_id = "c265b055-5f30-444f-ad88-1fefab65d59d"
    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding is not None
    assert finding.evidences.animation is None

    result = await get_result(
        email="reviewer@fluidattacks.com",
        evidence_id="ANIMATION",
        finding_id=finding_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(EvidenceNotFound())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_evidence")
async def test_approve_evidence_already_approved(populate: bool) -> None:
    assert populate
    finding_id = "c265b055-5f30-444f-ad88-1fefab65d59d"
    loaders = get_new_context()
    finding = await loaders.finding.load(finding_id)
    assert finding is not None
    assert finding.evidences.evidence2 is not None
    assert finding.evidences.evidence2.is_draft is False

    result = await get_result(
        email="reviewer@fluidattacks.com",
        evidence_id="EVIDENCE2",
        finding_id=finding_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(EvidenceNotFound())
