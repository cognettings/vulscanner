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


async def has_default_security_groups_in_use(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    reservations = response.get("Reservations", []) if response else []
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_HAS_DEFAULT_SECURITY_GROUPS_IN_USE
    for res in reservations:
        for instance in res["Instances"]:
            locations: list[Location] = []
            for index, security_group in enumerate(instance["SecurityGroups"]):
                group_name = security_group["GroupName"]
                if "default" in group_name:
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    f"/SecurityGroups/{index}/GroupName",
                                ),
                                arn=(f"arn:aws:ec2::{instance['InstanceId']}"),
                                values=(instance["SecurityGroups"],),
                                description=t(
                                    "src.lib_path.f177."
                                    "has_default_security_groups_in_use"
                                ),
                            )
                        ],
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=instance,
                ),
            )
    return vulns


async def use_default_security_group(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    security_group_attributes = {"SecurityGroups", "SecurityGroupIds"}
    method = core.MethodsEnum.AWS_DEFAULT_SECURITY_GROUP
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_launch_template_versions",
        parameters={
            "Versions": ["$Latest"],
        },
    )
    vulns: core.Vulnerabilities = ()

    launch_template_versions = response.get("LaunchTemplateVersions", {})
    if launch_template_versions:
        for template_version in launch_template_versions:
            locations: list[Location] = []
            template_data = template_version.get("LaunchTemplateData", {})
            if not any(
                template_data.get(attr, False)
                for attr in security_group_attributes
            ):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(
                            "arn:aws:ec2:::"
                            f"{template_version['LaunchTemplateId']}"
                        ),
                        values=(),
                        description=t(
                            "lib_path.f177.ec2_using_default_security_group"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=template_version,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    use_default_security_group,
    has_default_security_groups_in_use,
)
