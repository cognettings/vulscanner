from collections.abc import (
    Mapping,
)
from contextlib import (
    suppress,
)
import ctx
from ctx import (
    CRITERIA_REQUIREMENTS,
    CRITERIA_VULNERABILITIES,
)
from model import (
    core,
)
from model.utils.what import (
    format_what,
    get_apk_details,
    get_missing_dependency,
    get_sca_info,
)
import os
import sarif_om
from serializers import (
    make_snippet,
    Snippet,
    SnippetViewport,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
from utils.repositories import (
    get_repo_branch,
    get_repo_head_hash,
    get_repo_remote,
)
import yaml


def simplify_sarif(obj: Any) -> Any:
    simplified_obj: Any
    if hasattr(obj, "__attrs_attrs__"):
        simplified_obj = {
            attribute.metadata["schema_property_name"]: simplify_sarif(
                obj.__dict__[attribute.name]
            )
            for attribute in obj.__attrs_attrs__
            if obj.__dict__[attribute.name] != attribute.default
        }
    elif isinstance(obj, dict):
        simplified_obj = simplified_obj = {
            key: simplify_sarif(value) for key, value in obj.items()
        }
    elif isinstance(obj, (list, tuple, set)):
        simplified_obj = [simplify_sarif(item) for item in obj]
    else:
        simplified_obj = obj
    return simplified_obj


def _get_criteria_vulns() -> dict[str, Any]:
    with open(CRITERIA_VULNERABILITIES, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _get_criteria_requirements() -> dict[str, Any]:
    with open(CRITERIA_REQUIREMENTS, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


CRITERIA_VULNS = _get_criteria_vulns()


CRITERIA_REQS = _get_criteria_requirements()


def _get_rule(vuln_id: str) -> sarif_om.ReportingDescriptor:
    content = CRITERIA_VULNS[vuln_id]
    auto_approve = False
    with suppress(KeyError):
        auto_approve = core.FindingEnum[f"F{vuln_id}"].value.auto_approve

    return sarif_om.ReportingDescriptor(
        id=vuln_id,
        name=content["en"]["title"],
        full_description=sarif_om.MultiformatMessageString(
            text=content["en"]["description"]
        ),
        help_uri=(
            "https://docs.fluidattacks.com/criteria/"
            f"vulnerabilities/{vuln_id}#details"
        ),
        help=sarif_om.MultiformatMessageString(
            text=content["en"]["recommendation"]
        ),
        default_configuration=sarif_om.ReportingConfiguration(
            enabled=True, level="error"
        ),
        properties={"auto_approve": auto_approve},
    )


def _get_taxa(requirement_id: str) -> sarif_om.ReportingDescriptor:
    content = CRITERIA_REQS[requirement_id]
    return sarif_om.ReportingDescriptor(
        id=requirement_id,
        name=content["en"]["title"],
        short_description=sarif_om.MultiformatMessageString(
            text=content["en"]["summary"]
        ),
        full_description=sarif_om.MultiformatMessageString(
            text=content["en"]["description"]
        ),
        help_uri=(
            "https://docs.fluidattacks.com/criteria/"
            f"requirements/{requirement_id}"
        ),
    )


def _rule_is_present(base: sarif_om.SarifLog, rule_id: str) -> bool:
    for rule in base.runs[0].tool.driver.rules:
        if rule.id == rule_id:
            return True

    return False


def _taxa_is_present(base: sarif_om.SarifLog, taxa_id: str) -> bool:
    for rule in base.runs[0].taxonomies[0].taxa:
        if rule.id == taxa_id:
            return True

    return False


def _format_were(were: str) -> int | str:
    try:
        return int(were)
    except ValueError:
        return were


def _get_vuln_properties(
    vulnerability: core.Vulnerability, rule_id: str
) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    if vulnerability.skims_metadata.technique == core.TechniqueEnum.SCA and (
        sca_info := get_sca_info(vulnerability.what)
    ):
        properties = sca_info
    elif (
        (
            vulnerability.skims_metadata.source_method
            == "python.pip_incomplete_dependencies_list"
        )
        and rule_id == "120"
        and (dependency_info := get_missing_dependency(vulnerability.what))
    ):
        properties = dependency_info
    elif vulnerability.skims_metadata.technique == core.TechniqueEnum.APK and (
        apk_details := get_apk_details(vulnerability.what)
    ):
        properties = apk_details

    return properties


def _get_text_description(vulnerability: core.Vulnerability) -> str:
    return (
        vulnerability.skims_metadata.description
        if vulnerability.skims_metadata
        else ""
    )


def _get_render_snippet(vulnerability: core.Vulnerability) -> str:
    return (
        vulnerability.skims_metadata.snippet
        if vulnerability.skims_metadata
        else ""
    )


def _get_vulnerability_region(
    vulnerability: core.Vulnerability,
) -> Snippet | None:
    snippet = None
    if os.path.exists(vulnerability.what):
        with open(vulnerability.what, encoding="utf_8") as content_handler:
            try:
                snippet = make_snippet(
                    content=content_handler.read(),
                    viewport=SnippetViewport(
                        line=int(vulnerability.where),
                        column=0,
                        show_line_numbers=False,
                        highlight_line_number=False,
                    ),
                )
            except UnicodeDecodeError:
                return None
    if snippet and snippet.line:
        region = sarif_om.Region(
            start_line=max(snippet.line - snippet.line_context, 0),
            end_line=snippet.line + snippet.line_context,
            snippet=sarif_om.ArtifactContent(
                rendered=_get_render_snippet(vulnerability),
                text=snippet.content,
            ),
            start_column=snippet.column,
            char_length=snippet.columns_per_line,
            properties={
                "offset": snippet.offset,
                "line": snippet.line,
                "column": snippet.column,
                "line_context": snippet.line_context,
                "wrap": snippet.wrap,
                "show_line_numbers": snippet.show_line_numbers,
                "highlight_line_number": snippet.highlight_line_number,
            },
        )
    else:
        region = (
            sarif_om.Region(
                start_line=_format_were(vulnerability.where),
                snippet=sarif_om.ArtifactContent(
                    rendered=_get_render_snippet(vulnerability)
                ),
            ),
        )
    return region


def _get_properties(vulnerability: core.Vulnerability) -> dict[str, Any]:
    return {
        "cwe_ids": vulnerability.skims_metadata.cwe_ids,
        "cvss": vulnerability.skims_metadata.cvss,
        "kind": vulnerability.kind.value,
        "method_developer": (vulnerability.skims_metadata.developer.value),
        "source_method": (vulnerability.skims_metadata.source_method),
        "stream": vulnerability.stream,
        "technique": (vulnerability.skims_metadata.technique.value),
        **(
            vulnerability.skims_metadata.http_properties._asdict()
            if vulnerability.skims_metadata.http_properties is not None
            else {}
        ),
    }


def _get_sarif(
    stores: Mapping[core.FindingEnum, EphemeralStore],
) -> sarif_om.SarifLog:
    base = sarif_om.SarifLog(
        version="2.1.0",
        schema_uri=(
            "https://schemastore.azurewebsites.net/schemas/"
            "json/sarif-2.1.0-rtm.4.json"
        ),
        runs=[
            sarif_om.Run(
                tool=sarif_om.Tool(
                    driver=sarif_om.ToolComponent(
                        name="skims",
                        rules=[],
                    )
                ),
                results=[],
                version_control_provenance=[
                    sarif_om.VersionControlDetails(
                        repository_uri=get_repo_remote(
                            ctx.SKIMS_CONFIG.working_dir
                        ),
                        revision_id=get_repo_head_hash(
                            ctx.SKIMS_CONFIG.working_dir
                        ),
                        branch=get_repo_branch(ctx.SKIMS_CONFIG.working_dir),
                    )
                ],
                taxonomies=[
                    sarif_om.ToolComponent(
                        name="criteria",
                        version="1",
                        information_uri=(
                            "https://docs.fluidattacks.com/"
                            "criteria/requirements/"
                        ),
                        organization="Fluidattacks",
                        short_description=sarif_om.MultiformatMessageString(
                            text="The fluidattacks security requirements"
                        ),
                        taxa=[],
                        is_comprehensive=False,
                    )
                ],
                original_uri_base_ids={
                    "SRCROOT": sarif_om.ArtifactLocation(
                        uri=ctx.SKIMS_CONFIG.namespace
                    )
                },
            ),
        ],
    )

    for check in ctx.SKIMS_CONFIG.checks:
        base.runs[0].tool.driver.rules.append(
            _get_rule(check.name.replace("F", ""))
        )

    for store in stores.values():
        for vulnerability in store.iterate():
            # remove F from findings
            rule_id = vulnerability.finding.name.replace("F", "")
            properties = _get_vuln_properties(vulnerability, rule_id)

            result = sarif_om.Result(
                rule_id=rule_id,
                level="error",
                kind="open",
                message=sarif_om.MultiformatMessageString(
                    text=_get_text_description(vulnerability),
                    properties=properties,
                ),
                locations=[
                    sarif_om.Location(
                        physical_location=sarif_om.PhysicalLocation(
                            artifact_location=sarif_om.ArtifactLocation(
                                uri=format_what(vulnerability)
                            ),
                            region=sarif_om.Region(
                                start_line=_format_were(vulnerability.where),
                                snippet=sarif_om.MultiformatMessageString(
                                    text=_get_render_snippet(vulnerability)
                                ),
                            ),
                            context_region=_get_vulnerability_region(
                                vulnerability
                            ),
                        )
                    ),
                ],
                taxa=[],
                properties=_get_properties(vulnerability),
            )
            result.guid = vulnerability.digest_future

            # append rule if not is present
            if not _rule_is_present(base, rule_id):
                base.runs[0].tool.driver.rules.append(_get_rule(rule_id))

            # append requirement if not is present
            for taxa_id in CRITERIA_VULNS[rule_id]["requirements"]:
                if not _taxa_is_present(base, taxa_id):
                    base.runs[0].taxonomies[0].taxa.append(_get_taxa(taxa_id))
                result.taxa.append(
                    sarif_om.ReportingDescriptorReference(
                        id=taxa_id,
                        tool_component=sarif_om.ToolComponentReference(
                            name="criteria"
                        ),
                    )
                )
            base.runs[0].results.append(result)

    return base


def get_sarif(
    stores: Mapping[core.FindingEnum, EphemeralStore],
) -> dict[str, Any]:
    return simplify_sarif(_get_sarif(stores))
