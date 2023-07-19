from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from serializers import (
    Snippet,
)
from typing import (
    Any,
)
from vulnerabilities.domain.snippet import (
    set_snippet,
)


async def _set_snippet(
    vulnerability: Vulnerability, sarif_vulns: list[dict[str, Any]]
) -> None:
    sarif_vulnerability: dict[str, Any] | None = next(
        (
            vuln
            for vuln in sarif_vulns
            if vuln["locations"][0]["physicalLocation"]["artifactLocation"][
                "uri"
            ]
            == vulnerability.state.where
            and vuln["locations"][0]["physicalLocation"]["region"]["startLine"]
            == vulnerability.state.specific
        ),
        None,
    )
    if sarif_vulnerability:
        context_region = sarif_vulnerability["locations"][0][
            "physicalLocation"
        ]["contextRegion"]
        await set_snippet(
            vulnerability,
            Snippet(
                content=context_region["snippet"]["text"],
                offset=context_region["properties"]["offset"],
                line=context_region["properties"]["line"],
                column=context_region["properties"]["column"],
                line_context=context_region["properties"]["line_context"],
                wrap=context_region["properties"]["wrap"],
                show_line_numbers=context_region["properties"][
                    "show_line_numbers"
                ],
                highlight_line_number=context_region["properties"][
                    "highlight_line_number"
                ],
            ),
        )


async def update_snippets(
    loaders: Dataloaders,
    persisted_vulns: set[str],
    sarif_vulns: list[dict[str, Any]],
) -> None:
    vulnerabilities: list[Vulnerability] = [
        vuln
        for vuln in (await loaders.vulnerability.load_many(persisted_vulns))
        if vuln
    ]
    vulnerabilities = [
        vuln
        for vuln in vulnerabilities
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        and vuln.type == VulnerabilityType.LINES
    ]
    await collect(_set_snippet(vuln, sarif_vulns) for vuln in vulnerabilities)
