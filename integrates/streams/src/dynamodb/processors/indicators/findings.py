from .types import (
    Indicators as IndicatorsClass,
    IndicatorsChecker,
)
from .utils import (
    is_zr_confirmed_or_requested,
    is_zr_requested,
    verbose_for,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    StreamEvent,
)
from typing import (
    Any,
    Literal,
)

Indicators = IndicatorsClass()
EVENTS = [StreamEvent.INSERT, StreamEvent.MODIFY, StreamEvent.REMOVE]


@verbose_for(Indicators.STATUS)
def check_finding_status(params: IndicatorsChecker) -> None:
    """Checks if vulnerability must update the finding status.

    Also, updates `new_indicators` inplace if it is necessary.

    Args:
        params (IndicatorsChecker): Parameters for checking indicators.
    """
    finding = params.finding
    vuln = params.vuln
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    if status == "VULNERABLE" and not is_zr_req:
        new_indicators[Indicators.STATUS] = "VULNERABLE"
    else:
        released_nzr_vulns = params.vulnerabilities
        open_vulns = [
            x
            for x in released_nzr_vulns
            if x["state"]["status"] == "VULNERABLE"
        ]

        if len(open_vulns) > 0:
            new_indicators[Indicators.STATUS] = "VULNERABLE"
        else:
            new_indicators[Indicators.STATUS] = "SAFE"

        if len(released_nzr_vulns) == 0:
            new_indicators[Indicators.STATUS] = "DRAFT"


def _init_status(
    current_indicators: dict[str, Any],
    new_indicators: dict[str, Any],
) -> None:
    """Modifies `new_indicators` inplace for adding status keys.

    Current indicators gives the values. It will be `Decimal(0)`
    otherwise.
    """
    status_keys = [
        Indicators.OPEN_VULNERABILITIES,
        Indicators.CLOSED_VULNERABILITIES,
        Indicators.REJECTED_VULNERABILITIES,
        Indicators.SUBMITTED_VULNERABILITIES,
    ]
    for key in status_keys:
        new_indicators[key] = current_indicators.get(key, Decimal(0))


def _update_status(
    status: Literal["SUBMITTED", "REJECTED", "VULNERABLE", "SAFE"],
    increment: int,
    current_indicators: dict[str, Any],
    new_indicators: dict[str, Any],
) -> None:
    """Add increment to `new_indicators[status]`
    if status is a valid status.
    """
    key = ""
    if status == "SUBMITTED":
        key = Indicators.SUBMITTED_VULNERABILITIES
    elif status == "REJECTED":
        key = Indicators.REJECTED_VULNERABILITIES
    elif status == "VULNERABLE":
        key = Indicators.OPEN_VULNERABILITIES
    elif status == "SAFE":
        key = Indicators.CLOSED_VULNERABILITIES
    else:
        key = ""

    if key != "":
        key = str(key)
        current = current_indicators.get(key, Decimal(0))
        new = Decimal(current + increment)
        new_indicators[key] = new if new >= 0 else Decimal(0)


def _update_on_zero_risk(
    prev_vuln: Any,
    vuln: Any,
    current_indicators: Any,
    new_indicators: Any,
) -> None:
    status = vuln["state"]["status"]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    prev_status = prev_vuln["state"]["status"]
    prev_zr_requested = is_zr_requested(prev_vuln)

    # When both have zero risk, nothing happens.
    if is_zr_req and prev_zr_requested:
        return

    # When zero risk is requested, the status is substracted.
    if is_zr_req and not prev_zr_requested:
        _update_status(status, -1, current_indicators, new_indicators)

    # When zero risk is deleted, the status is added.
    elif prev_zr_requested:
        _update_status(status, 1, current_indicators, new_indicators)

    # When no zero risk, the status is changed.
    else:
        if prev_status == status:
            return
        _update_status(prev_status, -1, current_indicators, new_indicators)
        _update_status(status, 1, current_indicators, new_indicators)


@verbose_for(Indicators.OPEN_VULNERABILITIES)
@verbose_for(Indicators.CLOSED_VULNERABILITIES)
@verbose_for(Indicators.REJECTED_VULNERABILITIES)
@verbose_for(Indicators.SUBMITTED_VULNERABILITIES)
def check_finding_vulnerabilities_status(params: IndicatorsChecker) -> None:
    """Checks if vulnerability status must update the indicators.
    Indicators includes a count of vulnerabilities by
    `open`, `closed`, `submitted` and `rejected` status.

    Also, updates `new_indicators` inplace if it is necessary.

    Args:
        params (IndicatorsChecker): Parameters for checking indicators.
    """
    record = params.record
    event = params.event
    finding = params.finding
    vuln = params.vuln
    current_indicators = params.current_indicators
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]

    # Zero risk is an internal status, so it is not included in indicators.
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    if event == StreamEvent.REMOVE:
        if not is_zr_req:
            _update_status(status, -1, current_indicators, new_indicators)

    elif event == StreamEvent.INSERT:
        _init_status(current_indicators, new_indicators)
        if not is_zr_req:
            _update_status(status, 1, current_indicators, new_indicators)

    elif event == StreamEvent.MODIFY:
        _update_on_zero_risk(
            record.old_image,
            vuln,
            current_indicators,
            new_indicators,
        )


@verbose_for(Indicators.SEVERITY)
def check_finding_severity_score(params: IndicatorsChecker) -> None:
    """Checks if max open severity score must be updated.

    Also, updates `new_indicators` inplace if it is necessary.

    Args:
        params (IndicatorsChecker): Parameters for checking indicators.
    """
    event = params.event
    finding = params.finding
    vuln = params.vuln
    current_indicators = params.current_indicators
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]
    open_vulns = []

    insert_or_remove = [StreamEvent.INSERT, StreamEvent.REMOVE]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    if status != "VULNERABLE" and event in insert_or_remove:
        return

    if status == "VULNERABLE" and not is_zr_req:
        open_vulns.append(vuln)
        score = current_indicators.get(Indicators.SEVERITY, Decimal(0))
        if "severity_score" in vuln:
            new_score = vuln["severity_score"]["temporal_score"]
            if score < new_score:
                new_indicators[Indicators.SEVERITY] = new_score
            return

    open_vulns.extend(
        [
            x
            for x in params.vulnerabilities
            if x["state"]["status"] == "VULNERABLE" and x["pk"] != vuln["pk"]
        ]
    )

    scores = [
        x["severity_score"]["temporal_score"]
        if "severity_score" in x
        else finding["severity_score"]["temporal_score"]
        for x in open_vulns
    ]

    if len(scores) > 0:
        new_indicators[Indicators.SEVERITY] = max(scores)
    else:
        new_indicators[Indicators.SEVERITY] = Decimal(0)


@verbose_for(Indicators.OLDEST_REPORT_DATE)
def check_finding_release_date(params: IndicatorsChecker) -> None:
    """Checks if release date must be updated.

    Also, updates `new_indicators` inplace if it is necessary.

    Args:
        finding (Any): Finding data of vulnerability.
        vuln (Any): Vulnerability data.
        new_indicators (Any): New indicators to update.
    """
    finding = params.finding
    vuln = params.vuln
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    released_vulns = []
    if status in ["VULNERABLE", "SAFE"] and not is_zr_req:
        released_vulns.append(vuln)

    released_vulns.extend(
        [x for x in params.vulnerabilities if x["pk"] != vuln["pk"]]
    )

    # using unreliable due to vulnerability release date is there.
    dates = [
        datetime.fromisoformat(
            v["unreliable_indicators"]["unreliable_report_date"]
        )
        if "unreliable_indicators" in v
        and "unreliable_report_date" in v["unreliable_indicators"]
        else datetime.fromisoformat(v["state"]["modified_date"])
        for v in released_vulns
    ]

    if len(dates) > 0:
        date = min(dates)
        new_indicators[Indicators.OLDEST_REPORT_DATE] = date.isoformat()
    else:
        new_indicators[Indicators.OLDEST_REPORT_DATE] = None


def _init_treatment(
    current_indicators: dict[str, Any],
    new_indicators: dict[str, Any],
) -> None:
    """Modifies `new_indicators` inplace for adding treatment keys.

    Current indicators gives the values. It will be `0`
    otherwise.
    """
    status_keys = [
        "accepted",
        "accepted_undefined",
        "in_progress",
        "untreated",
    ]
    treatment = Indicators.TREATMENT_SUMMARY
    current = current_indicators.get(treatment, {}).copy()
    new = {}
    for key in status_keys:
        new[key] = current.get(key, 0)

    new_indicators[treatment] = new


def _update_treatment(
    treatment: Literal[
        "ACCEPTED", "ACCEPTED_UNDEFINED", "IN_PROGRESS", "UNTREATED"
    ],
    increment: int,
    current_indicators: dict[str, Any],
    new_indicators: dict[str, Any],
) -> None:
    """Add increment to `new_indicators[status]`
    if status is a valid status.
    """
    if treatment in [
        "ACCEPTED",
        "ACCEPTED_UNDEFINED",
        "IN_PROGRESS",
        "UNTREATED",
    ]:
        key = treatment.lower()
        treatment_key = Indicators.TREATMENT_SUMMARY
        current = current_indicators.get(treatment_key, {}).copy()
        actual = current.get(key, 0)
        new = actual + increment
        current[key] = new if new >= 0 else 0
        new_indicators[treatment_key] = current.copy()


def _update_treatment_on_zero_risk(
    prev_vuln: Any,
    vuln: Any,
    current_indicators: Any,
    new_indicators: Any,
) -> None:
    status = vuln["state"]["status"]
    treatment = vuln["treatment"]["status"]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    prev_status = prev_vuln["state"]["status"]
    prev_treatment = prev_vuln["treatment"]["status"]
    prev_zr_requested = is_zr_requested(prev_vuln)

    if status == "VULNERABLE":
        if is_zr_req and prev_zr_requested:
            return

        if is_zr_req and not prev_zr_requested:
            _update_treatment(
                treatment, -1, current_indicators, new_indicators
            )

        elif prev_zr_requested:
            _update_treatment(treatment, 1, current_indicators, new_indicators)

        else:
            if prev_treatment == treatment and prev_status == status:
                return
            _update_treatment(
                prev_treatment, -1, current_indicators, new_indicators
            )
            _update_treatment(treatment, 1, current_indicators, new_indicators)

    elif prev_status == "VULNERABLE" and status != "VULNERABLE":
        _update_treatment(treatment, -1, current_indicators, new_indicators)


@verbose_for(Indicators.TREATMENT_SUMMARY)
def check_finding_vulnerabilities_treatment(params: IndicatorsChecker) -> None:
    """Checks if vulnerability treatment must update the indicators.
    Indicators includes a count of vulnerabilities by
    `untreated`, `in_progress`, `accepted` and `accepted_undefined` status.

    Also, updates `new_indicators` inplace if it is necessary.

    Args:
        params (IndicatorsChecker): Parameters for checking indicators.
    """
    record = params.record
    event = params.event
    finding = params.finding
    vuln = params.vuln
    current_indicators = params.current_indicators
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]
    treatment = vuln["treatment"]["status"]

    # Zero risk is an internal status, so it is not included in indicators.
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    # Delete status always substracts from the treatment count
    if event == StreamEvent.REMOVE:
        if not is_zr_req:
            _update_treatment(
                treatment, -1, current_indicators, new_indicators
            )

    elif event == StreamEvent.INSERT:
        _init_treatment(current_indicators, new_indicators)
        if status == "VULNERABLE" and not is_zr_req:
            _update_treatment(treatment, 1, current_indicators, new_indicators)

    elif event == StreamEvent.MODIFY and record.old_image is not None:
        _update_treatment_on_zero_risk(
            record.old_image, vuln, current_indicators, new_indicators
        )


@verbose_for(Indicators.NEWEST_REPORT_DATE)
def check_finding_newest_report_date(params: IndicatorsChecker) -> None:
    """Checks if newest report date must be updated.

    It updates `new_indicators` inplace if it is necessary.

    Args:
        params (IndicatorsChecker): Parameters for checking indicators.
    """
    finding = params.finding
    vuln = params.vuln
    new_indicators = params.new_indicators

    if not finding:
        return

    status = vuln["state"]["status"]
    is_zr_req = is_zr_confirmed_or_requested(vuln)

    released_vulns = []
    if status in ["VULNERABLE", "SAFE"] and not is_zr_req:
        released_vulns.append(vuln)

    released_vulns.extend(
        [x for x in params.vulnerabilities if x["pk"] != vuln["pk"]]
    )

    # using unreliable due to vulnerability release date is there.
    dates = [
        datetime.fromisoformat(
            v["unreliable_indicators"]["unreliable_report_date"]
        )
        if "unreliable_indicators" in v
        and "unreliable_report_date" in v["unreliable_indicators"]
        else datetime.fromisoformat(v["state"]["modified_date"])
        for v in released_vulns
    ]

    if len(dates) > 0:
        date = max(dates)
        new_indicators[Indicators.NEWEST_REPORT_DATE] = date.isoformat()
    else:
        new_indicators[Indicators.NEWEST_REPORT_DATE] = None
