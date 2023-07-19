from aioextensions import (
    collect,
)
from aiohttp import (
    ClientConnectorError,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
    ServerTimeoutError,
)
from botocore.exceptions import (
    ClientError,
    ConnectTimeoutError,
    HTTPClientError,
    ReadTimeoutError,
)
from custom_exceptions import (
    RootNotFound,
    UnavailabilityError as CustomUnavailabilityError,
)
from custom_utils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
    findings as findings_utils,
)
from custom_utils.findings import (
    get_finding_release_date,
    is_finding_released,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    FindingVerification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from findings import (
    domain as findings_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from more_itertools import (
    chunked,
)
from pyexcelerate import (
    Alignment,
    Color,
    Format,
    Style,
    Workbook,
    Worksheet as WorksheetType,
)
from reports.types import (
    GroupVulnsReportHeader,
    OrgVulnsReportHeader,
    PDFWordlistEn,
)
from roots import (
    utils as roots_utils,
)
from settings.logger import (
    LOGGING,
)
from typing import (
    Any,
    Iterable,
)

logging.config.dictConfig(LOGGING)

EMPTY = "-"
HEADER_HEIGHT = 20
ROW_HEIGHT = 57
RED = Color(255, 52, 53, 1)  # FF3435
WHITE = Color(255, 255, 255, 1)
LOGGER = logging.getLogger(__name__)
STATE_TRANSLATION: dict[VulnerabilityStateStatus, str] = {
    VulnerabilityStateStatus.SAFE: "SAFE",
    VulnerabilityStateStatus.VULNERABLE: "VULNERABLE",
}


# pylint: disable=too-many-instance-attributes
class ITReport:
    """Class to generate IT reports."""

    current_sheet: WorksheetType = None
    data: list[Finding] = []
    filters = None
    lang = None
    result_filename = ""
    row = 1

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,  # NOSONAR
        data: Iterable[Finding],
        group_name: str,
        states: set[VulnerabilityStateStatus],
        treatments: set[VulnerabilityTreatmentStatus],
        verifications: set[VulnerabilityVerificationStatus],
        closing_date: datetime | None,
        finding_title: str,
        age: int | None,
        min_severity: Decimal | None,
        max_severity: Decimal | None,
        last_report: int | None,
        min_release_date: datetime | None,
        max_release_date: datetime | None,
        location: str,
        loaders: Dataloaders,
        generate_raw_data: bool = False,
    ) -> None:
        """Initialize variables."""

        self.vulnerability = {
            col_name: index + 1
            for index, col_name in enumerate(
                GroupVulnsReportHeader.labels()
                + (OrgVulnsReportHeader.labels() if generate_raw_data else [])
            )
        }
        self.raw_data: list[list[Any]] = []
        self.workbook: Workbook

        self.row_values: list[str | int | float | datetime | None] = [
            EMPTY for _ in range(len(self.vulnerability) + 1)
        ]
        self.generate_raw_data = generate_raw_data
        self.data = list(data)
        self.loaders = loaders
        self.group_name = group_name
        self.treatments = treatments
        self.states = states
        self.verifications = verifications
        self.closing_date = closing_date
        self.finding_title = finding_title
        self.age = age
        self.min_severity = min_severity
        self.max_severity = max_severity
        self.last_report = last_report
        self.min_release_date = min_release_date
        self.max_release_date = max_release_date
        self.location = location
        if self.closing_date:
            self.states = set(
                [
                    VulnerabilityStateStatus["SAFE"],
                ]
            )
            self.treatments = set(VulnerabilityTreatmentStatus)
            if self.verifications != set(
                [
                    VulnerabilityVerificationStatus["VERIFIED"],
                ]
            ):
                self.verifications = set()

        self.are_all_treatments = len(sorted(self.treatments)) == len(
            sorted(set(VulnerabilityTreatmentStatus))
        )
        self.are_all_verifications = len(self.verifications) == 0

        self.raw_data = [list(self.vulnerability.keys())]
        self.workbook = Workbook()
        self.current_sheet = self.workbook.new_sheet("Data")
        self.parse_template()

    async def generate_data(self) -> None:
        await self.generate(self.data)

    async def generate_file(self) -> None:
        await self.generate(self.data)
        self.style_sheet()
        self.save()

    async def _get_findings_vulnerabilities(
        self, findings_ids: Iterable[str]
    ) -> list[Vulnerability]:
        finding_vulnerabilities_released_nzr = (
            self.loaders.finding_vulnerabilities_released_nzr
        )
        findings = chain.from_iterable(
            await collect(
                tuple(
                    finding_vulnerabilities_released_nzr.load_many_chained(
                        chuncked_findings
                    )
                    for chuncked_findings in chunked(list(findings_ids), 16)
                ),
                workers=4,
            )
        )

        return list(findings)

    async def _get_findings_historics_verifications(
        self, findings_ids: Iterable[str]
    ) -> list[list[FindingVerification]]:
        return await self.loaders.finding_historic_verification.load_many(
            findings_ids
        )

    def _get_filtered_findings(self, data: Iterable[Finding]) -> list[Finding]:
        if self.max_release_date:
            return [
                finding
                for finding in data
                if is_finding_released(finding)
                and (indicators := finding.unreliable_indicators)
                and finding.creation
                and (
                    indicators.oldest_vulnerability_report_date
                    or finding.creation.modified_date
                )
                <= self.max_release_date
            ]

        return list(data)

    def _get_filtered_findings_date(
        self, data: Iterable[Finding]
    ) -> list[Finding]:
        if self.min_release_date:
            return [
                finding
                for finding in data
                if is_finding_released(finding)
                and (release_date := get_finding_release_date(finding))
                and release_date >= self.min_release_date
            ]

        return list(data)

    @staticmethod
    def _get_first_report_days(finding: Finding) -> int:
        unreliable_indicators = finding.unreliable_indicators
        return findings_domain.get_report_days(
            unreliable_indicators.oldest_vulnerability_report_date
        )

    @staticmethod
    def _get_last_report_days(finding: Finding) -> int:
        indicators = finding.unreliable_indicators
        return findings_domain.get_report_days(
            indicators.newest_vulnerability_report_date
        )

    @staticmethod
    def _get_filtered_vulnerabilities_max_severity(
        finding_data: dict[str, Finding],
        max_severity: Decimal,
        vulnerabilities: Iterable[Vulnerability],
    ) -> list[Vulnerability]:
        severity_scores = [
            vulnerability.severity_score.temporal_score
            if vulnerability.severity_score
            else finding_data[
                vulnerability.finding_id
            ].severity_score.temporal_score
            for vulnerability in vulnerabilities
        ]

        return [
            vulnerability
            for vulnerability, severity_score in zip(
                vulnerabilities, severity_scores
            )
            if severity_score <= max_severity
        ]

    @staticmethod
    def _get_filtered_vulnerabilities_min_severity(
        finding_data: dict[str, Finding],
        min_severity: Decimal,
        vulnerabilities: Iterable[Vulnerability],
    ) -> list[Vulnerability]:
        severity_scores = [
            vulnerability.severity_score.temporal_score
            if vulnerability.severity_score
            else finding_data[
                vulnerability.finding_id
            ].severity_score.temporal_score
            for vulnerability in vulnerabilities
        ]

        return [
            vulnerability
            for vulnerability, severity_score in zip(
                vulnerabilities, severity_scores
            )
            if min_severity <= severity_score
        ]

    @retry_on_exceptions(
        exceptions=(
            ClientConnectorError,
            ClientError,
            ClientPayloadError,
            ConnectionResetError,
            ConnectTimeoutError,
            CustomUnavailabilityError,
            HTTPClientError,
            ReadTimeoutError,
            ServerTimeoutError,
            UnavailabilityError,
        ),
        sleep_seconds=20,
        max_attempts=3,
    )
    async def generate(  # pylint: disable=too-many-locals # noqa: MC0001
        self, data: Iterable[Finding]
    ) -> None:
        filter_finding_title = data
        filter_age = data
        filter_min_severity = data
        filter_max_severity = data
        filter_last_report = data
        filter_min_release_date = self._get_filtered_findings_date(data)
        filter_max_release_date = self._get_filtered_findings(data)
        if self.finding_title:
            filter_finding_title = tuple(
                finding
                for finding in data
                if finding.title.startswith(self.finding_title)
            )
        if self.age is not None:
            filter_age = tuple(
                finding
                for finding in data
                if self._get_first_report_days(finding) <= self.age
            )
        if self.last_report is not None:
            filter_last_report = tuple(
                finding
                for finding in data
                if self._get_last_report_days(finding) <= self.last_report
            )

        filtered_findings_ids: set[str] = set.intersection(
            *[
                set(finding.id for finding in filter_finding_title),
                set(finding.id for finding in filter_age),
                set(finding.id for finding in filter_min_severity),
                set(finding.id for finding in filter_max_severity),
                set(finding.id for finding in filter_last_report),
                set(finding.id for finding in filter_min_release_date),
                set(finding.id for finding in filter_max_release_date),
            ],
        )

        data = tuple(
            finding for finding in data if finding.id in filtered_findings_ids
        )
        findings_ids = [finding.id for finding in data]
        findings_vulnerabilities = await self._get_findings_vulnerabilities(
            findings_ids
        )
        findings_verifications = (
            await self._get_findings_historics_verifications(findings_ids)
        )
        finding_data: dict[str, Finding] = {
            finding.id: finding for finding in data
        }
        finding_verification: dict[str, list[FindingVerification]] = {
            finding.id: verification
            for finding, verification in zip(data, findings_verifications)
        }

        vulnerabilities_filtered = [
            vulnerability
            for vulnerability in findings_vulnerabilities
            if (
                (
                    vulnerability.treatment
                    and vulnerability.treatment.status in self.treatments
                )
                or (not vulnerability.treatment and self.are_all_treatments)
            )
            and vulnerability.state.status in self.states
            and (
                (
                    vulnerability.verification
                    and vulnerability.verification.status in self.verifications
                )
                or self.are_all_verifications
            )
        ]
        if self.closing_date:
            vulnerabilities_filtered = [
                vulnerability
                for vulnerability in vulnerabilities_filtered
                if vulnerability.state.modified_date <= self.closing_date
            ]

        if self.location:
            vulnerabilities_filtered = [
                vulnerability
                for vulnerability in vulnerabilities_filtered
                if vulnerability.state.where.find(self.location) >= 0
            ]

        if self.min_severity is not None:
            vulnerabilities_filtered = (
                self._get_filtered_vulnerabilities_min_severity(
                    finding_data, self.min_severity, vulnerabilities_filtered
                )
            )

        if self.max_severity is not None:
            vulnerabilities_filtered = (
                self._get_filtered_vulnerabilities_max_severity(
                    finding_data, self.max_severity, vulnerabilities_filtered
                )
            )

        vulnereabilities_filtered_and_sorted = sorted(
            vulnerabilities_filtered,
            key=lambda x: x.severity_score.temporal_score
            if x.severity_score
            else finding_data[x.finding_id].severity_score.temporal_score,
            reverse=True,
        )

        vulnerabilities_historics: tuple[
            tuple[
                tuple[VulnerabilityTreatment, ...],
                tuple[VulnerabilityVerification, ...],
            ],
            ...,
        ] = await collect(
            tuple(
                self._get_vulnerability_data(vulnerability)
                for vulnerability in vulnereabilities_filtered_and_sorted
            ),
            workers=8,
        )

        for vulnerability, historics in zip(
            vulnereabilities_filtered_and_sorted, vulnerabilities_historics
        ):
            await self.set_vuln_row(
                vulnerability,
                finding_data[vulnerability.finding_id],
                historics[1],
                historics[0],
                finding_verification[vulnerability.finding_id],
            )
            self.row += 1

    @staticmethod
    def get_measure(metric: str, metric_value: Decimal) -> str:
        """Extract number of CSSV metrics."""
        metrics = {
            "attack_vector": {
                Decimal("0.85"): "Network",
                Decimal("0.62"): "Adjacent",
                Decimal("0.55"): "Local",
                Decimal("0.20"): "Physical",
            },
            "attack_complexity": {
                Decimal("0.77"): "Low",
                Decimal("0.44"): "High",
            },
            "privileges_required": {
                Decimal("0.85"): "None",
                Decimal("0.62"): "Low",
                Decimal("0.68"): "Low",
                Decimal("0.27"): "High",
                Decimal("0.50"): "High",
            },
            "user_interaction": {
                Decimal("0.85"): "None",
                Decimal("0.62"): "Required",
            },
            "severity_scope": {
                Decimal("0.0"): "Unchanged",
                Decimal("1.0"): "Changed",
            },
            "confidentiality_impact": {
                Decimal("0.56"): "High",
                Decimal("0.22"): "Low",
                Decimal("0.0"): "None",
            },
            "integrity_impact": {
                Decimal("0.56"): "High",
                Decimal("0.22"): "Low",
                Decimal("0.0"): "None",
            },
            "availability_impact": {
                Decimal("0.56"): "High",
                Decimal("0.22"): "Low",
                Decimal("0.0"): "None",
            },
            "exploitability": {
                Decimal("0.91"): "Unproven",
                Decimal("0.94"): "Proof of concept",
                Decimal("0.97"): "Functional",
                Decimal("1.0"): "High",
            },
            "remediation_level": {
                Decimal("0.95"): "Official Fix",
                Decimal("0.96"): "Temporary Fix",
                Decimal("0.97"): "Workaround",
                Decimal("1.0"): "Unavailable",
            },
            "report_confidence": {
                Decimal("0.92"): "Unknown",
                Decimal("0.96"): "Reasonable",
                Decimal("1.0"): "Confirmed",
            },
        }
        metric_descriptions = metrics.get(metric, {})

        return metric_descriptions.get(metric_value, EMPTY)

    def get_row_range(self, row: int) -> list[str]:
        # BB is the 54th column
        if self.generate_raw_data:
            return [f"A{row}", f"BB{row}"]

        return [f"A{row}", f"BA{row}"]

    def parse_template(self) -> None:
        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            list(self.vulnerability.keys())
        ]
        self.row += 1

    def save(self) -> None:
        today_date = datetime_utils.get_as_str(
            datetime_utils.get_now(), date_format="%Y-%m-%dT%H-%M-%S"
        )
        self.result_filename = (
            f"{self.group_name}-vulnerabilities-{today_date}.xlsx"
        )
        self.workbook.save(self.result_filename)

    def set_cvss_metrics_cell(
        self, finding: Finding, vulnerability: Vulnerability
    ) -> None:
        cvss_vector = (
            vulnerability.severity_score.cvss_v3
            if vulnerability.severity_score
            else finding.severity_score.cvss_v3
        )
        severity = cvss_utils.parse_cvss_vector_string(cvss_vector)
        cvss_measures = [
            "attack_vector",
            "attack_complexity",
            "privileges_required",
            "user_interaction",
            "severity_scope",
            "confidentiality_impact",
            "integrity_impact",
            "availability_impact",
            "exploitability",
            "remediation_level",
            "report_confidence",
        ]
        cvss_key = "CVSSv3.1 string vector"
        for ind, measure in enumerate(cvss_measures):
            value = self.get_measure(measure, getattr(severity, measure))
            self.row_values[self.vulnerability[cvss_key] + ind + 1] = value

        cvss_calculator_url = (
            f"https://www.first.org/cvss/calculator/3.1#{cvss_vector}"
        )
        cell_content = f'=HYPERLINK("{cvss_calculator_url}", "{cvss_vector}")'
        self.row_values[self.vulnerability[cvss_key]] = (
            cvss_calculator_url if self.generate_raw_data else cell_content
        )

    def get_severity_level(self, temporal_score: Decimal) -> str:
        words = dict(zip(PDFWordlistEn.keys(), PDFWordlistEn.labels()))
        if Decimal("9.0") <= temporal_score <= Decimal("10.0"):
            return words["crit_c"]
        if Decimal("7.0") <= temporal_score <= Decimal("8.9"):
            return words["crit_h"]
        if Decimal("4.0") <= temporal_score <= Decimal("6.9"):
            return words["crit_m"]

        return words["crit_l"]

    def set_severity_cell(
        self, finding: Finding, vulnerability: Vulnerability
    ) -> None:
        temporal_score = (
            vulnerability.severity_score.temporal_score
            if vulnerability.severity_score
            else finding.severity_score.temporal_score
        )
        self.row_values[self.vulnerability["Severity"]] = float(temporal_score)
        self.row_values[self.vulnerability["Severity Level"]] = (
            self.get_severity_level(temporal_score).lstrip("(").rstrip(")")
        )

    async def set_cwe_ids_cell(
        self, finding: Finding, vulnerability: Vulnerability
    ) -> None:
        cwe_ids = (
            vulnerability.cwe_ids
            if vulnerability.cwe_ids
            else await findings_utils.get_finding_criteria_cwe_ids(
                loaders=self.loaders, title=finding.title
            )
        )
        cwe_ids_formatted = "\n".join(cvss_utils.parse_cwe_ids(cwe_ids) or [])
        self.row_values[self.vulnerability["CWE ids"]] = cwe_ids_formatted

    def set_finding_data(self, finding: Finding, vuln: Vulnerability) -> None:
        finding_data = {
            "Description": finding.description,
            "Status": STATE_TRANSLATION[vuln.state.status],
            "Requirements": finding.requirements,
            "Impact": finding.attack_vector_description,
            "Threat": finding.threat,
            "Recommendation": finding.recommendation,
        }
        for key, value in finding_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_reattack_data(
        self,
        vuln: Vulnerability,
        historic_verification: tuple[VulnerabilityVerification, ...],
        finding_verification: tuple[FindingVerification, ...],
    ) -> None:
        reattack_requested = None
        reattack_date = None
        reattack_requester = None
        n_requested_reattacks = None
        remediation_effectiveness: str = EMPTY
        if historic_verification:
            vuln_verification: VulnerabilityVerification = (
                historic_verification[-1]
            )
            reattack_requested = (
                vuln_verification.status
                == VulnerabilityVerificationStatus.REQUESTED
            )
            n_requested_reattacks = len(
                [
                    verification
                    for verification in historic_verification
                    if verification.status
                    == VulnerabilityVerificationStatus.REQUESTED
                ]
            )
            if (
                vuln.state.status == VulnerabilityStateStatus.SAFE
                and n_requested_reattacks
            ):
                effectiveness: float = 100 / n_requested_reattacks
                remediation_effectiveness = (
                    f"{f'{effectiveness:.2f}'.rstrip('0').rstrip('.')}%"
                )
            if reattack_requested and vuln_verification.modified_date:
                reattack_date = datetime_utils.as_zone(
                    vuln_verification.modified_date
                )
                reattack_requester = self._get_reattack_requester(
                    vuln, finding_verification
                )
        reattack_data = {
            "Pending Reattack": "Yes" if reattack_requested else "No",
            "# Requested Reattacks": n_requested_reattacks or "0",
            "Last requested reattack": reattack_date or EMPTY,
            "Last reattack Requester": reattack_requester or EMPTY,
            "Remediation Effectiveness": remediation_effectiveness,
        }
        for key, value in reattack_data.items():
            self.row_values[self.vulnerability[key]] = value

    def set_row_height(self) -> None:
        self.current_sheet.set_row_style(
            self.row,
            Style(size=ROW_HEIGHT, alignment=Alignment(wrap_text=True)),
        )

        # this makes that the cells for severity get the rigth format
        self.current_sheet.set_cell_style(
            self.row,
            9,
            Style(
                size=ROW_HEIGHT,
                alignment=Alignment(wrap_text=True),
                format=Format(0.0),
            ),
        )

    @staticmethod
    def get_first_treatment(
        treatments: tuple[VulnerabilityTreatment, ...]
    ) -> VulnerabilityTreatment | None:
        return next(
            (
                treatment
                for treatment in treatments
                if treatment.status != VulnerabilityTreatmentStatus.UNTREATED
            ),
            None,
        )

    @staticmethod
    def format_treatment(treatment: VulnerabilityTreatmentStatus) -> str:
        if treatment == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED:
            return "Permanently accepted"
        if treatment == VulnerabilityTreatmentStatus.ACCEPTED:
            return "Temporarily accepted"
        if treatment == VulnerabilityTreatmentStatus.UNTREATED:
            return "Untreated"
        return treatment.value.capitalize().replace("_", " ")

    def set_treatment_data(
        self,
        vuln: Vulnerability,
        historic_treatment: tuple[VulnerabilityTreatment, ...],
    ) -> None:
        first_treatment = self.get_first_treatment(historic_treatment)
        current_treatment_data: dict[str, str] = {}
        current_treatment_exp_date = EMPTY
        if vuln.treatment:
            if vuln.treatment.accepted_until:
                current_treatment_exp_date = datetime_utils.get_as_str(
                    vuln.treatment.accepted_until
                )
            current_treatment_data = {
                "Current Treatment": self.format_treatment(
                    vuln.treatment.status
                ),
                "Current Treatment Moment": (
                    datetime_utils.get_as_str(vuln.treatment.modified_date)
                ),
                "Current Treatment Justification": (
                    vuln.treatment.justification or EMPTY
                ),
                "Current Treatment expiration Moment": (
                    current_treatment_exp_date
                ),
                "Current Assigned": vuln.treatment.assigned or EMPTY,
            }
        first_treatment_data = {
            "First Treatment": EMPTY,
            "First Treatment Moment": EMPTY,
            "First Treatment Justification": EMPTY,
            "First Treatment expiration Moment": EMPTY,
            "First Assigned": EMPTY,
        }
        if first_treatment:
            first_expiration = EMPTY
            if (
                first_treatment.status == VulnerabilityTreatmentStatus.ACCEPTED
                and first_treatment.accepted_until
            ):
                first_expiration = datetime_utils.get_as_str(
                    first_treatment.accepted_until
                )
            first_treatment_data = {
                "First Treatment": self.format_treatment(
                    first_treatment.status
                ),
                "First Treatment Moment": datetime_utils.get_as_str(
                    first_treatment.modified_date
                ),
                "First Treatment Justification": first_treatment.justification
                or EMPTY,
                "First Treatment expiration Moment": first_expiration,
                "First Assigned": first_treatment.assigned or EMPTY,
            }

        for key, value in current_treatment_data.items():
            self.row_values[self.vulnerability[key]] = (
                value
                if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
                else EMPTY
            )
            first_treatment_key = key.replace("Current", "First")
            kword = self.vulnerability[first_treatment_key]
            self.row_values[kword] = first_treatment_data[first_treatment_key]

    async def _get_historic_treatment(
        self, vulnerability_id: str
    ) -> tuple[VulnerabilityTreatment, ...]:
        return tuple(
            await self.loaders.vulnerability_historic_treatment.load(
                vulnerability_id
            )
        )

    async def _get_historic_verification(
        self, vulnerability: Vulnerability
    ) -> tuple[VulnerabilityVerification, ...]:
        if not vulnerability.verification:
            return tuple()

        return tuple(
            await self.loaders.vulnerability_historic_verification.load(
                vulnerability.id
            )
        )

    @retry_on_exceptions(
        exceptions=(
            ClientConnectorError,
            ClientError,
            ClientPayloadError,
            ConnectionResetError,
            ConnectTimeoutError,
            CustomUnavailabilityError,
            HTTPClientError,
            ReadTimeoutError,
            ServerTimeoutError,
            UnavailabilityError,
        ),
        sleep_seconds=20,
        max_attempts=10,
    )
    async def _get_vulnerability_data(
        self, vuln: Vulnerability
    ) -> tuple[
        tuple[VulnerabilityTreatment, ...],
        tuple[VulnerabilityVerification, ...],
    ]:
        return (
            await self._get_historic_treatment(vuln.id),
            await self._get_historic_verification(vuln),
        )

    @staticmethod
    def _get_reattack_requester(
        vuln: Vulnerability,
        historic_verification: tuple[FindingVerification, ...],
    ) -> str | None:
        reversed_historic_verification = tuple(reversed(historic_verification))
        for verification in reversed_historic_verification:
            if (
                verification.status == FindingVerificationStatus.REQUESTED
                and verification.vulnerability_ids is not None
                and vuln.id in verification.vulnerability_ids
            ):
                return verification.modified_by
        return None

    async def set_vuln_row(  # pylint: disable=too-many-arguments
        self,
        row: Vulnerability,
        finding: Finding,
        historic_verification: tuple[VulnerabilityVerification, ...],
        historic_treatment: tuple[VulnerabilityTreatment, ...],
        finding_verification: list[FindingVerification],
    ) -> None:
        vuln = self.vulnerability
        specific = row.state.specific
        if row.type == VulnerabilityType.LINES:
            specific = str(int(specific))

        commit = EMPTY
        if row.state.commit:
            commit = row.state.commit[0:7]

        tags = EMPTY
        if row.tags:
            tags = ", ".join(sorted(row.tags))

        stream = EMPTY
        if row.stream:
            stream = " > ".join(row.stream)

        business_critically = EMPTY
        if row.custom_severity:
            business_critically = str(row.custom_severity)

        nickname = EMPTY
        if row.root_id:
            try:
                root = await roots_utils.get_root(
                    self.loaders, row.root_id, finding.group_name
                )
                nickname = root.state.nickname
            except RootNotFound as ex:
                LOGGER.exception(
                    ex,
                    extra=dict(
                        extra=dict(
                            finding_id=finding.id,
                            group_name=row.group_name,
                            root_id=row.root_id,
                            vuln_id=row.id,
                        )
                    ),
                )

        self.row_values[vuln["#"]] = self.row - 1
        self.row_values[vuln["Related Finding"]] = finding.title
        self.row_values[vuln["Finding Id"]] = finding.id
        self.row_values[vuln["Vulnerability Id"]] = row.id
        self.row_values[vuln["Where"]] = row.state.where
        self.row_values[vuln["Business Critically"]] = business_critically
        self.row_values[vuln["Specific"]] = specific
        self.row_values[vuln["Commit Hash"]] = commit
        self.row_values[vuln["Tags"]] = tags
        self.row_values[vuln["Technique"]] = row.technique
        self.row_values[vuln["Stream"]] = stream
        self.row_values[vuln["Root Nickname"]] = nickname
        if self.generate_raw_data:
            self.row_values[vuln["Group"]] = row.group_name

        self.set_finding_data(finding, row)
        self.set_vuln_temporal_data(row)
        self.set_treatment_data(row, historic_treatment)
        self.set_reattack_data(
            row, historic_verification, tuple(finding_verification)
        )
        self.set_cvss_metrics_cell(finding, row)
        self.set_severity_cell(finding, row)
        await self.set_cwe_ids_cell(finding, row)

        self.raw_data.append(self.row_values[1:])
        self.current_sheet.range(*self.get_row_range(self.row)).value = [
            self.row_values[1:]
        ]
        self.set_row_height()

    def set_vuln_temporal_data(self, vuln: Vulnerability) -> None:
        vuln_date = (
            vuln.unreliable_indicators.unreliable_report_date
            or vuln.created_date
        )
        limit_date = datetime_utils.get_utc_now()
        vuln_close_date: str | datetime = EMPTY
        if vuln.state.status == VulnerabilityStateStatus.SAFE:
            limit_date = vuln_close_date = vuln.state.modified_date
        vuln_age_days = int((limit_date - vuln_date).days) if vuln_date else 0
        external_bts = vuln.bug_tracking_system_url or EMPTY

        vuln_temporal_data: dict[str, str | int | float | datetime | None] = {
            "Report Moment": vuln_date,
            "Age in days": vuln_age_days,
            "Close Moment": vuln_close_date,
            "External BTS": external_bts
            if self.generate_raw_data
            else f'=HYPERLINK("{external_bts}", "{external_bts}")',
        }
        for key, value in vuln_temporal_data.items():
            self.row_values[self.vulnerability[key]] = value

    def style_sheet(self) -> None:
        header = self.current_sheet.range(*self.get_row_range(1))
        header.style.fill.background = RED
        header.style.font.color = WHITE
        header.style.alignment.horizontal = "center"
        header.style.alignment.vertical = "center"
        header.style.alignment.wrap_text = True

        for column, col_width in enumerate(
            GroupVulnsReportHeader.widths()
            + (
                OrgVulnsReportHeader.widths() if self.generate_raw_data else []
            ),
            start=1,
        ):
            self.current_sheet.set_col_style(
                column,
                Style(size=col_width, alignment=Alignment(wrap_text=True)),
            )
