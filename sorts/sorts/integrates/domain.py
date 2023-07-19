from collections.abc import (
    Iterable,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from functools import (
    partial,
)
from integrates.dal import (
    get_finding_ids,
    get_vulnerabilities,
)
from integrates.typing import (
    Vulnerability,
    VulnerabilityKindEnum,
)
import os
from sorts.utils.logs import (
    log,
)
from sorts.utils.static import (
    read_allowed_names,
)
import time


def filter_allowed_files(
    vuln_files: Iterable[str], ignore_repos: Iterable[str]
) -> list[str]:
    """Leave files with allowed names and filter out from ignored repos"""
    allowed_vuln_files: list[str] = []
    extensions, composites = read_allowed_names()
    for vuln_file in vuln_files:
        vuln_repo: str = vuln_file.split(os.path.sep)[0]
        if vuln_repo not in ignore_repos:
            vuln_file_name: str = os.path.basename(vuln_file)
            vuln_file_extension: str = os.path.splitext(vuln_file_name)[
                1
            ].strip(".")
            if (
                vuln_file_extension in extensions
                or vuln_file_name in composites
            ):
                allowed_vuln_files.append(vuln_file)
    return allowed_vuln_files


def get_unique_vuln_files(token_fluidattacks: str, group: str) -> list[str]:
    """Removes repeated files from group vulnerabilities"""
    vulnerable_filenames: list[str] = [
        vuln.where
        for vuln in get_vulnerable_lines(token_fluidattacks, group)
        if vuln.kind.value == VulnerabilityKindEnum.LINES.value
    ]
    unique_vuln_filenames: set[str] = set(vulnerable_filenames)

    return sorted(unique_vuln_filenames)


def get_vulnerable_files(
    token_fluidattacks: str, group: str, ignore_repos: Iterable[str]
) -> list[str]:
    """Gets vulnerable files to fill the training DataFrame"""
    timer: float = time.time()
    unique_vuln_files: list[str] = get_unique_vuln_files(
        token_fluidattacks, group
    )
    allowed_vuln_files: list[str] = filter_allowed_files(
        unique_vuln_files, ignore_repos
    )
    log(
        "info",
        "Vulnerable files extracted after %.2f seconds",
        time.time() - timer,
    )
    return allowed_vuln_files


def get_vulnerable_lines(
    token_fluidattacks: str, group: str
) -> list[Vulnerability]:
    """Fetches the vulnerable files from a group"""
    vulnerabilities: list[Vulnerability] = []
    finding_ids: list[str] = get_finding_ids(token_fluidattacks, group)
    with ThreadPoolExecutor(max_workers=8) as executor:
        for finding_vulnerabilities in executor.map(
            partial(get_vulnerabilities, token_fluidattacks), finding_ids
        ):
            vulnerabilities.extend(finding_vulnerabilities)  # type: ignore

    return vulnerabilities
