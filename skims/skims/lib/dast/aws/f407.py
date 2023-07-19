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


async def ebs_has_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_volumes"
    )
    volumes = response.get("Volumes") if response else None
    method = core.MethodsEnum.AWS_EBS_HAS_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()

    if volumes:
        for volume in volumes:
            locations: list[Location] = []
            if not volume.get("Encrypted", False):
                locations = [
                    Location(
                        arn=(f"arn:aws:ec2:::VolumeId/{volume['VolumeId']}"),
                        description=t("f407.cfn_aws_ebs_volumes_unencrypted"),
                        values=(),
                        access_patterns=(),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=volume,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (ebs_has_encryption_disabled,)
