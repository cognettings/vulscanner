from dataloaders import (
    get_new_context,
)
from organizations.domain import (
    get_group_names,
)
import pytest
from schedulers.organization_vulnerabilities import (
    get_data,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_vulnerabilities")
async def test_organization_vulnerabilities_rows(populate: bool) -> None:
    assert populate

    loaders = get_new_context()
    org_id = "ORG#c4fc4bde-93fa-44d1-981b-9ce16c5435e8"
    org_name = "test_organization_1"
    all_groups_names = await get_group_names(loaders, org_id)

    rows: list[list[str]] = await get_data(
        groups=tuple(all_groups_names),
        loaders=loaders,
        organization_name=org_name,
    )

    assert len(rows) == 1
    assert len(rows[0]) == 54
    assert rows[0][-1] == "Group"

    org_id = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name = "orgtest"
    all_groups_names = await get_group_names(loaders, org_id)
    rows = await get_data(
        groups=tuple(all_groups_names),
        loaders=loaders,
        organization_name=org_name,
    )

    assert len(rows) == 6
    assert rows[0][-1] == "Group"
    assert rows[1][-1] == "group1"
    assert rows[0][-2] == "Severity Level"
    assert rows[1][-2] == "Medium"
