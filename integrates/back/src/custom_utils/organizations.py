from collections.abc import (
    Iterable,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
)
from pycountry import (
    countries,
)
from typing import (
    Any,
)


def is_deleted(organization: Organization) -> bool:
    return organization.state.status == OrganizationStateStatus.DELETED


def filter_active_organizations(
    organizations: Iterable[Organization],
) -> list[Organization]:
    return [
        organization
        for organization in organizations
        if not is_deleted(organization)
    ]


def get_organization_country(context: Any) -> str:
    country_code = context.headers.get("cf-ipcountry", "undefined")
    return (
        country_code
        if country_code == "undefined"
        else countries.get(alpha_2=country_code).name
    )
