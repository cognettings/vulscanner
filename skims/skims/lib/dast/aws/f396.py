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


async def kms_key_is_key_rotation_absent_or_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_keys"
    )
    method = core.MethodsEnum.AWS_KMS_IS_KEY_ROTATION_DISABLED
    keys = response.get("Keys", []) if response else []
    vulns: core.Vulnerabilities = ()
    if keys:
        for key in keys:
            locations: list[Location] = []
            key_rotation: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="kms",
                function="get_key_rotation_status",
                parameters={"KeyId": str(key["KeyId"])},
            )
            key_rotation_status = key_rotation.get("KeyRotationEnabled", "")

            if str(key_rotation_status) == "False":
                locations = [
                    *locations,
                    Location(
                        arn=(key["KeyArn"]),
                        description=t(
                            "src.lib_path.f396."
                            "kms_key_is_key_rotation_absent_or_disabled"
                        ),
                        values=(key_rotation["KeyRotationEnabled"],),
                        access_patterns=("/KeyRotationEnabled",),
                    ),
                ]
            elif not key_rotation_status:
                locations = [
                    *locations,
                    Location(
                        arn=(key["KeyArn"]),
                        description=t(
                            "src.lib_path.f396."
                            "kms_key_is_key_rotation_absent_or_disabled"
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
                    aws_response=key_rotation,
                ),
            )

    return vulns


async def secrets_manager_has_automatic_rotation_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    describe_file_systems: dict[str, Any] = await run_boto3_fun(
        credentials, service="secretsmanager", function="list_secrets"
    )
    secrets = describe_file_systems.get("SecretList", [])

    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_SECRETS_HAS_AUTOMATIC_ROTATION_DISABLED
    for secret_ in secrets:
        description: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="secretsmanager",
            function="describe_secret",
            parameters={"SecretId": secret_["Name"]},
        )
        rot_enabled = description.get("RotationEnabled", "")
        if not rot_enabled:
            locations = [
                Location(
                    arn=(description["ARN"]),
                    description=t(
                        "src.lib_path.f396."
                        "secrets_manager_has_automatic_rotation_disabled"
                    ),
                    values=(description["RotationEnabled"],)
                    if rot_enabled is False
                    else (),
                    access_patterns=("/RotationEnabled",)
                    if rot_enabled is False
                    else (),
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=description,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    kms_key_is_key_rotation_absent_or_disabled,
    secrets_manager_has_automatic_rotation_disabled,
)
