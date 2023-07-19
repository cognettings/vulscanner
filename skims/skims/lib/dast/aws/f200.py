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


async def redshift_has_audit_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_REDSHIFT_HAS_AUDIT_LOGS_DISABLED
    vulns: core.Vulnerabilities = ()
    locations: list[Location] = []
    clusters = await redshift_get_paginated_items(credentials)
    for cluster in clusters:
        cluster_id = cluster["ClusterIdentifier"]
        logging: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="redshift",
            function="describe_logging_status",
            parameters={
                "ClusterIdentifier": cluster_id,
            },
        )
        logging_enabled = logging.get("LoggingEnabled")
        if not logging_enabled:
            locations = [
                Location(
                    arn=(
                        "arn:aws:redshift::cluster:"
                        f"{cluster['ClusterIdentifier']}"
                    ),
                    description=t(
                        "src.lib_path.f200.redshift_has_audit_logging_disabled"
                    ),
                    values=(logging_enabled,),
                    access_patterns=("/LoggingEnabled",),
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=logging,
                ),
            )

    return vulns


async def redshift_is_user_activity_logging_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_REDSHIFT_HAS_USER_ACTIVITY_LOG_DISABLED
    vulns: core.Vulnerabilities = ()
    locations: list[Location] = []
    clusters = await redshift_get_paginated_items(credentials)
    for cluster in clusters:
        param_groups = cluster.get("ClusterParameterGroups", [])

        for group in param_groups:
            describe_cluster_parameters: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="redshift",
                function="describe_cluster_parameters",
                parameters={
                    "ParameterGroupName": group["ParameterGroupName"],
                },
            )
            params = describe_cluster_parameters.get("Parameters", [])

            for param in params:
                if (
                    param["ParameterName"] == "enable_user_activity_logging"
                    and param["ParameterValue"] == "false"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:redshift::cluster:"
                                f"{cluster['ClusterIdentifier']}"
                            ),
                            description=t(
                                "src.lib_path.f200."
                                "redshift_is_user_activity_logging_disabled"
                            ),
                            values=(
                                param["ParameterName"],
                                param["ParameterValue"],
                            ),
                            access_patterns=(
                                "/ParameterName",
                                "/ParameterValue",
                            ),
                        ),
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=param,
                        ),
                    )

    return vulns


async def vpcs_without_flowlog(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_vpcs",
        parameters={"Filters": [{"Name": "state", "Values": ["available"]}]},
    )
    vpcs = response.get("Vpcs", []) if response else []
    vulns: core.Vulnerabilities = ()
    if vpcs:
        for vpc in vpcs:
            locations: list[Location] = []
            cloud_id = vpc["VpcId"]
            net_interfaces: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="ec2",
                function="describe_flow_logs",
                parameters={
                    "Filters": [{"Name": "resource-id", "Values": [cloud_id]}]
                },
            )
            if not net_interfaces.get("FlowLogs"):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"arn:aws:vpc:::{cloud_id}"),
                        values=(),
                        description=t(
                            "src.lib_path.f200.vpcs_without_flowlog"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_VPC_WITHOUT_FLOWLOG),
                    aws_response=vpc,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    redshift_has_audit_logging_disabled,
    vpcs_without_flowlog,
    redshift_is_user_activity_logging_disabled,
)
