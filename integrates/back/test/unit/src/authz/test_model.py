import authz
import pytest
from typing import (
    Any,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["parameter", "expected"],
    [
        (
            authz.GROUP_LEVEL_ROLES,
            [
                "admin",
                "architect",
                "customer_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "user",
                "user_manager",
                "vulnerability_manager",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES,
            [
                "admin",
                "hacker",
                "user",
            ],
        ),
        (
            authz.SERVICE_ATTRIBUTES,
            [
                "asm",
                "continuous",
                "forces",
                "report_vulnerabilities",
                "request_zero_risk",
                "service_black",
                "service_white",
                "squad",
            ],
        ),
    ],
)
def test_model_integrity_keys_1(
    parameter: dict[str, Any], expected: list[str]
) -> None:
    assert sorted(parameter.keys()) == expected


@pytest.mark.parametrize(
    ["parameter"],
    [
        [authz.GROUP_LEVEL_ROLES],
        [authz.USER_LEVEL_ROLES],
    ],
)
def test_model_integrity_keys_2(parameter: dict[str, Any]) -> None:
    for value in parameter.values():
        assert sorted(value.keys()) == ["actions", "tags"]
