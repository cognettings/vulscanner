# pylint: disable=invalid-name
from enum import (
    Enum,
)


class Entity(str, Enum):
    event: str = "event"
    finding: str = "finding"
    root: str = "root"
    vulnerability: str = "vulnerability"


class EntityId(str, Enum):
    ids: str = "ids"


class EntityAttr(str, Enum):
    efficacy: str = "efficacy"
    closed_vulnerabilities: str = "closed_vulnerabilities"
    closing_date: str = "closing_date"
    solving_date: str = "solving_date"
    last_reattack_date: str = "last_reattack_date"
    last_reattack_requester: str = "last_reattack_requester"
    last_requested_reattack_date: str = "last_requested_reattack_date"
    last_status_update: str = "last_status_update"
    max_open_severity_score: str = "max_open_severity_score"
    newest_vulnerability_report_date: str = "last_vulnerability_report_date"
    oldest_open_vulnerability_report_date: str = (
        "oldest_open_vulnerability_report_date"
    )
    oldest_vulnerability_report_date: str = "oldest_vulnerability_report_date"
    open_vulnerabilities: str = "open_vulnerabilities"
    rejected_vulnerabilities: str = "rejected_vulnerabilities"
    report_date: str = "report_date"
    reattack_cycles: str = "reattack_cycles"
    source: str = "source"
    status: str = "status"
    submitted_vulnerabilities: str = "submitted_vulnerabilities"
    total_open_cvssf: str = "total_open_cvssf"
    treatment_changes: str = "treatment_changes"
    treatment_summary: str = "treatment_summary"
    verification_summary: str = "verification_summary"
    where: str = "where"


class EntityDependency(str, Enum):
    activate_root: str = "activate_root"
    approve_draft: str = "approve_draft"
    deactivate_root: str = "deactivate_root"
    handle_vulnerabilities_acceptance: str = (
        "handle_vulnerabilities_acceptance"
    )
    handle_finding_policy: str = "handle_finding_policy"
    move_root: str = "move_root"
    confirm_vulnerabilities: str = "confirm_vulnerabilities"
    reject_vulnerabilities: str = "reject_vulnerabilities"
    reject_vulnerabilities_zero_risk: str = "reject_vulnerabilities_zero_risk"
    remove_vulnerability: str = "remove_vulnerability"
    request_vulnerabilities_hold: str = "request_vulnerabilities_hold"
    request_vulnerabilities_verification: str = (
        "request_vulnerabilities_verification"
    )
    request_vulnerabilities_zero_risk: str = (
        "request_vulnerabilities_zero_risk"
    )
    reset_expired_accepted_findings: str = "reset_expired_accepted_findings"
    resubmit_vulnerabilities: str = "resubmit_vulnerabilities"
    solve_event: str = "solve_event"
    update_vulnerabilities_treatment: str = "update_vulnerabilities_treatment"
    update_vulnerability_commit: str = "update_vulnerability_commit"
    update_severity: str = "update_severity"
    upload_file: str = "upload_file"
    verify_vulnerabilities_request: str = "verify_vulnerabilities_request"
