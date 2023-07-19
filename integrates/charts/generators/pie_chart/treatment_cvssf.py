from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    TREATMENT,
)
from charts.generators.pie_chart.utils import (
    generate_all,
)
from collections import (
    Counter,
)
from custom_utils import (
    cvss as cvss_utils,
)
from custom_utils.findings import (
    get_group_findings,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)

Treatment = NamedTuple(
    "Treatment",
    [
        ("acceptedUndefined", int),
        ("accepted", int),
        ("inProgress", int),
        ("undefined", int),
    ],
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Treatment:
    loaders = get_new_context()
    group_findings = await get_group_findings(
        group_name=group, loaders=loaders
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: cvss_utils.get_cvssf_score(
            cvss_utils.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }

    vulnerabilities = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            finding_ids
        )
    )

    treatments: tuple[Counter[VulnerabilityTreatmentStatus], ...] = tuple(
        Counter(
            {
                vulnerability.treatment.status: Decimal(
                    finding_cvssf[vulnerability.finding_id]
                ).quantize(Decimal("0.001"))
            }
        )
        for vulnerability in vulnerabilities
        if vulnerability.treatment
        and vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    treatment: Counter[VulnerabilityTreatmentStatus] = sum(
        treatments, Counter()
    )

    return Treatment(
        acceptedUndefined=treatment[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        accepted=treatment[VulnerabilityTreatmentStatus.ACCEPTED],
        inProgress=treatment[VulnerabilityTreatmentStatus.IN_PROGRESS],
        undefined=treatment[VulnerabilityTreatmentStatus.UNTREATED],
    )


async def get_data_many_groups(groups: tuple[str, ...]) -> Treatment:
    groups_data: tuple[Treatment, ...] = await collect(
        map(get_data_one_group, groups), workers=32
    )

    return Treatment(
        acceptedUndefined=sum(
            group.acceptedUndefined for group in groups_data
        ),
        accepted=sum(group.accepted for group in groups_data),
        inProgress=sum(group.inProgress for group in groups_data),
        undefined=sum(group.undefined for group in groups_data),
    )


def format_data(data: Treatment) -> dict:
    translations: dict[str, str] = {
        "acceptedUndefined": "Permanently accepted",
        "accepted": "Temporarily accepted",
        "inProgress": "In progress",
        "undefined": "Untreated",
    }

    return {
        "data": {
            "columns": [
                [value, str(getattr(data, key))]
                for key, value in translations.items()
            ],
            "type": "pie",
            "colors": {
                "Permanently accepted": TREATMENT.more_passive,
                "Temporarily accepted": TREATMENT.passive,
                "In progress": TREATMENT.neutral,
                "Untreated": TREATMENT.more_agressive,
            },
        },
        "legend": {
            "position": "right",
        },
        "pie": {
            "label": {
                "show": True,
            },
        },
    }


if __name__ == "__main__":
    run(
        generate_all(
            get_data_one_group=get_data_one_group,
            get_data_many_groups=get_data_many_groups,
            format_document=format_data,
            header=["Treatment", "CVSSF"],
        )
    )
