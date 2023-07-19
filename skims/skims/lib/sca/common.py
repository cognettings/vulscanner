from aioextensions import (
    run,
)
from collections.abc import (
    Callable,
    Iterator,
)
import ctx
from custom_parsers.load_json import (
    loads_blocking as json_loads_blocking,
)
from dynamodb.resource import (
    dynamo_shutdown,
)
from frozendict import (
    frozendict,
)
from functools import (
    wraps,
)
import itertools
import json_parser
from model import (
    core,
)
from more_itertools import (
    windowed,
)
from pyarn import (
    lockfile,
)
import re
from sca import (
    get_vulnerabilities,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
    NamedTuple,
    TypeVar,
)
from utils.cvss import (
    max_cvss_list,
    set_default_temporal_scores,
)
from utils.fs import (
    get_file_content_block,
)
from utils.function import (
    shield,
    shield_blocking,
)
from utils.lists import (
    rm_duplicated,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)

# Constants
Tfun = TypeVar("Tfun", bound=Callable[..., Any])
DependencyType = tuple[frozendict, frozendict]

SHIELD: Callable[[Tfun], Tfun] = shield(on_error_return=())
SHIELD_BLOCKING: Callable[[Tfun], Tfun] = shield_blocking(on_error_return=())


class NpmDepInfo(NamedTuple):
    version: str
    product_line: int
    version_line: int


def get_vulnerabilities_for_incomplete_deps(
    content: str,
    description_key: str,
    iterator: Iterator[str],
    path: str,
    method: core.MethodsEnum,
) -> core.Vulnerabilities:
    results: core.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=f"{path} (missing dependency: {dep})",
            where="0",
            metadata=build_metadata(
                method=method,
                description=(
                    f"{t(key=description_key, name=dep)} "
                    f"{t(key='words.in')} "
                    f"{ctx.SKIMS_CONFIG.namespace}/{path}"
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=int(0), line=int(0)),
                ).content,
            ),
        )
        for dep in iterator
    )

    return results


def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    path: str,
    platform: core.Platform,
    method: core.MethodsEnum,
) -> core.Vulnerabilities:
    return run(
        _translate_dependencies_to_vulnerabilities(
            content=content,
            dependencies=dependencies,
            path=path,
            platform=platform,
            method=method,
        )
    )


async def _translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    path: str,
    platform: core.Platform,
    method: core.MethodsEnum,
) -> core.Vulnerabilities:
    try:
        # pylint: disable=consider-using-generator
        results: core.Vulnerabilities = tuple(
            [
                build_lines_vuln(
                    method=method,
                    what=" ".join(
                        (
                            path,
                            f'({product["item"]} v{version["item"]})',
                            f"[{', '.join([adv.id for adv in advisories])}]",
                        )
                    ),
                    where=str(product["line"]),
                    metadata=build_metadata(
                        method=method,
                        description=(
                            t(
                                key="f011.use_of_vulnerable_dependency",
                                product=product["item"],
                                version=version["item"],
                                cve=[adv.id for adv in advisories],
                            )
                            + f" {t(key='words.in')} "
                            f"{ctx.SKIMS_CONFIG.namespace}/{path}"
                        ),
                        cvss=set_default_temporal_scores(
                            max_cvss_list(
                                [
                                    adv.severity
                                    for adv in advisories
                                    if adv.severity
                                ]
                            )
                        ),
                        cwe_ids=rm_duplicated(
                            list(
                                itertools.chain(
                                    *[
                                        adv.cwe_ids
                                        for adv in advisories
                                        if adv.cwe_ids
                                    ]
                                )
                            )
                        ),
                        package=product["item"],
                        vulnerable_version=version["item"],
                        cve=[adv.id for adv in advisories],
                        snippet=make_snippet(
                            content=content,
                            viewport=SnippetViewport(
                                column=product["column"],
                                line=product["line"],
                            ),
                        ).content,
                    ),
                )
                for product, version in dependencies
                if (
                    advisories := await get_vulnerabilities(
                        platform,
                        product.get("item", None),
                        version.get("item", None),
                    )
                )
            ]
        )
    finally:
        await dynamo_shutdown()

    return results


def get_subdependencies(package: str, yarn_dict: lockfile) -> tuple:
    subdependencies: list[str] = []
    version: str | None = None
    for pkg_key, pkg_info in yarn_dict.items():
        # There may be keys in the yarn.lock file like this:
        # pkg@v1, pkg@v2, pkg@v3
        pkg_list = pkg_key.split(", ")
        if package in pkg_list:
            version = pkg_info.get("version")
            if "dependencies" in pkg_info:
                subdependencies = build_subdep_name(pkg_info["dependencies"])
    return subdependencies, version


def add_lines_enumeration(
    windower: Iterator[tuple[tuple[int, str], tuple[int, str]],],
    tree: dict[str, str],
) -> dict[str, NpmDepInfo]:
    enumerated_tree: dict[str, NpmDepInfo] = {}
    for (product_line, product), (version_line, version) in windower:
        product, version = product.strip(), version.strip()
        if (
            product.endswith(":")
            and not product.startswith(" ")
            and version.startswith("version")
        ):
            product = product.rstrip(":")
            product = product.strip('"')

            version = version.split(" ", maxsplit=1)[1]
            version = version.strip('"')

            if tree.get(product) == version:
                enumerated_tree[product] = NpmDepInfo(
                    version, product_line, version_line
                )
    return enumerated_tree


def build_subdep_name(dependencies: dict[str, str]) -> list[str]:
    dependencies_list: list[str] = []
    for key, value in dependencies.items():
        dependencies_list.append(key + "@" + value)
    return dependencies_list


def run_over_subdeps(
    subdeps: list[str], tree: dict[str, str], yarn_dict: lockfile
) -> dict[str, str]:
    while subdeps:
        current_subdep = subdeps[0]
        new_subdeps, version = get_subdependencies(current_subdep, yarn_dict)
        if version:
            tree[current_subdep] = version
        subdeps.remove(current_subdep)
        subdeps = [
            subdep
            for subdep in subdeps + new_subdeps
            if subdep not in tree  # Avoid infite loop with cyclic dependencies
        ]
    return tree


def build_dependencies_tree(  # pylint: disable=too-many-locals
    path_yarn: str,
    path_json: str,
    dependencies_type: core.DependenciesTypeEnum,
) -> dict[str, NpmDepInfo]:
    # Dependencies type could be "devDependencies" for dev dependencies
    # or "dependencies" for prod dependencies
    enumerated_tree: dict[str, NpmDepInfo] = {}
    yarn_content = get_file_content_block(path_yarn)
    windower: Iterator[
        tuple[tuple[int, str], tuple[int, str]]
    ] = windowed(  # type: ignore
        fillvalue="",
        n=2,
        seq=tuple(enumerate(yarn_content.splitlines(), start=1)),
        step=1,
    )
    yarn_dict = lockfile.Lockfile.from_file(path_yarn).data
    package_json_parser = json_parser.parse(get_file_content_block(path_json))
    tree: dict[str, str] = {}
    if dependencies_type.value in package_json_parser:
        package_json_dict = package_json_parser[dependencies_type.value]
        for json_pkg_name, json_pkg_version in package_json_dict.items():
            for yarn_pkg_key, yarn_pkg_info in yarn_dict.items():
                # There may be keys in the yarn.lock file like this:
                # pkg@v1, pkg@v2, pkg@v3
                yarn_pkg_list = yarn_pkg_key.split(", ")
                json_pkg = json_pkg_name + "@" + json_pkg_version
                if json_pkg in yarn_pkg_list:
                    tree[json_pkg] = yarn_pkg_info["version"]
                    if "dependencies" in yarn_pkg_info:
                        subdeps = build_subdep_name(
                            yarn_pkg_info["dependencies"]
                        )
                        tree = run_over_subdeps(subdeps, tree, yarn_dict)
        enumerated_tree = add_lines_enumeration(windower, tree)
    return enumerated_tree


def get_conan_dep_info(dep_line: str) -> tuple[str, str]:
    product, version = (
        re.sub(r"[\"\]\[]", "", dep_line).strip().split("@")[0].split("/")
    )
    if "," in version:
        version = re.sub(r",(?=[<>=])", " ", version).split(",")[0]
    return product, version


def format_conan_lock_dep(dep_info: frozendict) -> DependencyType:
    product, version = dep_info["item"].split("/")
    version = version.split("#")[0]
    dep_line = dep_info["line"]
    return format_pkg_dep(product, version, dep_line, dep_line)


def resolve_conan_lock_deps(
    content: str, requires: str
) -> Iterator[DependencyType]:
    content_json = json_loads_blocking(content, default={})
    dependencies: Iterator[DependencyType] = (
        format_conan_lock_dep(dep_info)
        for key in content_json
        if key["item"] == requires
        for dep_info in content_json[key]["item"]
    )
    return dependencies


def format_pkg_dep(
    pkg_name: str,
    version: str,
    product_line: int,
    version_line: int,
    column: int = 0,
) -> DependencyType:
    return (
        {
            "column": column,
            "line": product_line,
            "item": pkg_name,
        },
        {
            "column": column,
            "line": version_line,
            "item": version,
        },
    )


def pkg_deps_to_vulns(
    platform: core.Platform, method: core.MethodsEnum
) -> Callable[[Tfun], Callable[[str, str], core.Vulnerabilities]]:
    def resolve_deps(
        resolve_dependencies: Tfun,
    ) -> Callable[[str, str], core.Vulnerabilities]:
        @wraps(resolve_dependencies)
        def resolve_vulns(content: str, path: str) -> core.Vulnerabilities:
            return translate_dependencies_to_vulnerabilities(
                content=content,
                dependencies=resolve_dependencies(content, path),
                path=path,
                platform=platform,
                method=method,
            )

        return resolve_vulns

    return resolve_deps
