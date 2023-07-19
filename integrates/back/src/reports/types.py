from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from findings.types import (
    SeverityLevelsInfo,
)
from typing import (
    NamedTuple,
)
from vulnerabilities.types import (
    GroupedVulnerabilitiesInfo,
)


# XLS reports types definitions
class ColumnConfig(NamedTuple):
    label: str
    width: int = -1


class GenericHeader(Enum):
    @classmethod
    def labels(cls) -> list[str]:
        return [member.value.label for member in cls]

    @classmethod
    def widths(cls) -> list[int]:
        return [member.value.width for member in cls]


class OrgVulnsReportHeader(GenericHeader):
    GROUP: ColumnConfig = ColumnConfig(label="Group", width=65)


class GroupVulnsReportHeader(GenericHeader):
    NUMBER: ColumnConfig = ColumnConfig(label="#", width=4)
    FINDING: ColumnConfig = ColumnConfig(label="Related Finding", width=55)
    FINDING_ID: ColumnConfig = ColumnConfig(label="Finding Id", width=25)
    VULNERABILITY_ID: ColumnConfig = ColumnConfig(
        label="Vulnerability Id", width=50
    )
    WHERE: ColumnConfig = ColumnConfig(label="Where", width=45)
    STREAM: ColumnConfig = ColumnConfig(label="Stream", width=45)
    SPECIFIC: ColumnConfig = ColumnConfig(label="Specific", width=38)
    DESCRIPTION: ColumnConfig = ColumnConfig(label="Description", width=95)
    STATUS: ColumnConfig = ColumnConfig(label="Status", width=13)
    SEVERITY: ColumnConfig = ColumnConfig("Severity", width=13)
    REQUIREMENTS: ColumnConfig = ColumnConfig(label="Requirements", width=100)
    IMPACT: ColumnConfig = ColumnConfig(label="Impact", width=65)
    THREAT: ColumnConfig = ColumnConfig(label="Threat", width=55)
    RECOMMENDATION: ColumnConfig = ColumnConfig(
        label="Recommendation", width=100
    )
    EXTERNAL_BTS: ColumnConfig = ColumnConfig(label="External BTS", width=80)
    COMPROMISED_ATTRS: ColumnConfig = ColumnConfig(
        label="Compromised Attributes", width=35
    )
    TAGS: ColumnConfig = ColumnConfig(label="Tags", width=60)
    BUSINESS_CRITICALLY: ColumnConfig = ColumnConfig(
        label="Business Critically", width=25
    )
    TECHNIQUE: ColumnConfig = ColumnConfig(label="Technique", width=25)
    REPORT_MOMENT: ColumnConfig = ColumnConfig(label="Report Moment", width=25)
    CLOSE_MOMENT: ColumnConfig = ColumnConfig(label="Close Moment", width=25)
    AGE: ColumnConfig = ColumnConfig(label="Age in days", width=20)
    FIRST_TREATMENT: ColumnConfig = ColumnConfig(
        label="First Treatment", width=20
    )
    FIRST_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label="First Treatment Moment", width=25
    )
    FIRST_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label="First Treatment Justification", width=95
    )
    FIRST_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label="First Treatment expiration Moment", width=40
    )
    FIRST_ASSIGNED: ColumnConfig = ColumnConfig(
        label="First Assigned", width=35
    )
    CURRENT_TREATMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment", width=20
    )
    CURRENT_TREATMENT_MOMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment Moment", width=25
    )
    CURRENT_TREATMENT_JUSTIFICATION: ColumnConfig = ColumnConfig(
        label="Current Treatment Justification", width=95
    )
    CURRENT_TREATMENT_EXP_MOMENT: ColumnConfig = ColumnConfig(
        label="Current Treatment expiration Moment", width=40
    )
    CURRENT_ASSIGNED: ColumnConfig = ColumnConfig(
        label="Current Assigned", width=35
    )
    PENDING_REATTACK: ColumnConfig = ColumnConfig(
        label="Pending Reattack", width=25
    )
    N_REQUESTED_REATTACKS: ColumnConfig = ColumnConfig(
        label="# Requested Reattacks", width=25
    )
    REMEDIATION_EFFECTIVENESS: ColumnConfig = ColumnConfig(
        label="Remediation Effectiveness", width=25
    )
    LAST_REQUESTED_REATTACK: ColumnConfig = ColumnConfig(
        label="Last requested reattack", width=25
    )
    LAST_REATTACK_REQUESTER: ColumnConfig = ColumnConfig(
        label="Last reattack Requester", width=35
    )
    CVSS_VECTOR: ColumnConfig = ColumnConfig(
        label="CVSSv3.1 string vector", width=55
    )
    ATTACK_VECTOR: ColumnConfig = ColumnConfig(label="Attack Vector", width=18)
    ATTACK_COMPLEXITY: ColumnConfig = ColumnConfig(
        label="Attack Complexity", width=20
    )
    PRIVILEGES_REQUIRED: ColumnConfig = ColumnConfig(
        label="Privileges Required", width=25
    )
    USER_INTERACTION: ColumnConfig = ColumnConfig(
        label="User Interaction", width=20
    )
    SEVERITY_SCOPE: ColumnConfig = ColumnConfig(
        label="Severity Scope", width=20
    )
    CONFIDENTIALITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Confidentiality Impact", width=23
    )
    INTEGRITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Integrity Impact", width=20
    )
    AVAILABILITY_IMPACT: ColumnConfig = ColumnConfig(
        label="Availability Impact", width=20
    )
    EXPLOITABILITY: ColumnConfig = ColumnConfig(
        label="Exploitability", width=18
    )
    REMEDIATION_LEVEL: ColumnConfig = ColumnConfig(
        label="Remediation Level", width=25
    )
    REPORT_CONFIDENCE: ColumnConfig = ColumnConfig(
        label="Report Confidence", width=25
    )
    CWE_IDS: ColumnConfig = ColumnConfig(label="CWE ids", width=20)
    COMMIT_HASH: ColumnConfig = ColumnConfig(label="Commit Hash", width=25)
    ROOT_NICKNAME: ColumnConfig = ColumnConfig(label="Root Nickname", width=25)
    SEVERITY_LEVEL: ColumnConfig = ColumnConfig("Severity Level", width=18)


# PDF report types definitions


class PdfFindingInfo(NamedTuple):
    attack_vector_description: str
    closed_vulnerabilities: int
    description: str
    evidence_set: list[dict[str, str]]
    grouped_inputs_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_lines_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    grouped_ports_vulnerabilities: tuple[GroupedVulnerabilitiesInfo, ...]
    open_vulnerabilities: int
    recommendation: str
    requirements: str
    severity_score: Decimal
    state: str
    title: str
    threat: str
    treatment: str
    where: str


class CertFindingInfo(NamedTuple):
    closed_vulnerabilities: int
    open_vulnerabilities: int
    risk_exposure: Decimal
    severity_levels: SeverityLevelsInfo


class UnfulfilledRequirementInfo(NamedTuple):
    description: str
    id: str
    title: str


class UnfulfilledStandardInfo(NamedTuple):
    standard_id: str
    title: str
    summary: str
    unfulfilled_requirements: list[UnfulfilledRequirementInfo]


class WordlistItem(NamedTuple):
    key: str
    label: str | list[str]


class Wordlist(Enum):
    @classmethod
    def keys(cls) -> list[str]:
        return [member.value.key for member in cls]

    @classmethod
    def labels(cls) -> list[str]:
        return [member.value.label for member in cls]


class PDFWordlistEn(Wordlist):
    ACCEPTED_VULNS_TITLE: WordlistItem = WordlistItem(
        "accepted_vulns_title", "Accepted Vulnerabilities"
    )
    ATTACK_VECTOR_TITLE: WordlistItem = WordlistItem(
        "attack_vector_title", "Attack Vector"
    )
    CARDINALITY_TITLE: WordlistItem = WordlistItem(
        "cardinality_title", "Vulnerabilities"
    )
    CLOSED_VULNS_TITLE: WordlistItem = WordlistItem(
        "closed_vulns_title", "Remediated Vulnerabilities"
    )
    CODE_REPOSITORY: WordlistItem = WordlistItem(
        "code_repository", "Code Repository"
    )
    COMMIT_HASH: WordlistItem = WordlistItem("commit_hash", "Commit Hash")
    CONTENT_LIST: WordlistItem = WordlistItem(
        "content_list",
        [
            "1. Goals",
            "2. Scope",
            "3. Finding Table",
            "4. General View",
            "5. Findings Summary",
        ],
    )
    CONTENT_TITLE: WordlistItem = WordlistItem("content_title", "Content")
    CRIT_C: WordlistItem = WordlistItem("crit_c", "(Critical)")
    CRIT_H: WordlistItem = WordlistItem("crit_h", "(High)")
    CRIT_L: WordlistItem = WordlistItem("crit_l", "(Low)")
    CRIT_M: WordlistItem = WordlistItem("crit_m", "(Medium)")
    DATE_ADDED: WordlistItem = WordlistItem("date_added", "Date Added")
    DESCRIPTION_TITLE: WordlistItem = WordlistItem(
        "description_title", "Vulnerability"
    )
    ENVIRONMENT: WordlistItem = WordlistItem("environment", "Environment")
    EVIDENCE_TITLE: WordlistItem = WordlistItem("evidence_title", "Evidences")
    EXECUTIVE: WordlistItem = WordlistItem("executive", "Executive Report")
    FIELD: WordlistItem = WordlistItem("field", "Field")
    FIN_STATUS_CLOSED: WordlistItem = WordlistItem("fin_status_closed", "Safe")
    FIN_STATUS_OPEN: WordlistItem = WordlistItem(
        "fin_status_open", "Vulnerable"
    )
    FINDING_NUMBER_TITLE: WordlistItem = WordlistItem(
        "finding_number_title", "Number of Findings"
    )
    FINDING_SECTION_TITLE: WordlistItem = WordlistItem(
        "finding_section_title", "Summary"
    )
    FINDING_TITLE: WordlistItem = WordlistItem("finding_title", "Finding")
    GOALS_TITLE: WordlistItem = WordlistItem("goals_title", "Goals")
    INPUTS: WordlistItem = WordlistItem("inputs", "Inputs")
    LINE: WordlistItem = WordlistItem("line", "Line")
    LINES: WordlistItem = WordlistItem("lines", "Lines")
    METHODOLOGY_TITLE: WordlistItem = WordlistItem(
        "metodology_title", "Methodology"
    )
    PATH: WordlistItem = WordlistItem("path", "Path")
    PORT: WordlistItem = WordlistItem("port", "Port")
    PORTS: WordlistItem = WordlistItem("ports", "Ports")
    RECORDS_TITLE: WordlistItem = WordlistItem("records_title", "Records")
    REQUISITE_TITLE: WordlistItem = WordlistItem(
        "requisite_title", "Requirement"
    )
    REQUIREMENT: WordlistItem = WordlistItem("requirement", "Requirement")
    RESUME_PAGE_TITLE: WordlistItem = WordlistItem(
        "resume_page_title", "General View"
    )
    RESUME_PERC_MULTILINE_TITLE: WordlistItem = WordlistItem(
        "resume_perc_multiline_title",
        """Remediation +
        Rate""",
    )
    RESUME_PERC_TITLE: WordlistItem = WordlistItem(
        "resume_perc_title", "Remediation Rate"
    )
    RESUME_TABLE_TITLE: WordlistItem = WordlistItem(
        "resume_table_title", "Finding Table"
    )
    RESUME_TOP_TITLE: WordlistItem = WordlistItem(
        "resume_top_title", "Finding Top"
    )
    RESUME_TTAB_TITLE: WordlistItem = WordlistItem("resume_ttab_title", "Name")
    RESUME_VNAME_TITLE: WordlistItem = WordlistItem(
        "resume_vname_title", "Name"
    )
    RESUME_VNUM_TITLE: WordlistItem = WordlistItem("resume_vnum_title", "#")
    RESUME_VULN_TITLE: WordlistItem = WordlistItem(
        "resume_vuln_title", "Vulnerabilities"
    )
    ROOT_ADDRESS: WordlistItem = WordlistItem("root_address", "Address")
    ROOT_BRANCH: WordlistItem = WordlistItem("root_branch", "Branch")
    ROOT_ENVIRONMENT_TITLE: WordlistItem = WordlistItem(
        "root_environment_title", "Environment URLs"
    )
    ROOT_GIT_TITLE: WordlistItem = WordlistItem("root_git_title", "Git Roots")
    ROOT_HOST: WordlistItem = WordlistItem("root_host", "Host")
    ROOT_IP_TITLE: WordlistItem = WordlistItem("root_ip_title", "IP Roots")
    ROOT_NICKNAME: WordlistItem = WordlistItem("root_nickname", "Nickname")
    ROOT_SCOPE_TITLE: WordlistItem = WordlistItem("root_scope_title", "Scope")
    ROOT_STATE_TITLE: WordlistItem = WordlistItem("root_state", "State")
    ROOT_URL_TITLE: WordlistItem = WordlistItem("root_url_title", "URL Roots")
    ROOT_URL: WordlistItem = WordlistItem("root_url", "URL")
    SEVERITY_MULTILINE_TITLE: WordlistItem = WordlistItem(
        "severity_multiline_title",
        """Severity +
        (CVSS{nbsp}3.1)""",
    )
    SEVERITY_TITLE: WordlistItem = WordlistItem(
        "severity_title", "Severity (CVSS{nbsp}3.1)"
    )
    SOLUTION_TITLE: WordlistItem = WordlistItem("solution_title", "Solution")
    STANDARD: WordlistItem = WordlistItem("standard", "Standard")
    STATE_TITLE: WordlistItem = WordlistItem("state_title", "Status")
    TECH: WordlistItem = WordlistItem("tech", "Technical Report")
    UNFULFILLED_STANDARDS: WordlistItem = WordlistItem(
        "unfulfilled_standards", "Unfulfilled Standards"
    )
    THREAT_TITLE: WordlistItem = WordlistItem("threat_title", "Threat")
    TOTAL_VULNS_TITLE: WordlistItem = WordlistItem(
        "total_vulns_title", "Reported Vulnerabilities"
    )
    TREAT_PERMANENTLY_ASU: WordlistItem = WordlistItem(
        "treat_per_asu", "Permanently Accepted"
    )
    TREAT_STATUS_ASU: WordlistItem = WordlistItem(
        "treat_status_asu", "Temporarily Accepted"
    )
    TREAT_STATUS_REM: WordlistItem = WordlistItem(
        "treat_status_rem", "In Progress"
    )
    TREAT_STATUS_WOR: WordlistItem = WordlistItem(
        "treat_status_wor", "Untreated"
    )
    TREATMENT_TITLE: WordlistItem = WordlistItem(
        "treatment_title", "Treatment"
    )
    VULN_C: WordlistItem = WordlistItem(
        "vuln_c", "Critical (9.0{nbsp}-{nbsp}10.0)"
    )
    VULN_H: WordlistItem = WordlistItem("vuln_h", "High (7.0{nbsp}-{nbsp}8.9)")
    VULN_L: WordlistItem = WordlistItem("vuln_l", "Low (0.1{nbsp}-{nbsp}3.9)")
    VULN_M: WordlistItem = WordlistItem("vuln_m", "Medium (4.0 - 6.9)")
    VULN_C_PLAIN: WordlistItem = WordlistItem("vuln_c_plain", "Critical")
    VULN_H_PLAIN: WordlistItem = WordlistItem("vuln_h_plain", "High")
    VULN_L_PLAIN: WordlistItem = WordlistItem("vuln_l_plain", "Low")
    VULN_M_PLAIN: WordlistItem = WordlistItem("vuln_m_plain", "Medium")
    WHERE_TITLE: WordlistItem = WordlistItem("where_title", "Where")


class PDFWordlistEs(Wordlist):
    ACCEPTED_VULNS_TITLE: WordlistItem = WordlistItem(
        "accepted_vulns_title", "Vulnerabilidades Aceptadas"
    )
    ATTACK_VECTOR_TITLE: WordlistItem = WordlistItem(
        "attack_vector_title", "Vector de ataque"
    )
    CARDINALITY_TITLE: WordlistItem = WordlistItem(
        "cardinality_title", "Vulnerabilidades"
    )
    CODE_REPOSITORY: WordlistItem = WordlistItem(
        "code_repository", "Repositorio"
    )
    COMMIT_HASH: WordlistItem = WordlistItem("commit_hash", "Commit Hash")
    CONTENT_LIST: WordlistItem = WordlistItem(
        "content_list",
        [
            "1. Metas",
            "2. Alcance",
            "3. Tabla de hallazgos",
            "4. Visión general",
            "5. Resumen de hallazgos",
        ],
    )
    CONTENT_TITLE: WordlistItem = WordlistItem("content_title", "Contenido")
    CRIT_C: WordlistItem = WordlistItem("crit_c", "(Crítico)")
    CRIT_H: WordlistItem = WordlistItem("crit_h", "(Alto)")
    CRIT_L: WordlistItem = WordlistItem("crit_l", "(Bajo)")
    CRIT_M: WordlistItem = WordlistItem("crit_m", "(Medio)")
    CLOSED_VULNS_TITLE: WordlistItem = WordlistItem(
        "closed_vulns_title", "Vulnerabilidades Remediadas"
    )
    DATE_ADDED: WordlistItem = WordlistItem("date_added", "Fecha de adición")
    DESCRIPTION_TITLE: WordlistItem = WordlistItem(
        "description_title", "Vulnerabilidad"
    )
    ENVIRONMENT: WordlistItem = WordlistItem("environment", "Ambiente")
    EVIDENCE_TITLE: WordlistItem = WordlistItem("evidence_title", "Evidencias")
    EXECUTIVE: WordlistItem = WordlistItem("executive", "Reporte Ejecutivo")
    FIELD: WordlistItem = WordlistItem("field", "Campo")
    FIN_STATUS_CLOSED: WordlistItem = WordlistItem(
        "fin_status_closed", "Seguro"
    )
    FIN_STATUS_OPEN: WordlistItem = WordlistItem(
        "fin_status_open", "Vulnerable"
    )
    FINDING_NUMBER_TITLE: WordlistItem = WordlistItem(
        "finding_number_title", "Cantidad de Tipologías"
    )
    FINDING_SECTION_TITLE: WordlistItem = WordlistItem(
        "finding_section_title", "Resumen"
    )
    FINDING_TITLE: WordlistItem = WordlistItem("finding_title", "Hallazgo")
    GOALS_TITLE: WordlistItem = WordlistItem("goals_title", "Metas")
    INPUTS: WordlistItem = WordlistItem("inputs", "Entradas")
    LINE: WordlistItem = WordlistItem("line", "Línea")
    LINES: WordlistItem = WordlistItem("lines", "Líneas")
    METHODOLOGY_TITLE: WordlistItem = WordlistItem(
        "metodology_title", "Metodología"
    )
    PATH: WordlistItem = WordlistItem("path", "Dirección")
    PORT: WordlistItem = WordlistItem("port", "Puerto")
    PORTS: WordlistItem = WordlistItem("ports", "Puertos")
    RECORDS_TITLE: WordlistItem = WordlistItem("records_title", "Registros")
    REQUISITE_TITLE: WordlistItem = WordlistItem(
        "requisite_title", "Requisito"
    )
    REQUIREMENT: WordlistItem = WordlistItem("requirement", "Requisito")
    RESUME_PERC_MULTILINE_TITLE: WordlistItem = WordlistItem(
        "resume_perc_multiline_title",
        """Porcentaje de +
        Remediación""",
    )
    RESUME_PERC_TITLE: WordlistItem = WordlistItem(
        "resume_perc_title", "Porcentaje de Remediación"
    )
    RESUME_PAGE_TITLE: WordlistItem = WordlistItem(
        "resume_page_title", "Vista General"
    )
    RESUME_TABLE_TITLE: WordlistItem = WordlistItem(
        "resume_table_title", "Tabla de Hallazgos"
    )
    RESUME_TOP_TITLE: WordlistItem = WordlistItem(
        "resume_top_title", "Top Hallazgo"
    )
    RESUME_TTAB_TITLE: WordlistItem = WordlistItem(
        "resume_ttab_title", "Nombre"
    )
    RESUME_VNAME_TITLE: WordlistItem = WordlistItem(
        "resume_vname_title", "Nombre"
    )
    RESUME_VNUM_TITLE: WordlistItem = WordlistItem("resume_vnum_title", "#")
    RESUME_VULN_TITLE: WordlistItem = WordlistItem(
        "resume_vuln_title", "Vulnerabilidades"
    )
    ROOT_ADDRESS: WordlistItem = WordlistItem("root_address", "Dirección")
    ROOT_BRANCH: WordlistItem = WordlistItem("root_branch", "Rama")
    ROOT_ENVIRONMENT_TITLE: WordlistItem = WordlistItem(
        "root_environment_title", "URLs del entorno"
    )
    ROOT_GIT_TITLE: WordlistItem = WordlistItem("root_git_title", "Raíces Git")
    ROOT_HOST: WordlistItem = WordlistItem("root_host", "Host")
    ROOT_IP_TITLE: WordlistItem = WordlistItem("root_ip_title", "Raíces IP")
    ROOT_NICKNAME: WordlistItem = WordlistItem("root_nickname", "Nickname")
    ROOT_SCOPE_TITLE: WordlistItem = WordlistItem(
        "root_scope_title", "Alcance"
    )
    ROOT_STATE_TITLE: WordlistItem = WordlistItem("root_state", "Estado")
    ROOT_URL_TITLE: WordlistItem = WordlistItem("root_url_title", "Raíces URL")
    ROOT_URL: WordlistItem = WordlistItem("root_url", "URL")
    SOLUCION_TITLE: WordlistItem = WordlistItem("solution_title", "Solución")
    STANDARD: WordlistItem = WordlistItem("standard", "Estándar")
    STATE_TITLE: WordlistItem = WordlistItem("state_title", "Estado")
    TECH: WordlistItem = WordlistItem("tech", "Reporte Técnico")
    UNFULFILLED_STANDARDS: WordlistItem = WordlistItem(
        "unfulfilled_standards", "Estándares Incumplidos"
    )
    SEVERITY_MULTILINE_TITLE: WordlistItem = WordlistItem(
        "severity_multiline_title",
        """Severidad +
        (CVSS{nbsp}3.1)""",
    )
    SEVERITY_TITLE: WordlistItem = WordlistItem(
        "severity_title", "Severidad (CVSS{nbsp}3.1)"
    )
    TOTAL_VULNS_TITLE: WordlistItem = WordlistItem(
        "total_vulns_title", "Vulnerabilidades Reportadas"
    )
    THREAT_TITLE: WordlistItem = WordlistItem("threat_title", "Amenaza")
    TREAT_PERMANENTLY_ASU: WordlistItem = WordlistItem(
        "treat_per_asu", "Permanently Accepted"
    )
    TREAT_STATUS_ASU: WordlistItem = WordlistItem(
        "treat_status_asu", "Temporarily Accepted"
    )
    TREAT_STATUS_REM: WordlistItem = WordlistItem(
        "treat_status_rem", "In Progress"
    )
    TREAT_STATUS_WOR: WordlistItem = WordlistItem(
        "treat_status_wor", "Untreated"
    )
    TREATMENT_TITLE: WordlistItem = WordlistItem(
        "treatment_title", "Tratamiento"
    )
    VULN_C: WordlistItem = WordlistItem(
        "vuln_c", "Crítica (9.0{nbsp}-{nbsp}10.0)"
    )
    VULN_H: WordlistItem = WordlistItem("vuln_h", "Alta (7.0{nbsp}-{nbsp}8.9)")
    VULN_L: WordlistItem = WordlistItem("vuln_l", "Baja (0.1{nbsp}-{nbsp}3.9)")
    VULN_M: WordlistItem = WordlistItem(
        "vuln_m", "Media (4.0{nbsp}-{nbsp}6.9)"
    )
    VULN_C_PLAIN: WordlistItem = WordlistItem("vuln_c_plain", "Crítica")
    VULN_H_PLAIN: WordlistItem = WordlistItem("vuln_h_plain", "Alta")
    VULN_L_PLAIN: WordlistItem = WordlistItem("vuln_l_plain", "Baja")
    VULN_M_PLAIN: WordlistItem = WordlistItem("vuln_m_plain", "Media")
    WHERE_TITLE: WordlistItem = WordlistItem("where_title", "Donde")
    # To avoid setlocale's global effects, we'll have to support these names
    JANUARY: WordlistItem = WordlistItem("january", "Enero")
    FEBRUARY: WordlistItem = WordlistItem("february", "Febrero")
    MARCH: WordlistItem = WordlistItem("march", "Marzo")
    APRIL: WordlistItem = WordlistItem("april", "Abril")
    MAY: WordlistItem = WordlistItem("may", "Mayo")
    JUNE: WordlistItem = WordlistItem("june", "Junio")
    JULY: WordlistItem = WordlistItem("july", "Julio")
    AUGUST: WordlistItem = WordlistItem("august", "Agosto")
    SEPTEMBER: WordlistItem = WordlistItem("september", "Septiembre")
    OCTOBER: WordlistItem = WordlistItem("october", "Octubre")
    NOVEMBER: WordlistItem = WordlistItem("november", "Noviembre")
    DECEMBER: WordlistItem = WordlistItem("december", "Diciembre")
