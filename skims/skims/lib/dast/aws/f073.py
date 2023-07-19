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
    if db_instances:
        for index, instance in enumerate(db_instances):
            instance_arn = instance["DBInstanceArn"]
            locations: list[Location] = []

            if instance.get("PubliclyAccessible", False):
                locations = [
                    Location(
                        access_patterns=(f"/{index}/PubliclyAccessible",),
                        arn=(f"{instance_arn}"),
                        values=(instance["PubliclyAccessible"],),
                        description=t("f073.rds_is_publicly_accessible"),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_HAS_PUBLIC_INSTANCES),
                    aws_response=db_instances,
                ),
            )
    return vulns


def _get_vulns_db_clusters(response: dict[str, Any]) -> core.Vulnerabilities:
    db_clusters = response.get("DBClusters", []) if response else []
    vulns: core.Vulnerabilities = ()
    if db_clusters:
        for index, clusters in enumerate(db_clusters):
            cluster_arn = clusters["DBClusterArn"]
            locations: list[Location] = []
            if clusters.get("PubliclyAccessible", False):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(f"/{index}/PubliclyAccessible",),
                        arn=(f"{cluster_arn}"),
                        values=(clusters["PubliclyAccessible"],),
                        description=t("f073.rds_is_publicly_accessible"),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_HAS_PUBLIC_INSTANCES),
                    aws_response=db_clusters,
                ),
            )
    return vulns


async def has_public_instances(
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


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (has_public_instances,)
