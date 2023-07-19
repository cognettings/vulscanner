from .schema import (
    GROUP,
)
from custom_utils.vulnerabilities import (
    get_inverted_state_converted,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    VulnerabilityEdge,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
    get_inverted_treatment_converted,
)
from graphql import (
    GraphQLResolveInfo,
)
import logging
from search.operations import (
    search,
)
from typing import (
    Any,
)
from vulnerabilities.domain.core import (
    get_vulns_filters_by_root_nickname,
)

LOGGER = logging.getLogger(__name__)


@GROUP.field("vulnerabilities")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    group_name = parent.name
    loaders: Dataloaders = info.context.loaders
    vulnerabilities_filters: dict[str, Any] = await vulnerabilities_filter(
        loaders, group_name, **kwargs
    )

    results = await search(
        after=kwargs.get("after"),
        exact_filters={"group_name": parent.name},
        must_filters=vulnerabilities_filters["must_filters"],
        should_match_prefix_filters=vulnerabilities_filters[
            "should_match_prefix_filters"
        ],
        must_not_filters=vulnerabilities_filters["must_not_filters"],
        index="vulnerabilities",
        limit=kwargs.get("first", 10),
        should_and_filters=vulnerabilities_filters["should_and_filters"],
        query=kwargs.get("search"),
    )

    vulnerabilities = tuple(
        format_vulnerability(result) for result in results.items
    )

    return VulnerabilitiesConnection(
        edges=tuple(
            VulnerabilityEdge(
                cursor=results.page_info.end_cursor,
                node=vulnerability,
            )
            for vulnerability in vulnerabilities
        ),
        page_info=results.page_info,
        total=results.total,
    )


async def vulnerabilities_filter(
    loaders: Dataloaders, group_name: str, **kwargs: Any
) -> dict[str, Any]:
    vulns_must_filters: list[dict[str, Any]] = must_filter(**kwargs)
    vulns_should_match_prefix_filters: list[
        dict[str, Any]
    ] = should_match_prefix_filter(**kwargs)
    vulns_must_not_filters: list[dict[str, Any]] = must_not_filter(**kwargs)
    vulns_should_and_filter = await should_and_filter(
        loaders, group_name, **kwargs
    )

    if zero_risk := kwargs.get("zero_risk"):
        vulns_must_filters.append({"zero_risk.status": zero_risk})
    else:
        vulns_must_not_filters.append(
            {"zero_risk.status": VulnerabilityZeroRiskStatus.REQUESTED}
        )

    filters: dict[str, Any] = {
        "must_filters": vulns_must_filters,
        "should_match_prefix_filters": vulns_should_match_prefix_filters,
        "must_not_filters": vulns_must_not_filters,
        "should_and_filters": vulns_should_and_filter,
    }

    return filters


def must_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_filters = []

    if vulnerability_type := kwargs.get("type"):
        must_filters.append({"type": str(vulnerability_type).upper()})

    if state := kwargs.get("state_status"):
        must_filters.append(
            {"state.status": get_inverted_state_converted(str(state).upper())}
        )

    if treatment := kwargs.get("treatment"):
        must_filters.append(
            {
                "treatment.status": get_inverted_treatment_converted(
                    str(treatment).upper()
                )
            }
        )

    if verification := kwargs.get("verification_status"):
        if verification != "NotRequested":
            must_filters.append(
                {"verification.status": str(verification).upper()}
            )

    return must_filters


def should_match_prefix_filter(**kwargs: Any) -> list[dict[str, Any]]:
    should_match_prefix_filters = []

    if root := kwargs.get("root"):
        should_match_prefix_filters.append({"state.where": str(root)})

    return should_match_prefix_filters


def must_not_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_not_filters: list[dict[str, Any]] = [
        {"state.status": VulnerabilityStateStatus.DELETED.value},
        {"state.status": VulnerabilityStateStatus.MASKED.value},
        {"state.status": VulnerabilityStateStatus.REJECTED.value},
        {"state.status": VulnerabilityStateStatus.SUBMITTED.value},
        {"zero_risk.status": VulnerabilityZeroRiskStatus.CONFIRMED.value},
    ]
    if verification := kwargs.get("verification_status"):
        if verification == "NotRequested":
            must_not_filters.append({"verification.status": "REQUESTED"})
            must_not_filters.append({"verification.status": "ON_HOLD"})
            must_not_filters.append(
                {"state.status": VulnerabilityStateStatus.SAFE.value}
            )

    return must_not_filters


async def should_and_filter(
    loaders: Dataloaders, group_name: str, **kwargs: Any
) -> list[dict[str, Any]]:
    if root := kwargs.get("root"):
        return await get_vulns_filters_by_root_nickname(
            loaders, group_name, root
        )

    return []
