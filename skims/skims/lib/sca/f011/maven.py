import bs4
from collections.abc import (
    Iterator,
)
import glob
from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core import (
    MethodsEnum,
    Platform,
)
import os
import re
from utils.fs import (
    get_file_content_block,
)

# Constants
QUOTE = r'["\']'
TEXT = r'[^"\']+'
WS = r"\s*"

# Regexes
RE_LINE_COMMENT: re.Pattern[str] = re.compile(r"^.*" rf"{WS}//" r".*$")
RE_GRADLE_A: re.Pattern[str] = re.compile(
    r"^.*"
    rf"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    rf"group{WS}:{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}"
    rf",{WS}name{WS}:{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}"
    rf"(?:,{WS}version{WS}:{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS})?"
    rf".*$"
)
RE_GRADLE_B: re.Pattern[str] = re.compile(
    r"^.*"
    rf"{WS}(?:compile|compileOnly|implementation){WS}[(]?{WS}"
    rf"{QUOTE}(?P<statement>{TEXT}){QUOTE}"
    rf".*$"
)
RE_SBT: re.Pattern[str] = re.compile(
    r"^[^%]*"
    rf"{WS}{QUOTE}(?P<group>{TEXT}){QUOTE}{WS}%"
    rf"{WS}{QUOTE}(?P<name>{TEXT}){QUOTE}{WS}%"
    rf"{WS}{QUOTE}(?P<version>{TEXT}){QUOTE}{WS}"
    r".*$"
)


def avoid_cmt(line: str, is_block_cmt: bool) -> tuple[str, bool]:
    if RE_LINE_COMMENT.match(line):
        line = line.split("//", 1)[0]
    if is_block_cmt:
        if "*/" in line:
            is_block_cmt = False
            line = line.split("*/", 1).pop()
        else:
            return "", is_block_cmt
    if "/*" in line:
        line_cmt_open = line.split("/*", 1)[0]
        if "*/" in line:
            line = line_cmt_open + line.split("*/", 1).pop()
        else:
            line = line_cmt_open
            is_block_cmt = True
    return line, is_block_cmt


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_GRADLE)
def maven_gradle(content: str, path: str) -> Iterator[DependencyType]:
    is_block_cmt = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        line, is_block_cmt = avoid_cmt(line, is_block_cmt)
        if match := RE_GRADLE_A.match(line):
            column: int = match.start("group")
            product: str = match.group("group") + ":" + match.group("name")
            version = match.group("version") or ""
        elif match := RE_GRADLE_B.match(line):
            column = match.start("statement")
            statement = match.group("statement")
            product, version = (
                statement.rsplit(":", maxsplit=1)
                if statement.count(":") >= 2
                else (statement, "")
            )
        else:
            continue

        # Assuming a wildcard in Maven if the version is not found can
        # result in issues.
        # https://gitlab.com/fluidattacks/universe/-/issues/5635
        if version == "":
            continue

        yield format_pkg_dep(product, version, line_no, line_no, column)


def get_pom_xml(content: str) -> bs4.BeautifulSoup | None:
    root = bs4.BeautifulSoup(content, features="lxml")
    if root.project and (xmlns := root.project.get("xmlns")):
        if str(xmlns) == "http://maven.apache.org/POM/4.0.0":
            return root
    return None


def _get_parent_paths(path: str) -> list[str]:
    paths: list[str] = []
    split_path: list[str] = path.split("/")
    for pos in range(1, len(split_path) - 1):
        paths.append("/".join(split_path[0:pos]))
    return paths[::-1]


def _get_properties(root: bs4.BeautifulSoup) -> dict[str, str]:
    return {
        property.name.lower(): property.get_text()
        for properties in root.find_all("properties", limit=2)
        for property in properties.children
        if isinstance(property, bs4.element.Tag)
    }


def _get_deps_management(
    poms_trees: list[bs4.BeautifulSoup],
) -> dict[str, str]:
    deps_info: dict[str, str] = {}
    for pom in poms_trees:
        for manage in pom.find_all("dependencymanagement"):
            for dependency in manage.find_all("dependency", recursive=True):
                group = dependency.groupid.get_text()
                artifact = dependency.artifactid.get_text()
                version = dependency.version.get_text()
                deps_info[f"{group}:{artifact}"] = version
    return deps_info


def _get_parent_deps_management(
    current_pom: bs4.BeautifulSoup, dir_paths: list[str]
) -> dict[str, str]:
    parent_pom = _get_parent_pom(current_pom, dir_paths)
    poms_to_get_deps = [current_pom]
    if parent_pom:
        poms_to_get_deps.insert(0, parent_pom)
    return _get_deps_management(poms_to_get_deps)


def _find_vars(value: str, properties: dict[str, str]) -> str:
    if not value.startswith("${"):
        return value
    value = re.sub(r"[\$\{\}]", "", value)
    property_value = properties.get(value, "")
    return property_value


def _add_properties_vars(properties_vars: dict[str, str], path: str) -> None:
    content = get_file_content_block(path)
    if root_pom := get_pom_xml(content):
        properties = _get_properties(root_pom)
        properties_vars.update(properties)


def _get_vars_from_properties(
    current_path: str, parent_paths: list[str]
) -> dict[str, str]:
    properties_vars: dict[str, str] = {}
    _add_properties_vars(properties_vars, current_path)
    for path in parent_paths:
        pom_files = glob.glob(f"{path}/*.xml", recursive=False)
        for pom_file in pom_files:
            _add_properties_vars(properties_vars, pom_file)
    return properties_vars


def _get_parent_pom(
    root: bs4.BeautifulSoup, dir_paths: list[str]
) -> bs4.BeautifulSoup | None:
    parent_ref = root.find("parent")
    if not parent_ref:
        return None
    parent_group = parent_ref.groupid.get_text()
    parent_artifact = parent_ref.artifactid.get_text()
    parent_version = parent_ref.version.get_text()
    root_path = dir_paths[-1]
    pom_files = glob.glob(f"{root_path}/**/*.xml", recursive=True)
    for pom_file in pom_files:
        content = get_file_content_block(pom_file)
        if root_pom := get_pom_xml(content):
            project = root_pom.project
            group = project.find("groupid", recursive=False)
            artifact = project.find("artifactid", recursive=False)
            version = project.find("version", recursive=False)
            if not (group and artifact and version):
                continue
            group = group.get_text()
            artifact = artifact.get_text()
            version = version.get_text()
            if (
                group == parent_group
                and artifact == parent_artifact
                and version == parent_version
            ):
                return root_pom
    return None


def get_deps_modules(
    dir_paths: list[str],
    current_path: str,
    manage_deps: dict[str, str],
    root: bs4.BeautifulSoup,
) -> None:
    root_path = dir_paths[-1]
    pom_module = os.path.dirname(current_path)
    pom_files = glob.glob(f"{root_path}/**/*.xml", recursive=True)
    for pom_file in pom_files:
        pom_file_dir = os.path.dirname(pom_file)
        content = get_file_content_block(pom_file)
        if parent_pom := get_pom_xml(content):
            for modules in parent_pom.find_all("modules"):
                for module in modules.find_all("module"):
                    ref_module_path = os.path.normpath(
                        os.path.join(pom_file_dir, module.get_text())
                    )
                    if ref_module_path == pom_module:
                        module_deps = _get_deps_management([parent_pom, root])
                        manage_deps.update(module_deps)


@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_POM_XML)
def maven_pom_xml(  # pylint: disable=too-many-locals
    content: str, path: str
) -> Iterator[DependencyType]:
    root = bs4.BeautifulSoup(content, features="html.parser")
    parent_paths = _get_parent_paths(path)
    properties = _get_vars_from_properties(path, parent_paths)
    manage_deps = _get_parent_deps_management(root, parent_paths)
    get_deps_modules(parent_paths, path, manage_deps, root)
    for dependency in root.find_all("dependency", recursive=True):
        group = dependency.groupid
        artifact = dependency.artifactid
        version = dependency.find("version")
        g_text = _find_vars(group.get_text(), properties)
        a_text = _find_vars(artifact.get_text(), properties)
        product = f"{g_text}:{a_text}"
        if version is None:
            managed_version = manage_deps.get(product)
            if not managed_version:
                continue
            v_text = _find_vars(managed_version, properties)
            column = artifact.sourcepos
            line = artifact.sourceline
            yield format_pkg_dep(product, v_text, line, line, column)
        else:
            v_text = _find_vars(version.get_text(), properties)
            column = version.sourcepos
            line = version.sourceline
            yield format_pkg_dep(product, v_text, line, line, column)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.MAVEN, MethodsEnum.MAVEN_SBT)
def maven_sbt(content: str, path: str) -> Iterator[DependencyType]:
    for line_no, line in enumerate(content.splitlines(), start=1):
        if match := RE_SBT.match(line):
            column: int = match.start("group")
            product: str = match.group("group") + ":" + match.group("name")
            version = match.group("version")
        else:
            continue

        yield format_pkg_dep(product, version, line_no, line_no, column)
