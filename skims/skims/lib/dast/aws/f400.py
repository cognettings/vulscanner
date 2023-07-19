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


async def elbv2_has_access_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elbv2", function="describe_load_balancers"
    )
    method = core.MethodsEnum.AWS_ELBV2_HAS_ACCESS_LOGGING_DISABLED
    balancers = response.get("LoadBalancers", []) if response else []
    vulns: core.Vulnerabilities = ()
    if balancers:
        for balancer in balancers:
            load_balancer_arn = balancer["LoadBalancerArn"]
            locations: list[Location] = []
            key_rotation: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="elbv2",
                function="describe_load_balancer_attributes",
                parameters={"LoadBalancerArn": str(load_balancer_arn)},
            )
            attributes = key_rotation.get("Attributes", "")

            for index, attrs in enumerate(attributes):
                if (
                    attrs["Key"] == "access_logs.s3.enabled"
                    and attrs["Value"] != "true"
                ):
                    locations = [
                        *locations,
                        Location(
                            arn=(balancer["LoadBalancerArn"]),
                            description=t(
                                "f400.elb2_has_access_logs_s3_disabled"
                            ),
                            values=(attrs["Key"],),
                            access_patterns=(f"/{index}/Key",),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=attributes,
                ),
            )

    return vulns


async def cloudfront_has_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    method = core.MethodsEnum.AWS_CLOUDFRONT_HAS_LOGGING_DISABLED
    distributions = response.get("DistributionList", {}) if response else {}
    vulns: core.Vulnerabilities = ()
    if distributions:
        for dist in distributions["Items"]:
            dist_id = dist["Id"]
            dist_arn = dist["ARN"]
            locations: list[Location] = []
            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution",
                parameters={"Id": str(dist_id)},
            )
            distribution = config.get("Distribution", "")
            distribution_config = distribution.get("DistributionConfig", {})
            is_logging_enabled = distribution_config["Logging"]["Enabled"]
            if not is_logging_enabled:
                locations = [
                    *locations,
                    Location(
                        arn=(dist_arn),
                        description=t("f400.has_logging_disabled"),
                        values=(is_logging_enabled,),
                        access_patterns=(
                            "/DistributionConfig/Logging/Enabled",
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=distribution,
                ),
            )

    return vulns


async def cloudtrail_trails_not_multiregion(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core.MethodsEnum.AWS_CLOUDTRAIL_TRAILS_NOT_MULTIREGION
    trails = response.get("trailList", []) if response else []
    vulns: core.Vulnerabilities = ()
    if trails:
        for trail in trails:
            trail_arn = trail["TrailARN"]
            locations: list[Location] = []
            if not trail["IsMultiRegionTrail"]:
                locations = [
                    Location(
                        arn=(trail_arn),
                        description=t("f400.trails_not_multiregion"),
                        values=(trail["IsMultiRegionTrail"],),
                        access_patterns=("/IsMultiRegionTrail",),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=trail,
                ),
            )

    return vulns


async def is_trail_bucket_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core.MethodsEnum.AWS_IS_TRAIL_BUCKET_LOGGING_DISABLED
    trails = response.get("trailList", []) if response else []
    vulns: core.Vulnerabilities = ()
    if trails:
        for trail in trails:
            locations: list[Location] = []
            t_arn = trail["TrailARN"]
            t_bucket = trail["S3BucketName"]
            logging: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_logging",
                parameters={"Bucket": t_bucket},
            )
            if not logging.get("LoggingEnabled"):
                locations = [
                    Location(
                        arn=(t_arn),
                        description=t("f400.is_trail_bucket_logging_disabled"),
                        values=(),
                        access_patterns=(),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=trail,
                ),
            )

    return vulns


async def s3_has_server_access_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    method = core.MethodsEnum.AWS_S3_HAS_ACCESS_LOGGING_DISABLED
    buckets = response.get("Buckets", {}) if response else {}
    vulns: core.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            bucket_name = bucket["Name"]
            locations: list[Location] = []
            bucket_logging: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_logging",
                parameters={"Bucket": str(bucket_name)},
            )

            bucket_logging_enabled = bool(bucket_logging.get("LoggingEnabled"))
            if not bucket_logging_enabled:
                locations = [
                    *locations,
                    Location(
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        description=t("f400.bucket_has_logging_disabled"),
                        values=(),
                        access_patterns=(),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=bucket_logging,
                ),
            )

    return vulns


async def ec2_monitoring_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    reservations = response.get("Reservations", []) if response else []
    method = core.MethodsEnum.AWS_EC2_MONITORING_DISABLED
    vulns: core.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            locations: list[Location] = []
            for index, i in enumerate(instances["Instances"]):
                monitoring = i.get("Monitoring", "")
                if monitoring["State"] != "enabled":
                    locations = [
                        *locations,
                        Location(
                            arn=(
                                f"arn:aws:ec2::{instances['OwnerId']}:"
                                f"instance-id/{i['InstanceId']}"
                            ),
                            description=t("f400.bucket_has_logging_disabled"),
                            values=(monitoring["State"],),
                            access_patterns=(
                                f"/Instances/{index}/Monitoring/State",
                            ),
                        ),
                    ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=instances,
                ),
            )
    return vulns


async def cf_distribution_has_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudfront", function="list_distributions"
    )
    method = core.MethodsEnum.AWS_CF_DISTRIBUTION_HAS_LOGGING_DISABLED
    distributions = response.get("DistributionList", {}) if response else {}
    vulns: core.Vulnerabilities = ()
    if distributions:
        for dist in distributions["Items"]:
            dist_id = dist["Id"]
            dist_arn = dist["ARN"]
            locations: list[Location] = []
            config: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="cloudfront",
                function="get_distribution_config",
                parameters={"Id": str(dist_id)},
            )
            distribution_config = config.get("DistributionConfig", {})
            logging = distribution_config.get("Logging", "")
            if not logging["Enabled"]:
                locations = [
                    *locations,
                    Location(
                        arn=(dist_arn),
                        description=t("f400.has_logging_disabled"),
                        values=(logging["Enabled"],),
                        access_patterns=("/Logging/Enabled",),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=distribution_config,
                ),
            )

    return vulns


async def eks_has_disable_cluster_logging(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="eks", function="list_clusters"
    )
    method = core.MethodsEnum.AWS_EKS_HAS_DISABLED_CLUSTER_LOGGING
    cluster_names = response.get("clusters", []) if response else []
    vulns: core.Vulnerabilities = ()
    locations: list[Location] = []
    for cluster in cluster_names:
        cluster_desc = await run_boto3_fun(
            credentials,
            service="eks",
            function="describe_cluster",
            parameters={"name": str(cluster)},
        )
        cluster_attrs = dict(cluster_desc["cluster"])
        for log in cluster_attrs["logging"]["clusterLogging"]:
            if not log["enabled"]:
                locations = [
                    Location(
                        arn=(cluster_attrs["arn"]),
                        description=t("f400.eks_has_disable_cluster_logging"),
                        values=(log["enabled"],),
                        access_patterns=("/enabled",),
                    ),
                ]

                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=log,
                    ),
                )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    is_trail_bucket_logging_disabled,
    ec2_monitoring_disabled,
    elbv2_has_access_logging_disabled,
    cloudfront_has_logging_disabled,
    cloudtrail_trails_not_multiregion,
    s3_has_server_access_logging_disabled,
    cf_distribution_has_logging_disabled,
    eks_has_disable_cluster_logging,
)
