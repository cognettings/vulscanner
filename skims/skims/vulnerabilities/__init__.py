import ctx
from model.core import (
    HTTPProperties,
    MethodsEnum,
    SkimsVulnerabilityMetadata,
    TechniqueEnum,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from model.cvss3 import (
    find_score_data,
)


def search_method(method_path: str) -> MethodsEnum | None:
    for method in MethodsEnum:
        if f"{method.value.file_name}.{method.value. name}" == method_path:
            return method
    return None


def build_metadata(  # pylint: disable=too-many-arguments
    method: MethodsEnum,
    description: str,
    snippet: str,
    http_properties: HTTPProperties | None = None,
    cvss: str | None = None,
    cwe_ids: list[str] | None = None,
    package: str | None = None,
    vulnerable_version: str | None = None,
    cve: list[str] | None = None,
) -> SkimsVulnerabilityMetadata:
    cwe = cwe_ids if cwe_ids else method.value.get_cwe()
    if not cvss:
        if method.value.cvss:
            cvss = method.value.cvss
        else:
            cvss = find_score_data(
                method.value.get_finding()
            ).score_to_vector_string()
    return SkimsVulnerabilityMetadata(
        cve=cve,
        cwe_ids=cwe,
        cvss=cvss,
        description=description,
        http_properties=http_properties,
        package=package,
        snippet=snippet,
        source_method=method.value.get_name(),
        developer=method.value.developer,
        technique=method.value.technique,
        vulnerable_version=vulnerable_version,
    )


def build_inputs_vuln(
    method: MethodsEnum,
    stream: str,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    kind = VulnerabilityKindEnum.DAST
    if method.value.file_name == "aws":
        kind = VulnerabilityKindEnum.CSPM
    return Vulnerability(
        finding=method.value.finding,
        kind=kind,
        namespace=ctx.SKIMS_CONFIG.namespace,
        state=VulnerabilityStateEnum.OPEN,
        stream=stream,
        what=what,
        where=where,
        skims_metadata=metadata,
    )


def build_lines_vuln(
    method: MethodsEnum,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    kind = VulnerabilityKindEnum.SAST
    if method.value.technique == TechniqueEnum.SCA:
        kind = VulnerabilityKindEnum.SCA
    elif method.value.technique == TechniqueEnum.APK:
        kind = VulnerabilityKindEnum.DAST

    return Vulnerability(
        finding=method.value.finding,
        kind=kind,
        namespace=ctx.SKIMS_CONFIG.namespace,
        state=VulnerabilityStateEnum.OPEN,
        what=what,
        where=where,
        skims_metadata=metadata,
    )
