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


async def get_paginated_items(
    credentials: AwsCredentials,
) -> list:
    """Get all items in paginated API calls."""
    pools: list[dict] = []
    args: dict[str, Any] = {
        "credentials": credentials,
        "service": "efs",
        "function": "describe_file_systems",
        "parameters": {"MaxItems": 50},
    }
    data = await run_boto3_fun(**args)
    object_name = "FileSystems"
    pools += data.get(object_name, [])

    next_token = data.get("NextMarker", None)
    while next_token:
        args["parameters"]["Marker"] = next_token
        data = await run_boto3_fun(**args)
        pools += data.get(object_name, [])
        next_token = data.get("NextMarker", None)

    return pools


async def efs_is_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_EFS_IS_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    filesystems = await get_paginated_items(credentials)
    for filesystem in filesystems:
        locations: list[Location] = []
        if not filesystem.get("Encrypted"):
            locations = [
                Location(
                    arn=(filesystem["FileSystemArn"]),
                    description=t("f406.aws_efs_unencrypted"),
                    values=(filesystem["Encrypted"],),
                    access_patterns=("/Encrypted",),
                ),
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=filesystem,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (efs_is_encryption_disabled,)
