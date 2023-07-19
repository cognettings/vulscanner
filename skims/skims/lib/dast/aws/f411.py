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


async def ebs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_volumes"
    )
    method = core.MethodsEnum.AWS_EBS_USES_DEFAULT_KMS_KEY
    volumes = response.get("Volumes", []) if response else []
    vulns: core.Vulnerabilities = ()
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    locations: list[Location] = []
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []
    for volume in volumes:
        vol_key = volume.get("KmsKeyId", "")
        if vol_key:
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and alias.get("AliasName") == "alias/aws/ebs"
                ):
                    locations = [
                        Location(
                            arn=(
                                f"arn:aws:ec2:::VolumeId/{volume['VolumeId']}"
                            ),
                            description=t(
                                "lib_path.f411.ebs_uses_default_kms_key"
                            ),
                            values=(alias,),
                            access_patterns=("/TargetKeyId",),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


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


async def efs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    filesystems = await get_paginated_items(credentials)
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_EFS_USES_DEFAULT_KMS_KEY
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []
    for filesystem in filesystems:
        vol_key = filesystem.get("KmsKeyId", "")
        if vol_key:
            locations: list[Location] = []
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and str(alias.get("AliasName", ""))
                    == "alias/aws/elasticfilesystem"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:ec2:::FileSystemId/"
                                f"{filesystem['FileSystemId']}"
                            ),
                            description=t(
                                "lib_path.f411.efs_uses_default_kms_key"
                            ),
                            values=(),
                            access_patterns=(),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


async def fsx_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    describe_file_systems: dict[str, Any] = await run_boto3_fun(
        credentials, service="fsx", function="describe_file_systems"
    )
    filesystems = (
        describe_file_systems.get("FileSystems", [])
        if describe_file_systems
        else []
    )

    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_FSX_USES_DEFAULT_KMS_KEY
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []

    for filesystem in filesystems:
        if vol_key := filesystem.get("KmsKeyId", ""):
            locations: list[Location] = []
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and str(alias.get("AliasName", "")) == "alias/aws/fsx"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:ec2:::FileSystemId/"
                                f"{filesystem['FileSystemId']}"
                            ),
                            description=t(
                                "lib_path.f411.efs_uses_default_kms_key"
                            ),
                            values=(),
                            access_patterns=(),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


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


async def redshift_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_REDSHIFT_USES_DEFAULT_KMS_KEY
    vulns: core.Vulnerabilities = ()
    list_aliases: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_aliases"
    )
    locations: list[Location] = []
    kms_aliases = list_aliases.get("Aliases", []) if list_aliases else []
    clusters = await redshift_get_paginated_items(credentials)
    for cluster in clusters:
        if vol_key := cluster.get("KmsKeyId", ""):
            for alias in kms_aliases:
                if (
                    alias.get("TargetKeyId", "") == vol_key.split("/")[1]
                    and alias.get("AliasName") == "alias/aws/redshift"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:redshift::cluster:"
                                f"{cluster['ClusterIdentifier']}"
                            ),
                            description=t(
                                "lib_path.f411.redshift_uses_default_kms_key"
                            ),
                            values=(alias,),
                            access_patterns=("/TargetKeyId",),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=alias,
                        ),
                    )

    return vulns


async def secrets_encrypted_with_default_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    describe_file_systems: dict[str, Any] = await run_boto3_fun(
        credentials, service="secretsmanager", function="list_secrets"
    )
    secrets = describe_file_systems.get("SecretList", [])

    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_FSX_USES_DEFAULT_KMS_KEY

    for key in secrets:
        describe_key: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="kms",
            function="describe_key",
            parameters={"KeyId": str(key["KmsKeyId"])},
        )
        key_description = describe_key.get("KeyMetadata", {})
        if key_description.get("KeyManager", "") == "AWS":
            locations = [
                Location(
                    arn=(key_description["Arn"]),
                    description=t("lib_path.f411.efs_uses_default_kms_key"),
                    values=(key_description["KeyManager"],),
                    access_patterns=("/KeyManager",),
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=key_description,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    ebs_uses_default_kms_key,
    efs_uses_default_kms_key,
    fsx_uses_default_kms_key,
    secrets_encrypted_with_default_keys,
    redshift_uses_default_kms_key,
)
