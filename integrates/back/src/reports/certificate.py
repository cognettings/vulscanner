from aioextensions import (
    collect,
)
from collections.abc import (
    ValuesView,
)
from custom_utils import (
    datetime as datetime_utils,
)
from custom_utils.reports import (
    get_ordinal_ending,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
import jinja2
from jinja2.utils import (
    select_autoescape,
)
import logging
import matplotlib
from reports.pdf import (
    CreatorPdf,
)
from reports.types import (
    CertFindingInfo,
)
from s3 import (
    operations as s3_ops,
)
from settings.logger import (
    LOGGING,
)
import subprocess  # nosec
import tempfile
from typing import (
    Iterable,
    TypedDict,
)
import uuid

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
CertContext = TypedDict(
    "CertContext",
    {
        "business": str,
        "business_number": str,
        "environment_urls": dict[str, str],
        "has_squad": bool,
        "solution": str,
        "remediation_table": ValuesView[list[int | str]],
        "start_day": str,
        "start_month": str,
        "start_year": str,
        "start_ordinal_ending": str,
        "remediation_rate": str,
        "report_day": str,
        "report_month": str,
        "report_year": str,
        "report_ordinal_ending": str,
        "roots": dict[str, str],
        "signature_img": str,
        "total_risk_exposure": int,
        "words": dict[str, str],
    },
)


async def format_finding(
    loaders: Dataloaders,
    finding: Finding,
) -> CertFindingInfo:
    closed_vulnerabilities = (
        await findings_domain.get_closed_vulnerabilities_len(
            loaders, finding.id
        )
    )
    open_vulnerabilities = await findings_domain.get_open_vulnerabilities_len(
        loaders, finding.id
    )
    risk_exposure = await findings_domain.get_total_open_cvssf(
        loaders, finding.id
    )
    severity_levels = await findings_domain.get_severity_levels_info(
        loaders, finding
    )

    return CertFindingInfo(
        closed_vulnerabilities=closed_vulnerabilities,
        open_vulnerabilities=open_vulnerabilities,
        risk_exposure=risk_exposure,
        severity_levels=severity_levels,
    )


def _set_percentage(total_vulns: int, closed_vulns: int) -> str:
    if total_vulns != 0:
        percentage = closed_vulns * 100.0 / total_vulns
        if percentage == int(percentage):
            return f"{percentage:.0f}%"
        return f"{percentage:.1f}%"
    return "N/A"


def get_created_date(date: datetime | None) -> str:
    if not date:
        return "-"

    return date.strftime("%Y-%m-%d")


async def get_environments_url(
    loaders: Dataloaders, root_id: str
) -> list[dict[str, str]]:
    environments_urls = await loaders.root_environment_urls.load((root_id))
    return [
        {f"{env_url.url}": get_created_date(env_url.created_at)}
        for env_url in environments_urls
    ]


def _format_severity_level(
    findings_info: Iterable[CertFindingInfo], severity_level: str, word: str
) -> list[int | str]:
    total_vulns = sum(
        getattr(finding.severity_levels, severity_level).total
        for finding in findings_info
    )
    closed_vulns = sum(
        getattr(finding.severity_levels, severity_level).closed
        for finding in findings_info
    )
    accepted_vulns = sum(
        getattr(finding.severity_levels, severity_level).accepted
        for finding in findings_info
    )
    remediation_percentage = _set_percentage(total_vulns, closed_vulns)

    return [
        word,
        total_vulns,
        closed_vulns,
        accepted_vulns,
        remediation_percentage,
    ]


def make_remediation_table(
    findings_info: Iterable[CertFindingInfo], words: dict[str, str]
) -> ValuesView[list[int | str]]:
    critical, high, medium, low = (
        words["vuln_c"],
        words["vuln_h"],
        words["vuln_m"],
        words["vuln_l"],
    )
    remediation_dict = {
        critical: _format_severity_level(findings_info, "critical", critical),
        high: _format_severity_level(findings_info, "high", high),
        medium: _format_severity_level(findings_info, "medium", medium),
        low: _format_severity_level(findings_info, "low", low),
    }

    return remediation_dict.values()


def resolve_month_name(
    lang: str, date: datetime, words: dict[str, str]
) -> str:
    if lang.lower() == "en":
        return date.strftime("%B")
    return words[date.strftime("%B").lower()]


class CertificateCreator(CreatorPdf):
    """Class to generate certificates in PDF."""

    cert_context: CertContext

    def __init__(  # pylint: disable=too-many-arguments
        self, lang: str, doctype: str, tempdir: str, group: str, user: str
    ) -> None:
        "Class constructor"
        super().__init__(
            lang, doctype, tempdir, group, user, style="certificate"
        )
        self.proj_tpl = f"templates/pdf/certificate_{lang}.adoc"

    async def fill_context(  # noqa
        self,
        findings: Iterable[Finding],
        group_name: str,
        description: str,
        loaders: Dataloaders,
    ) -> None:
        """Fetch information and fill out the context."""
        words = self.wordlist[self.lang]
        context_findings = await collect(
            [format_finding(loaders, finding) for finding in findings]
        )
        remediation_table = make_remediation_table(context_findings, words)
        group = await groups_domain.get_group(loaders, group_name)
        roots_data = await loaders.group_roots.load(group_name)
        roots = {
            f"{root.state.url} ({root.state.branch})": get_created_date(
                root.created_date
            )
            for root in roots_data
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
        }
        environment_urls = await collect(
            [
                get_environments_url(loaders, root.id)
                for root in roots_data
                if isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            ]
        )
        oldest_vuln_date: (
            datetime | None
        ) = await groups_domain.get_oldest_finding_date(loaders, group_name)
        start_date: datetime = (
            min(group.created_date, oldest_vuln_date)
            if oldest_vuln_date
            else group.created_date
        )
        current_date = datetime_utils.get_utc_now()

        self.cert_context = {
            "business": group.business_name or "",
            "business_number": group.business_id or "",
            "environment_urls": {
                list(env_url.keys())[0]: list(env_url.values())[0]
                for env_urls in environment_urls
                for env_url in env_urls
                if env_url
            },
            "has_squad": group.state.has_squad,
            "remediation_table": remediation_table,
            "start_day": str(start_date.day),
            "start_month": resolve_month_name(self.lang, start_date, words),
            "start_year": str(start_date.year),
            "start_ordinal_ending": get_ordinal_ending(start_date.day),
            "remediation_rate": _set_percentage(
                sum(
                    (
                        finding.open_vulnerabilities
                        + finding.closed_vulnerabilities
                    )
                    for finding in context_findings
                ),
                sum(
                    finding.closed_vulnerabilities
                    for finding in context_findings
                ),
            ),
            "report_day": str(current_date.day),
            "report_month": resolve_month_name(self.lang, current_date, words),
            "report_year": str(current_date.year),
            "report_ordinal_ending": get_ordinal_ending(current_date.day),
            "roots": roots,
            "solution": description,
            "signature_img": "placeholder value",
            "total_risk_exposure": int(
                sum(finding.risk_exposure for finding in context_findings)
            ),
            "words": words,
        }

    async def cert(  # noqa
        self,
        findings: Iterable[Finding],
        group_name: str,
        description: str,
        loaders: Dataloaders,
    ) -> None:
        """Create the template to render and apply the context."""
        await self.fill_context(findings, group_name, description, loaders)
        self.out_name = f"{str(uuid.uuid4())}.pdf"
        searchpath = self.path
        template_loader = jinja2.FileSystemLoader(searchpath=searchpath)
        template_env = jinja2.Environment(
            loader=template_loader,
            autoescape=select_autoescape(["html", "xml"], default=True),
        )
        template = template_env.get_template(self.proj_tpl)
        tpl_name = f"{self.tpl_dir}{group_name}_CERT.tpl"
        # Fetch signature resource
        with tempfile.NamedTemporaryFile(mode="w+") as file:
            await s3_ops.download_file(
                "resources/certificate/signature.png",
                file.name,
            )
            self.cert_context[
                "signature_img"
            ] = f"image::{file.name}[Signature,180,45]"
            render_text = template.render(self.cert_context)
            with open(tpl_name, "wb") as tplfile:
                tplfile.write(render_text.encode("utf-8"))
            self.create_command(tpl_name, self.out_name)
            subprocess.call(self.command, shell=True)  # nosec
