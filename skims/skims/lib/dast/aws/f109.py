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


def _get_vuln_db_instances(response: dict[str, Any]) -> core.Vulnerabilities:
    db_instances = response.get("DBInstances", []) if response else []
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_NOT_INSIDE_A_DB_SUBNET_GROUP
    if db_instances:
        for instance in db_instances:
            instance_arn = instance["DBInstanceArn"]
            locations: list[Location] = []

            if not instance.get("DBSubnetGroup", {}):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"{instance_arn}"),
                        values=(),
                        description=t(
                            "f109.rds_is_not_inside_a_db_subnet_group"
                        ),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=db_instances,
                ),
            )
    return vulns


def _get_vulns_db_clusters(response: dict[str, Any]) -> core.Vulnerabilities:
    db_clusters = response.get("DBClusters", []) if response else []
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_NOT_INSIDE_A_DB_SUBNET_GROUP
    if db_clusters:
        for clusters in db_clusters:
            cluster_arn = clusters["DBClusterArn"]
            locations: list[Location] = []
            if not clusters.get("DBSubnetGroup", {}):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(),
                        arn=(f"{cluster_arn}"),
                        values=(),
                        description=t(
                            "f109.rds_is_not_inside_a_db_subnet_group"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=db_clusters,
                ),
            )
    return vulns


async def is_not_inside_a_db_subnet_group(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    vulns: core.Vulnerabilities = ()
    describe_db_instances: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )

    describe_db_clusters: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_clusters"
    )
    vulns = (
        *_get_vuln_db_instances(describe_db_instances),
        *_get_vulns_db_clusters(describe_db_clusters),
    )

    return vulns


async def rds_unrestricted_db_security_groups(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_RDS_UNRESTRICTED_DB_SECURITY_GROUPS
    describe_db_instances: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )
    db_instances = (
        describe_db_instances.get("DBInstances", [])
        if describe_db_instances
        else []
    )
    locations: list[Location] = []
    for instance in db_instances:
        security_groups_ids = list(
            map(
                lambda x: x["VpcSecurityGroupId"],
                instance["VpcSecurityGroups"],
            )
        )
        describe_security_groups: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="ec2",
            function="describe_security_groups",
            parameters={"GroupIds": security_groups_ids},
        )
        security_groups = describe_security_groups.get("SecurityGroups", [])
        for group in security_groups:
            for ip_permission in group["IpPermissions"]:
                locations = [
                    *locations,
                    *[
                        Location(
                            access_patterns=(f"/IpRanges/{index}/CidrIp",),
                            arn=(
                                "arn:aws:rds::"
                                f"VpcSecurityGroupId:{group['GroupId']}"
                            ),
                            values=(ip_range["CidrIp"],),
                            description=t(
                                "f109.rds_unrestricted_db_security_groups"
                            ),
                        )
                        for index, ip_range in enumerate(
                            ip_permission["IpRanges"]
                        )
                        if ip_range["CidrIp"] == "0.0.0.0/0"
                    ],
                ]

                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=ip_permission,
                    ),
                )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    is_not_inside_a_db_subnet_group,
    rds_unrestricted_db_security_groups,
)
