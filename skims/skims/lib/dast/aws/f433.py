from collections.abc import (
    Callable,
    Coroutine,
)
from lib.dast.aws.types import (
    Location,
)
from lib.dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core,
)
from model.core import (
    AwsCredentials,
    Vulnerability,
)
from typing import (
    Any,
)
from zone import (
    t,
)


async def redshift_get_paginated_items(
    credentials: AwsCredentials,
) -> list:
    """Get all items in paginated API calls."""
    pools: list[dict] = []
    args: dict[str, Any] = {
        "credentials": credentials,
        "service": "redshift",
        "function": "describe_clusters",
        "parameters": {"MaxRecords": 50},
    }
    data = await run_boto3_fun(**args)
    object_name = "Clusters"
    pools += data.get(object_name, [])

    next_token = data.get("Marker", None)
    while next_token:
        args["parameters"]["Marker"] = next_token
        data = await run_boto3_fun(**args)
        pools += data.get(object_name, [])
        next_token = data.get("Marker", None)

    return pools


async def redshift_has_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    clusters = await redshift_get_paginated_items(credentials)
    method = core.MethodsEnum.AWS_REDSHIFT_HAS_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    for cluster in clusters:
        locations: list[Location] = []
        if not cluster["Encrypted"]:
            locations = [
                Location(
                    access_patterns=("/Encrypted",),
                    arn=(
                        "arn:aws:redshift::cluster:"
                        f"{cluster['ClusterIdentifier']}"
                    ),
                    values=(cluster["Encrypted"],),
                    description=t(
                        "lib_dast.f433.redshift_has_encryption_disabled"
                    ),
                )
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=cluster,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (redshift_has_encryption_disabled,)
