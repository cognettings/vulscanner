from authz.model.types import (
    RoleLevel,
)

SERVICE_FORCES_ROLE: dict[str, RoleLevel] = dict(
    group_level=RoleLevel(
        actions={
            "api_mutations_add_forces_execution_mutate",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_root_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
        },
        tags={"forces"},
    ),
)
