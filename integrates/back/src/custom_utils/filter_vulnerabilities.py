from collections.abc import (
    Iterable,
)
from db_model.vulnerabilities.constants import (
    RELEASED_FILTER_STATUSES,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)


def filter_no_treatment_vulns(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.treatment
        and vuln.treatment.status == VulnerabilityTreatmentStatus.UNTREATED
    ]


def filter_non_deleted(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status
        not in {
            VulnerabilityStateStatus.DELETED,
            VulnerabilityStateStatus.MASKED,
        }
    ]


def filter_open_vulns(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    ]


def filter_closed_vulns(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.SAFE
    ]


def filter_released_vulns(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status in RELEASED_FILTER_STATUSES
    ]


def filter_non_confirmed_zero_risk(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if not vulnerability.zero_risk
        or vulnerability.zero_risk.status
        != VulnerabilityZeroRiskStatus.CONFIRMED
    ]


def filter_non_zero_risk(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vuln
        for vuln in vulnerabilities
        if not vuln.zero_risk
        or vuln.zero_risk.status
        not in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
    ]


def filter_remediated(
    vulnerabilities: Iterable[Vulnerability],
) -> list[Vulnerability]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.verification
        and vulnerability.verification.status
        == VulnerabilityVerificationStatus.REQUESTED
    ]


def filter_same_values(
    historic_state: list[VulnerabilityState],
) -> list[VulnerabilityState]:
    return [
        state
        for index, state in enumerate(historic_state)
        if index == 0 or state.status != historic_state[index - 1].status
    ]
