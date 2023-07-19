from .findings import (
    check_finding_newest_report_date,
    check_finding_release_date,
    check_finding_severity_score,
    check_finding_status,
    check_finding_vulnerabilities_status,
    check_finding_vulnerabilities_treatment,
)
from .operations import (
    get_finding,
    get_released_nzr_vulns_by_finding as get_vulns,
    update_indicators,
)
from .types import (
    IndicatorsChecker,
)
from .utils import (
    LOGGER,
)
from dynamodb.types import (
    Record,
    StreamEvent,
)
from typing import (
    Any,
)


def _init_check_parameters(
    record: Record,
    event: StreamEvent,
    vuln: Any,
    default_to_update: dict[str, Any],
) -> IndicatorsChecker:
    if vuln is None:
        vuln = record.old_image
    finding = get_finding(
        pk=vuln["sk"],
        sk=vuln["pk_5"],
    )
    if finding and "pk" in finding:
        vulnerabilities = get_vulns(finding_id=finding["pk"])
        return IndicatorsChecker(
            record=record,
            event=event,
            vuln=vuln,
            finding=finding,
            vulnerabilities=vulnerabilities,
            current_indicators=finding.get("unreliable_indicators", {}),
            new_indicators=default_to_update,
        )
    return IndicatorsChecker(
        record=record,
        event=event,
        vuln=vuln,
        finding=None,
        vulnerabilities=[],
        current_indicators={},
        new_indicators={},
    )


def process(records: tuple[Record, ...]) -> None:
    for record in records:
        LOGGER.info("!! %s (%s)", record.event_name, record.sequence_number)

        last_update = ""

        if not record.old_image and record.new_image:
            last_update = record.new_image["created_date"]
        elif not record.new_image and record.old_image:
            last_update = record.old_image["state"]["modified_date"]
        elif record.new_image and record.old_image:
            last_update = record.new_image["state"]["modified_date"]

        checker_params = _init_check_parameters(
            record=record,
            event=record.event_name,
            vuln=record.new_image,
            default_to_update={
                "unreliable_last_status_update": last_update,
            },
        )

        check_finding_vulnerabilities_status(
            params=checker_params,
        )

        check_finding_vulnerabilities_treatment(
            params=checker_params,
        )

        check_finding_status(
            params=checker_params,
        )

        check_finding_severity_score(
            params=checker_params,
        )

        check_finding_release_date(
            params=checker_params,
        )

        check_finding_newest_report_date(
            params=checker_params,
        )

        update_indicators(
            finding=checker_params.finding,
            current_indicators=checker_params.current_indicators,
            new_indicators=checker_params.new_indicators,
        )
