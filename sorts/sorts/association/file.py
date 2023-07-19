from concurrent.futures import (
    ThreadPoolExecutor,
)
from functools import (
    partial,
)
from integrates.dal import (
    get_finding_ids,
    get_vulnerabilities,
    update_toe_lines_suggestions,
)
from integrates.typing import (
    Vulnerability,
    VulnerabilityKindEnum,
)
from itertools import (
    groupby,
)
from sorts.utils.logs import (
    log,
)
from training.redshift import (
    db as redshift,
)

ASSOCIATION_RULES_QUERY = """
SELECT antecedents, consequents, confidence
FROM sorts.association_rules
ORDER BY confidence DESC
"""


def get_vulnerable_lines(token_fluidattacks: str, group: str) -> list:
    """Fetches the vulnerable files from a group"""
    vulnerabilities: list[Vulnerability] = []
    finding_ids: list[str] = get_finding_ids(token_fluidattacks, group)
    with ThreadPoolExecutor(max_workers=8) as executor:
        for finding_vulnerabilities in executor.map(
            partial(get_vulnerabilities, token_fluidattacks), finding_ids
        ):
            vulnerabilities.extend(finding_vulnerabilities)  # type: ignore

    return [
        [vuln.where, vuln.title]
        for vuln in vulnerabilities
        if vuln.kind == VulnerabilityKindEnum.LINES
    ]


def remove_repeated(repeated_list: list[str]) -> list[str]:
    unique_list = []
    for element in repeated_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


def associate_vulns_to_files(
    token_fluidattacks: str,
    group_name: str,
    vuln_types_by_file: list[list[str]],
) -> None:
    association_rules: list[str] = redshift.fetch_data(ASSOCIATION_RULES_QUERY)
    with ThreadPoolExecutor(max_workers=8) as executor:
        for file in vuln_types_by_file:
            sorts_suggestions = []
            for rule in association_rules:
                antecedents = rule[0].split(", ")
                consequents = rule[1].split(", ")
                if all(item in file[1:] for item in antecedents):
                    for consequent in consequents:
                        suggestion = {
                            "findingTitle": consequent,
                            "probability": int(rule[2] * 100),
                        }
                        sorts_suggestions.append(suggestion)
                if len(sorts_suggestions) >= 5:
                    break
            file_info = {
                "rootNickname": file[0].split("/")[0],
                "filename": file[0].split("/", 1)[1],
                "sortsSuggestions": sorts_suggestions[:5],
            }
            if sorts_suggestions:
                executor.submit(
                    update_toe_lines_suggestions,
                    token_fluidattacks,
                    group_name,
                    file_info["rootNickname"],  # type: ignore
                    file_info["filename"],  # type: ignore
                    file_info["sortsSuggestions"],  # type: ignore
                )
    log("info", f"ToeLines's sortsSuggestions for {group_name} updated")


def execute_association_rules(
    token_fluidattacks: str, group_name: str
) -> None:
    group_all_vulns = get_vulnerable_lines(token_fluidattacks, group_name)
    # Group all vuln types with the same filename
    # each under one list with its filename at the start
    vuln_types_by_file = [
        [k] + [j[1] for j in list(v)]
        for k, v in groupby(
            sorted(group_all_vulns, key=lambda x: x[0]), lambda x: x[0]
        )
    ]
    unique_vuln_types_by_file = [
        remove_repeated(file) for file in vuln_types_by_file
    ]
    associate_vulns_to_files(
        token_fluidattacks, group_name, unique_vuln_types_by_file
    )
