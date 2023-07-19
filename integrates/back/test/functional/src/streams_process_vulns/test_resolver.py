from . import (
    get_result,
)
from asyncio import (
    sleep,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
import pytest
from search.operations import (
    search,
)
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_vulns")
@pytest.mark.parametrize(
    [
        "email",
        "finding_id",
        "vulnerability_id",
    ],
    [
        [
            "admin@fluidattacks.com",
            "3c475384-834c-47b0-ac71-a41a022e401c",
            "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
        ],
    ],
)
async def test_streams_process_vulns(
    populate: bool,
    email: str,
    finding_id: str,
    vulnerability_id: str,
) -> None:
    assert populate

    partition_key: str = f"VULN#{vulnerability_id}"
    sort_key: str = f"FIN#{finding_id}"

    query: str = f""""
    "match": {{
        "id": "{vulnerability_id}"
    }}
    """
    search_result = await search(
        index="vulnerabilities", limit=10, query=query
    )

    assert search_result.total == 1

    item = search_result.items[0]

    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
    assert item["state"]["status"] == VulnerabilityStateStatus.VULNERABLE

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vulnerability_id
    )

    assert "errors" not in result

    await sleep(5)

    search_result = await search(
        index="vulnerabilities", limit=10, query=query
    )

    assert search_result.total == 1

    item = search_result.items[0]

    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
    assert item["state"]["status"] == VulnerabilityStateStatus.DELETED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("streams_process_vulns")
@pytest.mark.parametrize(
    [
        "email",
        "finding_id",
        "vulnerability_id",
    ],
    [
        [
            "hacker@gmail.com",
            "475041514",
            "c99e0bd7-23e0-47b7-801c-50f9f8b585b0",
        ],
        [
            "reattacker@gmail.com",
            "475041514",
            "c99e0bd7-23e0-47b7-801c-50f9f8b585b0",
        ],
    ],
)
async def test_streams_process_vulns_not_add(
    populate: bool,
    email: str,
    finding_id: str,
    vulnerability_id: str,
) -> None:
    assert populate

    partition_key: str = f"VULN#{vulnerability_id}"
    sort_key: str = f"FIN#{finding_id}"
    query: str = f""""
    "match": {{
        "id": "{vulnerability_id}"
    }}
    """
    search_result = await search(
        index="vulnerabilities", limit=10, query=query
    )

    assert search_result.total == 1

    item = search_result.items[0]

    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
    assert item["state"]["status"] == VulnerabilityStateStatus.VULNERABLE

    result: dict[str, Any] = await get_result(
        user=email, finding=finding_id, vulnerability=vulnerability_id
    )

    assert "errors" in result

    search_result = await search(
        index="vulnerabilities", limit=10, query=query
    )

    assert search_result.total == 1

    item = search_result.items[0]

    assert item["pk"] == partition_key
    assert item["sk"] == sort_key
    assert item["state"]["status"] == VulnerabilityStateStatus.VULNERABLE
