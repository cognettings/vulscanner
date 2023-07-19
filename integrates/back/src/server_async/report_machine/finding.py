from custom_utils import (
    cvss as cvss_utils,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
    FindingMetadataToUpdate,
)
from db_model.findings.update import (
    update_metadata,
)
from dynamodb.types import (
    Item,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingAttributesToAdd,
)


async def update_finding_metadata(
    finding_data: tuple[str, str, str],
    finding: Finding,
    criteria_vulnerability: Item,
    criteria_requirements: Item,
) -> None:
    group_name, vulnerability_id, language = finding_data
    language = language.lower()
    current_attrs = FindingMetadataToUpdate(
        attack_vector_description=finding.attack_vector_description,
        description=finding.description,
        min_time_to_remediate=finding.min_time_to_remediate,
        recommendation=finding.recommendation,
        requirements=finding.requirements,
        severity=finding.severity,
        severity_score=finding.severity_score,
        threat=finding.threat,
        title=finding.title,
    )
    cvss3_vector = cvss_utils.get_criteria_cvss_vector(criteria_vulnerability)
    severity_legacy = cvss_utils.parse_cvss_vector_string(cvss3_vector)

    updated_attrs = FindingMetadataToUpdate(
        attack_vector_description=criteria_vulnerability[language]["impact"],
        description=criteria_vulnerability[language]["description"],
        min_time_to_remediate=int(criteria_vulnerability["remediation_time"]),
        recommendation=criteria_vulnerability[language]["recommendation"],
        requirements="\n".join(
            [
                criteria_requirements[item][language]["title"]
                for item in criteria_vulnerability["requirements"]
            ]
        ),
        severity=severity_legacy,
        severity_score=cvss_utils.get_severity_score_from_cvss_vector(
            cvss3_vector
        ),
        threat=criteria_vulnerability[language]["threat"],
        title=(
            f"{vulnerability_id}. {criteria_vulnerability[language]['title']}"
        ),
    )

    if current_attrs != updated_attrs:
        await update_metadata(
            group_name=group_name,
            finding_id=finding.id,
            metadata=updated_attrs,
        )


async def create_finding(
    loaders: Dataloaders,
    group_name: str,
    vulnerability_id: str,
    language: str,
    criteria_vulnerability: Item,
) -> Finding:
    language = language.lower()
    cvss3_vector = cvss_utils.get_criteria_cvss_vector(criteria_vulnerability)
    severity_legacy = cvss_utils.parse_cvss_vector_string(cvss3_vector)
    return await findings_domain.add_finding(
        loaders=loaders,
        group_name=group_name,
        stakeholder_email="machine@fluidattacks.com",
        attributes=FindingAttributesToAdd(
            attack_vector_description=criteria_vulnerability[language][
                "impact"
            ],
            description=criteria_vulnerability[language]["description"],
            min_time_to_remediate=criteria_vulnerability["remediation_time"],
            recommendation=criteria_vulnerability[language]["recommendation"],
            severity=severity_legacy,
            severity_score=cvss_utils.get_severity_score_from_cvss_vector(
                cvss3_vector
            ),
            source=Source.MACHINE,
            threat=criteria_vulnerability[language]["threat"],
            title=(
                f"{vulnerability_id}."
                f" {criteria_vulnerability[language]['title']}"
            ),
            unfulfilled_requirements=criteria_vulnerability["requirements"],
        ),
        is_from_machine=True,
    )


def filter_same_findings(
    criteria_vuln_id: str, finding: Finding, same_type_of_findings: list
) -> None:
    if finding.title.startswith(f"{criteria_vuln_id}."):
        same_type_of_findings.append(finding)


def split_target_findings(
    same_type_of_findings: tuple[Finding, ...],
) -> tuple[Finding | None, tuple[Finding, ...]]:
    target_finding = None
    non_target_findings: list[Finding] = []
    for finding in sorted(
        same_type_of_findings,
        key=lambda x: x.creation.modified_date.timestamp()
        if x.creation
        else 0,
    ):
        if (
            finding.creation
            and finding.creation.modified_by == "machine@fluidattacks.com"
        ):
            target_finding = target_finding or finding
        else:
            non_target_findings.append(finding)
    return target_finding, tuple(non_target_findings)
