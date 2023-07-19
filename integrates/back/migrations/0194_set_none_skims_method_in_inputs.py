# type: ignore

# pylint: disable=invalid-name
"""
Set skims_method for INPUTS vulnerabilities based on
0194_set_none_skims_method_in_inputs.yaml

Execution Time:    2022-02-22 at 21:31:28 UTC
Finalization Time: 2022-02-22 at 22:40:15 UTC
"""


from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from groups.domain import (
    get_active_groups,
)
import logging
from settings import (
    LOGGING,
)
from time import (
    strftime as format_time,
)
import yaml

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Element = tuple[Finding, Vulnerability]


def read_yaml(file_name: str) -> dict[object, object]:
    with open(file_name, "r", encoding="utf8") as f:
        data = yaml.safe_load(f)
    return data


def vuln_is_machine(vuln: Vulnerability) -> bool:
    return vuln.state.source == Source.MACHINE


def vuln_is_input(vuln: Vulnerability) -> bool:
    return vuln.type == VulnerabilityType.INPUTS


def meth_is_none(vuln: Vulnerability) -> bool:
    return vuln.skims_method is None


async def vulns_to_update(
    loaders: Dataloaders, group: str
) -> tuple[Vulnerability, ...]:
    raw_findings = await loaders.group_findings.load(group)
    f_ids = (finding.id for finding in raw_findings)
    return tuple(
        v
        for v in await loaders.finding_vulnerabilities.load_many_chained(f_ids)
        if vuln_is_machine(v) and vuln_is_input(v) and meth_is_none(v)
    )


def get_method(vuln: Vulnerability, methods: dict[str, str]) -> str | None:
    for specific in methods:
        if specific in vuln.specific:
            return methods[specific]
    return None


async def process_group(
    loaders: Dataloaders, group: str, methods: dict[str, str], progress: float
) -> None:
    # pylint: disable=logging-fstring-interpolation

    total = 0
    for vuln in await vulns_to_update(loaders, group):
        total += 1

        if skims_method := get_method(vuln, methods):
            await update_metadata(
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    skims_method=skims_method,
                ),
            )
        else:
            LOGGER_CONSOLE.info(
                f"specific not founded: {vuln.specific}",
                extra={"extra": vuln.id},
            )

    LOGGER_CONSOLE.info(
        f"progress: {progress:.2f}%, vulns updated: {total}",
        extra={"extra": group},
    )


async def main() -> None:
    loaders = get_new_context()
    groups = await get_active_groups()
    n_groups = len(groups)

    methods = read_yaml("0194_set_none_skims_method_in_inputs.yaml")

    await collect(
        tuple(
            process_group(loaders, group, methods, count / n_groups * 100)
            for count, group in enumerate(groups)
        ),
        workers=10,
    )


if __name__ == "__main__":
    print(format_time("Execution Time:    %Y-%m-%d at %H:%M:%S UTC"))
    run(main())
    print(format_time("Finalization Time: %Y-%m-%d at %H:%M:%S UTC"))
