import re
from semantic_version import (
    base,
    NpmSpec,
    Version,
)
from utils.logs import (
    log_blocking,
)

SINGLE_VER: re.Pattern[str] = re.compile(
    r"^={0,2}(?P<version>\d+\.\d+\.\d+[0-9A-Za-z-\+\.]*)$"
)
VERSION_SEPARATORS: re.Pattern[str] = re.compile("([-+])")
SPACE_PATTERN: re.Pattern[str] = re.compile(r"\s+")
RANGES_SEPARATOR: re.Pattern[str] = re.compile(r"\s*\|\|\s*")


def check_extremes_intersection(
    min_spec: base.Range, max_spec: base.Range | None
) -> bool:
    if max_spec is None:
        return True
    min_version: Version = min_spec.target
    max_version: Version = max_spec.target
    if min_spec.operator == ">" or max_spec.operator == "<":
        return max_version > min_version
    return max_version >= min_version


def get_min_and_max_ver(
    spec: base.AllOf,
) -> tuple[base.Range, base.Range | None]:
    npm_clause_list = list(spec)
    if len(npm_clause_list) == 1:
        return npm_clause_list[0], None
    sorted_clause_list = sorted(
        npm_clause_list, key=lambda x: (x.target, -ord(x.operator[0]))
    )
    min_dep = sorted_clause_list[0]
    max_dep = sorted_clause_list[-1]
    return min_dep, max_dep


def check_ranges_intersection(
    range_1: base.AllOf, range_2: base.AllOf
) -> bool:
    range_2_spec: base.Range = next(iter(range_2))
    if range_2_spec.operator == "==":
        return range_1.match(range_2_spec.target)
    min_range_1, max_range_1 = get_min_and_max_ver(range_1)
    min_range_2, max_range_2 = get_min_and_max_ver(range_2)
    return check_extremes_intersection(
        min_range_2, max_range_1
    ) and check_extremes_intersection(min_range_1, max_range_2)


def coerce(constraint: str) -> str:
    constraint_tokens = VERSION_SEPARATORS.split(constraint)
    version_coerced = constraint_tokens[0].split(".")
    tags = "".join(constraint_tokens[1:])
    first_item = version_coerced[0]
    desired_length = 3
    coerced_length = len(version_coerced)
    if "v" in first_item:
        version_coerced[0] = first_item.replace("v", "")
    if coerced_length < desired_length:
        filler_item = "*" if first_item.startswith("~") else "0"
        version_coerced += [filler_item] * (desired_length - coerced_length)

    return f"{'.'.join(version_coerced[:3])}{tags}"


def coerce_range(range_str: str) -> str:
    range_str = SPACE_PATTERN.sub(" ", range_str)
    range_tokens = RANGES_SEPARATOR.split(range_str)
    arr_range_tokens = []
    for tokens in range_tokens:
        if tokens.startswith("<"):
            tokens = f">=0.0.0 {tokens}"
        coerced_tokens = " ".join(coerce(token) for token in tokens.split())
        arr_range_tokens.append(coerced_tokens)
    range_coerced = "||".join(arr_range_tokens)
    return range_coerced


def check_multiple_ranges(
    version_clause: base.Clause, constraint_clause: base.Clause
) -> bool:
    if isinstance(constraint_clause, base.AllOf):
        if isinstance(version_clause, base.AnyOf):
            return any(
                check_ranges_intersection(version_range, constraint_clause)
                for version_range in version_clause
            )
        return check_ranges_intersection(version_clause, constraint_clause)
    return any(
        check_multiple_ranges(version_clause, const_range)
        for const_range in constraint_clause
    )


def semver_match(dep_version: str, vulnerable_version: str) -> bool:
    if dep_version == "":
        return False
    dep_coerced = coerce_range(dep_version)
    vulnerable_coerced = coerce_range(vulnerable_version)
    try:
        vulnerable_specs: base.Clause = NpmSpec(vulnerable_coerced).clause
        if matched := SINGLE_VER.match(dep_coerced):
            single_dep_version = Version(matched.group("version"))
            return vulnerable_specs.match(single_dep_version)
        dep_specs: base.Clause = NpmSpec(dep_coerced).clause
        return check_multiple_ranges(dep_specs, vulnerable_specs)
    except ValueError:
        log_blocking(
            "error",
            "Semver match %s to %s: Invalid semver version",
            dep_version,
            vulnerable_version,
        )
        return False
