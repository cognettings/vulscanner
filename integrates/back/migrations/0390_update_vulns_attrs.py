# pylint: disable=invalid-name
"""
Add cvss3 and cwe_ids to F011 and F393 vulnerabilities,
extracting the data from s3.

Execution Time:    2023-04-20 at 22:37:13 UTC
Finalization Time: 2023-04-20 at 23:46:25 UTC

Execution Time:    2023-04-21 at 00:40:33 UTC
Finalization Time: 2023-04-21 at 00:53:47 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from class_types.types import (
    Item,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    ErrorDownloadingFile,
)
from custom_utils import (
    cvss as cvss_utils,
)
from cvss import (
    CVSS3,
    CVSS3Error,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from dynamodb import (
    keys,
    operations,
)
import itertools
import json
from organizations.domain import (
    get_all_group_names,
)
from os.path import (
    split,
    splitext,
)
import re
from s3.resource import (
    get_s3_resource,
    s3_shutdown,
    s3_start_resource,
)
from tempfile import (
    NamedTemporaryFile,
)
import time
from typing import (
    Any,
)

SUPPORTED_PLATFORMS = (
    "maven",
    "npm",
    "nuget",
    "pip",
    "gem",
    "go",
    "conan",
    "pub",
)

DATABASE: dict | None = None
DATABASE_PATCH: dict | None = None


async def download_json_fileobj(
    bucket: str,
    file_name: str,
) -> dict[str, Any]:
    return_value: dict[str, Any] = {}
    with NamedTemporaryFile() as temp:
        try:
            client = await get_s3_resource()
            await client.download_fileobj(
                bucket,
                file_name,
                temp,
            )
            temp.seek(0)
            return_value = json.loads(temp.read().decode(encoding="utf-8"))
        except ValueError as ex:
            print("error", "%s", ex)
        return return_value


async def download_advisories(
    needed_platforms: Iterable[str],
    dl_only_patches: bool = False,
) -> tuple[Item, Item]:
    s3_advisories = {}
    s3_patch_advisories = {}
    bucket_name = "skims.sca"
    for plt in needed_platforms:
        if not dl_only_patches:
            dict_obj: Item = await download_json_fileobj(
                bucket_name, f"{plt}.json"
            )
            s3_advisories.update({plt: dict_obj})
        if plt not in {"go", "conan", "pub"}:
            dict_patch_obj: Item = await download_json_fileobj(
                bucket_name, f"{plt}_patch.json"
            )
            s3_patch_advisories.update({plt: dict_patch_obj})
    return s3_advisories, s3_patch_advisories


async def get_advisories_from_s3(platform: str) -> dict[str, dict] | None:
    if DATABASE is None or DATABASE_PATCH is None:
        return None

    platform_ads = DATABASE.get(platform, {})
    platform_patch_ads = DATABASE_PATCH.get(platform, {})
    updated_adv = {}
    for pkg_name, patch_ads in platform_patch_ads.items():
        ads = platform_ads.get(pkg_name, {})
        for key, value in patch_ads.items():
            if isinstance(value, dict):
                updated_adv[key] = {
                    "vulnerable_version": value.get("vulnerable_version"),
                    "cvss": value.get("cvss"),
                    "cwe_ids": value.get("cwe_ids"),
                }
            ads.update(updated_adv)
        no_gms_ads = {
            key: value
            for key, value in ads.items()
            if not key.startswith("GMS")
        }
        platform_ads[pkg_name] = no_gms_ads
    return platform_ads


def rm_nones(target: list) -> list:
    return [x for x in target if x]


def rm_duplicated(target: list) -> list:
    return list(dict.fromkeys(target))


def max_cvss_list(target: list) -> str | None:
    if target:
        try:
            scores = [CVSS3(elem).temporal_score for elem in target]
            return target[max(range(len(scores)), key=scores.__getitem__)]
        except CVSS3Error:
            print(
                "error",
                "Could not generate the CVSS3 score",
            )
    return None


def remove_last_slash(input_str: str | None) -> str | None:
    if input_str and input_str.endswith("/"):
        input_str = input_str[:-1]
    return input_str


async def process_advisories(
    item: Item,
    associated_advisories: list[str],
) -> tuple[str | None, list[str]]:
    cwe_ids = []
    cvss = []
    for package in item.values():
        for cve, values in package.items():
            for adv in associated_advisories:
                if cve == adv.strip():
                    cwe_ids.append(values["cwe_ids"])
                    cvss.append(remove_last_slash(values["cvss"]))
    cvss_v3 = max_cvss_list(rm_nones(cvss))
    cwe_ids = rm_duplicated(list(itertools.chain(*rm_nones(cwe_ids))))
    return (cvss_v3, cwe_ids)


async def process_sca_item(
    path: str, associated_advisories: list[str]
) -> tuple[str | None, list[str]]:
    item: Item | None = {}
    _, file_info = split(path)
    file_name, file_extension = splitext(file_info)
    file_extension = file_extension[1:]
    if file_extension in {"xml", "gradle"} or (file_name, file_extension) == (
        "build",
        "sbt",
    ):
        item = await get_advisories_from_s3("maven")
    if (file_name, file_extension) == ("yarn", "lock"):
        item = await get_advisories_from_s3("npm")
    if file_extension == "csproj" or (file_name, file_extension) == (
        "packages",
        "config",
    ):
        item = await get_advisories_from_s3("nuget")
    if (file_name, file_extension) == ("package", "json") or (
        file_name,
        file_extension,
    ) == ("package-lock", "json"):
        item = await get_advisories_from_s3("npm")
    if (file_name, file_extension) == ("requirements", "txt"):
        item = await get_advisories_from_s3("pip")
    if (file_name, file_extension) == (
        "Gemfile",
        "lock",
    ) or file_name == "Gemfile":
        item = await get_advisories_from_s3("gem")
    return await process_advisories(item or {}, associated_advisories)


async def get_finding_vulnerabilities_items(
    finding_id: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def persist_vulnerability_parameters(
    vulnerability: Vulnerability,
    cvss_v3: str | None,
    cwe_ids: list[str] | None,
) -> bool:
    severity_score = None
    if cvss_v3:
        cvss_utils.validate_cvss_vector(cvss_v3)
        severity_score = cvss_utils.get_severity_score_from_cvss_vector(
            cvss_v3
        )
    cwe_ids = cvss_utils.parse_cwe_ids(cwe_ids)
    if severity_score is None and cwe_ids is None:
        return False
    if (
        vulnerability.severity_score == severity_score
        and vulnerability.cwe_ids == cwe_ids
    ):
        return False

    await vulns_model.update_metadata(
        vulnerability_id=vulnerability.id,
        finding_id=vulnerability.finding_id,
        metadata=VulnerabilityMetadataToUpdate(
            cwe_ids=cwe_ids,
            severity_score=severity_score,
        ),
    )
    print(f"Vuln updated {vulnerability.id=} {severity_score=} {cwe_ids=}")

    return True


async def process_vulnerability_item(item: Item) -> bool:
    vulnerability: Vulnerability = format_vulnerability(item)
    pattern = r"^(.*?)\s*\(([^)]* v([\d.]+)[^)]*\))\s*\[(.*?)\]$"
    match = re.search(pattern, vulnerability.state.where)
    if not match:
        return False

    result = (
        match.group(1),
        match.group(2),
        match.group(4).split(","),
    )
    cvss_v3, cwe_ids = await process_sca_item(
        path=result[0],
        associated_advisories=result[2],
    )
    return await persist_vulnerability_parameters(
        vulnerability=vulnerability, cvss_v3=cvss_v3, cwe_ids=cwe_ids
    )


async def process_finding(finding: Finding) -> None:
    items = await get_finding_vulnerabilities_items(finding_id=finding.id)
    if not items:
        return

    results = list(
        await collect(
            tuple(process_vulnerability_item(item) for item in items),
            workers=16,
        )
    )
    print(
        f"Finding updated {finding.id=} {len(items)=} {results.count(True)=}"
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_findings = await loaders.group_findings.load(group_name)
    if not group_findings:
        return
    findings_filtered = [
        fin
        for fin in group_findings
        if fin.title
        in {
            "011. Use of software with known vulnerabilities",
            "393. Use of software with known vulnerabilities "
            "in development",
        }
        and fin.state.source == Source.MACHINE
    ]
    if not findings_filtered:
        return

    await collect(
        tuple(
            process_finding(finding=finding) for finding in findings_filtered
        ),
        workers=2,
    )
    print(f"Group processed {group_name} {str(round(progress, 2))}")


async def main() -> None:
    global DATABASE, DATABASE_PATCH  # pylint: disable=global-statement
    await s3_start_resource(is_public=True)
    s3_advisories, s3_patch_advisories = await download_advisories(
        needed_platforms=SUPPORTED_PLATFORMS
    )
    DATABASE = s3_advisories
    DATABASE_PATCH = s3_patch_advisories
    await s3_shutdown()
    if DATABASE is None or DATABASE_PATCH is None:
        raise ErrorDownloadingFile()

    loaders: Dataloaders = get_new_context()
    group_names = sorted(await get_all_group_names(loaders))
    print(f"{group_names=}")
    print(f"{len(group_names)=}")
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group,
                progress=count / len(group_names),
            )
            for count, group in enumerate(group_names)
        ),
        workers=8,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
