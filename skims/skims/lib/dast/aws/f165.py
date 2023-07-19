# pylint: disable=too-many-lines

from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
)
import csv
from io import (
    StringIO,
)
import json
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


async def users_with_multiple_access_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_USER_WITH_MULTIPLE_ACCESS_KEYS
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_users",
    )
    vulns: core.Vulnerabilities = ()

    users = response.get("Users", [])

    if users:
        for user in users:
            access_keys: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_access_keys",
                parameters={
                    "UserName": user["UserName"],
                },
            )
            access_key_metadata = (
                access_keys["AccessKeyMetadata"] if access_keys else {}
            )
            locations: list[Location] = []
            access_keys_activated = list(
                filter(
                    lambda y: y == "Active",
                    list(
                        map(lambda attr: attr["Status"], access_key_metadata)
                    ),
                )
            )
            if len(access_keys_activated) > 1:
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"arn:aws:iam:::{user['UserName']}"),
                        values=(),
                        description=t("f165.users_with_multiple_access_keys"),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=access_key_metadata,
                ),
            )

    return vulns


async def root_has_access_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    locations: list[Location] = []
    vulns: core.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))

    key_names = ("access_key_1_active", "access_key_2_active")
    with suppress(KeyError):
        if credentials_report:
            root_user = credentials_report[0]
            root_arn = root_user["arn"]
            for index, name in enumerate(key_names):
                if root_user.get(name) == "true":
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/{key_names[index]}",),
                            arn=(f"{root_arn}"),
                            values=(root_user[key_names[index]],),
                            description=t("f165.root_has_access_keys"),
                        ),
                    ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_IAM_ROOT_HAS_ACCESS_KEYS),
                    aws_response=root_user,  # type: ignore
                ),
            )

    return vulns


async def has_not_support_role(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_IAM_HAS_NOT_SUPPORT_ROLE
    vulns: core.Vulnerabilities = ()
    attached_times: int = 0
    policy_arn = "arn:aws:iam::aws:policy/AWSSupportAccess"
    entities: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_entities_for_policy",
        parameters={
            "PolicyArn": policy_arn,
        },
    )

    locations: list[Location] = []
    attached_times = (
        len(list(filter(None, entities.get("PolicyUsers", []))))
        + len(list(filter(None, entities.get("PolicyGroups", []))))
        + len(list(filter(None, entities.get("PolicyRoles", []))))
    )
    if entities and attached_times == 0:
        locations = [
            Location(
                access_patterns=(),
                arn=(f"{policy_arn}"),
                values=(),
                description=t("f165.has_not_support_role"),
            ),
        ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(method),
                aws_response=entities,
            ),
        )

    return vulns


async def has_root_active_signing_certificates(  # NOSONAR
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_IAM_HAS_ROOT_ACTIVE_SIGNING_CERTIFICATES
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    vulns: core.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    if credentials_report:
        root_user = credentials_report[0]
        root_arn = root_user["arn"]
        root_has_active_signing_certs: bool = any(
            (
                root_user.get("cert_1_active", "") == "true",
                root_user.get("cert_2_active", "") == "true",
            )
        )
        locations: list[Location] = []
        if root_has_active_signing_certs:
            key_names = ("cert_1_active", "cert_2_active")
            for index, name in enumerate(key_names):
                if root_user.get(name) == "true":
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/{key_names[index]}",),
                            arn=(f"{root_arn}"),
                            values=(root_user[key_names[index]],),
                            description=t(
                                "f165.has_root_active_signing_certificates"
                            ),
                        ),
                    ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(method),
                aws_response=root_user,  # type: ignore
            ),
        )

    return vulns


async def dynamob_encrypted_with_aws_master_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="dynamodb", function="list_tables"
    )
    table_names = response.get("TableNames", []) if response else []
    method = core.MethodsEnum.AWS_DYNAMODB_ENCRYPTED_WITH_AWS_MASTER_KEYS
    vulns: core.Vulnerabilities = ()
    if table_names:
        for table_name in table_names:
            locations: list[Location] = []

            describe_table: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_table",
                parameters={
                    "TableName": table_name,
                },
            )
            table_arn = describe_table["Table"]["TableArn"]
            table = describe_table["Table"]
            try:
                table_ssetype = table["SSEDescription"]["SSEType"]
                if table_ssetype == "AES256":
                    locations = [
                        Location(
                            access_patterns=("/SSEDescription/SSEType",),
                            arn=(table_arn),
                            values=(table_ssetype,),
                            description=t(
                                "f165."
                                "dynamob_encrypted_with_aws_master_keys"
                            ),
                        ),
                    ]
                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=table,
                        ),
                    )

            except KeyError:
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(table_arn),
                        values=(),
                        description=t(
                            "f165.dynamob_encrypted_with_aws_master_keys"
                        ),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=table,
                    ),
                )
    return vulns


async def eks_has_endpoints_publicly_accessible(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="eks", function="list_clusters"
    )
    method = core.MethodsEnum.AWS_EKS_HAS_ENDPOINTS_PUBLICLY_ACCESSIBLE
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
        cluster_description = dict(cluster_desc["cluster"])
        vulnerable = (
            cluster_description["resourcesVpcConfig"]["endpointPublicAccess"]
            and not cluster_description["resourcesVpcConfig"][
                "endpointPrivateAccess"
            ]
        )
        if vulnerable:
            locations = [
                Location(
                    access_patterns=(
                        "/resourcesVpcConfig/endpointPrivateAccess",
                        "/resourcesVpcConfig/endpointPublicAccess",
                    ),
                    arn=(cluster_description["arn"]),
                    values=(
                        cluster_description["resourcesVpcConfig"][
                            "endpointPrivateAccess"
                        ],
                        cluster_description["resourcesVpcConfig"][
                            "endpointPublicAccess"
                        ],
                    ),
                    description=t(
                        "f165.dynamob_encrypted_with_aws_master_keys"
                    ),
                ),
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=cluster_description,
                ),
            )

    return vulns


async def rds_has_public_snapshots(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_snapshots"
    )
    snapshots = response.get("DBSnapshots", []) if response else []
    method = core.MethodsEnum.AWS_RDS_HAS_PUBLIC_SNAPSHOTS
    vulns: core.Vulnerabilities = ()
    for snapshot in snapshots:
        locations: list[Location] = []
        snapshot_attributes: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="rds",
            function="describe_db_snapshot_attributes",
            parameters={
                "DBSnapshotIdentifier": snapshot["DBSnapshotIdentifier"],
            },
        )
        attr_results = snapshot_attributes.get(
            "DBSnapshotAttributesResult", {}
        )
        for index, attr in enumerate(attr_results["DBSnapshotAttributes"]):
            if "all" in attr["AttributeValues"]:
                locations = [
                    *locations,
                    Location(
                        access_patterns=(f"/{index}/AttributeValues",),
                        arn=(
                            "arn:aws:rds:::DBSnapshotIdentifier:"
                            f"{attr_results['DBSnapshotIdentifier']}"
                        ),
                        values=(attr["AttributeValues"],),
                        description=t("f165.rds_has_public_snapshots"),
                    ),
                ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(method),
                aws_response=attr_results["DBSnapshotAttributes"],
            ),
        )

    return vulns


async def not_uses_iam_authentication(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )
    instances = response.get("DBInstances", []) if response else []
    method = core.MethodsEnum.AWS_RDS_NOT_USES_IAM_AUTHENTICATION
    vulns: core.Vulnerabilities = ()
    for instance in instances:
        locations: list[Location] = []
        if not instance["IAMDatabaseAuthenticationEnabled"]:
            locations = [
                *locations,
                Location(
                    access_patterns=("/IAMDatabaseAuthenticationEnabled",),
                    arn=(instance["DBInstanceArn"]),
                    values=(instance["IAMDatabaseAuthenticationEnabled"],),
                    description=t("f165.not_uses_iam_authentication"),
                ),
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=instance,
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


async def redshift_has_public_clusters(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    clusters = await redshift_get_paginated_items(credentials)
    method = core.MethodsEnum.AWS_REDSHIFT_HAS_PUBLIC_CLUSTERS
    vulns: core.Vulnerabilities = ()
    if clusters:
        for cluster in clusters:
            if cluster["PubliclyAccessible"]:
                locations = [
                    Location(
                        access_patterns=("/PubliclyAccessible",),
                        arn=(cluster["PubliclyAccessible"]),
                        values=(cluster["ClusterNamespaceArn"],),
                        description=t("f165.not_uses_iam_authentication"),
                    ),
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


async def redshift_not_requires_ssl(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_REDSHIFT_NOT_REQUIRES_SSL
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
                    param["ParameterName"] == "require_ssl"
                    and param["ParameterValue"] == "false"
                ):
                    locations = [
                        Location(
                            arn=(
                                "arn:aws:redshift::cluster:"
                                f"{cluster['ClusterIdentifier']}"
                            ),
                            description=t("f165.redshift_not_requires_ssl"),
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


async def elasticache_uses_default_port(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elasticache", function="describe_cache_clusters"
    )
    caches = response.get("CacheClusters", []) if response else []
    method = core.MethodsEnum.AWS_ELASTICACHE_USES_DEFAULT_PORT
    vulns: core.Vulnerabilities = ()
    for cluster in caches:
        locations: list[Location] = []
        if cluster.get("Engine") == "memcached" and cluster.get(
            "ConfigurationEndpoint"
        )["Port"] in (11211, 6379):
            locations = [
                *locations,
                Location(
                    access_patterns=(
                        "/Engine",
                        "/ConfigurationEndpoint/Port",
                    ),
                    arn=(cluster["ARN"]),
                    values=(
                        cluster["Engine"],
                        cluster["ConfigurationEndpoint"]["Port"],
                    ),
                    description=t("f165.not_uses_iam_authentication"),
                ),
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


async def elasticache_is_transit_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elasticache", function="describe_cache_clusters"
    )
    caches = response.get("CacheClusters", []) if response else []
    method = core.MethodsEnum.AWS_ELASTICACHE_TRANSIT_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    for cluster in caches:
        locations: list[Location] = []
        if cluster.get("Engine") == "redis" and not cluster.get(
            "TransitEncryptionEnabled", True
        ):
            locations = [
                *locations,
                Location(
                    access_patterns=(
                        "/Engine",
                        "/TransitEncryptionEnabled",
                    ),
                    arn=(cluster["ARN"]),
                    values=(
                        cluster["Engine"],
                        cluster["TransitEncryptionEnabled"],
                    ),
                    description=t(
                        "f165.elasticache_is_transit_encryption_disabled"
                    ),
                ),
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


async def elasticache_is_at_rest_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="elasticache", function="describe_cache_clusters"
    )
    caches = response.get("CacheClusters", []) if response else []
    method = core.MethodsEnum.AWS_ELASTICACHE_REST_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    for cluster in caches:
        locations: list[Location] = []
        if cluster.get("Engine") == "redis" and not cluster.get(
            "AtRestEncryptionEnabled", True
        ):
            locations = [
                *locations,
                Location(
                    access_patterns=(
                        "/Engine",
                        "/AtRestEncryptionEnabled",
                    ),
                    arn=(cluster["ARN"]),
                    values=(
                        cluster["Engine"],
                        cluster["AtRestEncryptionEnabled"],
                    ),
                    description=t(
                        "f165.elasticache_is_at_rest_encryption_disabled"
                    ),
                ),
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


async def sns_is_server_side_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sns", function="list_topics"
    )
    topics = response.get("Topics", []) if response else []
    method = core.MethodsEnum.AWS_SNS_HAS_SERVER_SIDE_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    if topics:
        for topic in topics:
            topic_arn = topic["TopicArn"]
            get_topic_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sns",
                function="get_topic_attributes",
                parameters={
                    "TopicArn": topic_arn,
                },
            )
            attrs = get_topic_attributes["Attributes"]
            if not attrs.get("KmsMasterKeyId", ""):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(topic_arn),
                        values=(),
                        description=t(
                            "f165.sns_is_server_side_encryption_disabled"
                        ),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=attrs,
                    ),
                )

    return vulns


async def sns_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sns", function="list_topics"
    )
    topics = response.get("Topics", []) if response else []
    method = core.MethodsEnum.AWS_SNS_USES_DEFAULT_KMS_KEY
    vulns: core.Vulnerabilities = ()
    if topics:
        for topic in topics:
            topic_arn = topic["TopicArn"]
            get_topic_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sns",
                function="get_topic_attributes",
                parameters={
                    "TopicArn": topic_arn,
                },
            )
            attrs = get_topic_attributes["Attributes"]
            if attrs.get("KmsMasterKeyId", "") == "alias/aws/sns":
                locations = [
                    Location(
                        access_patterns=("/KmsMasterKeyId",),
                        arn=(topic_arn),
                        values=(attrs["KmsMasterKeyId"],),
                        description=t("f165.sns_uses_default_kms_key"),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=attrs,
                    ),
                )

    return vulns


async def sqs_is_encryption_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sqs", function="list_queues"
    )
    queues = response.get("QueueUrls", []) if response else []
    method = core.MethodsEnum.AWS_SQS_HAS_ENCRYPTION_DISABLED
    vulns: core.Vulnerabilities = ()
    if queues:
        for queue_url in queues:
            get_queue_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sqs",
                function="get_queue_attributes",
                parameters={
                    "QueueUrl": queue_url,
                    "AttributeNames": ["QueueArn", "KmsMasterKeyId"],
                },
            )
            attr = get_queue_attributes.get("Attributes", {})
            if not attr.get("KmsMasterKeyId", ""):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(attr["QueueArn"]),
                        values=(),
                        description=t("f165.sqs_is_encryption_disabled"),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=attr,
                    ),
                )

    return vulns


async def sqs_uses_default_kms_key(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sqs", function="list_queues"
    )
    queues = response.get("QueueUrls", []) if response else []
    method = core.MethodsEnum.AWS_SQS_USES_DEFAULT_KMS_KEY
    vulns: core.Vulnerabilities = ()
    if queues:
        for queue_url in queues:
            get_queue_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sqs",
                function="get_queue_attributes",
                parameters={
                    "QueueUrl": queue_url,
                    "AttributeNames": ["QueueArn", "All"],
                },
            )
            attr = get_queue_attributes.get("Attributes", {})
            if attr.get("KmsMasterKeyId", "") == "alias/aws/sqs":
                locations = [
                    Location(
                        access_patterns=("/KmsMasterKeyId",),
                        arn=(attr["QueueArn"]),
                        values=(attr["KmsMasterKeyId"],),
                        description=t("f165.sqs_uses_default_kms_key"),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=attr,
                    ),
                )

    return vulns


async def sqs_is_public(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sqs", function="list_queues"
    )
    queues = response.get("QueueUrls", []) if response else []
    method = core.MethodsEnum.AWS_SQS_IS_PUBLIC
    vulns: core.Vulnerabilities = ()
    if queues:
        for queue_url in queues:
            get_queue_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sqs",
                function="get_queue_attributes",
                parameters={
                    "QueueUrl": queue_url,
                    "AttributeNames": ["QueueArn", "All"],
                },
            )
            attrs = get_queue_attributes.get("Attributes", {})
            policy = json.loads(attrs.get("Policy", "{}"))

            for statement in policy.get("Statement", []):
                if statement.get("Principal", "") == "*" and not statement.get(
                    "Condition", {}
                ):
                    locations = [
                        Location(
                            access_patterns=("/Principal",),
                            arn=(attrs["QueueArn"]),
                            values=(statement["Principal"],),
                            description=t("f165.sqs_is_public"),
                        ),
                    ]
                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=statement,
                        ),
                    )

    return vulns


async def sns_can_anyone_publish(  # NOSONAR
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sns", function="list_topics"
    )
    topics = response.get("Topics", []) if response else []
    method = core.MethodsEnum.AWS_SNS_CAN_ANYONE_PUBLISH
    vulns: core.Vulnerabilities = ()
    if topics:
        for topic in topics:
            topic_arn = topic["TopicArn"]
            get_topic_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sns",
                function="get_topic_attributes",
                parameters={
                    "TopicArn": topic_arn,
                },
            )
            attrs = get_topic_attributes["Attributes"]
            if policy := json.loads(attrs.get("Policy", "{}")):
                for statement in policy.get("Statement", []):
                    condition = (
                        statement.get("Effect", "") == "Allow"
                        and statement.get("Principal", {}).get("AWS", "")
                        == "*"
                        and (
                            {"SNS:Publish"}.issubset(
                                statement.get("Action", {})
                            )
                            or statement.get("Action", "") == "SNS:Publish"
                        )
                        and statement.get("Resource", "") == topic_arn
                    )
                    if condition and not statement.get("Condition", {}):
                        locations = [
                            Location(
                                access_patterns=("/Principal/AWS", "/Action"),
                                arn=(topic_arn),
                                values=(
                                    statement["Principal"]["AWS"],
                                    statement["Action"],
                                ),
                                description=t("f165.sns_can_anyone_publish"),
                            ),
                        ]
                        vulns = (
                            *vulns,
                            *build_vulnerabilities(
                                locations=locations,
                                method=(method),
                                aws_response=statement,
                            ),
                        )

    return vulns


async def sns_can_anyone_subscribe(  # NOSONAR
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="sns", function="list_topics"
    )
    topics = response.get("Topics", []) if response else []
    method = core.MethodsEnum.AWS_SNS_CAN_ANYONE_SUBSCRIBE
    vulns: core.Vulnerabilities = ()
    if topics:
        for topic in topics:
            topic_arn = topic["TopicArn"]
            get_topic_attributes: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="sns",
                function="get_topic_attributes",
                parameters={
                    "TopicArn": topic_arn,
                },
            )
            attrs = get_topic_attributes["Attributes"]
            if policy := json.loads(attrs.get("Policy", "{}")):
                for statement in policy.get("Statement", []):
                    condition = (
                        statement.get("Effect", "") == "Allow"
                        and statement.get("Principal", {}).get("AWS", "")
                        == "*"
                        and {"SNS:Subscribe", "SNS:Receive"}.issubset(
                            statement.get("Action", {})
                        )
                        and statement.get("Resource", "") == topic_arn
                    )
                    if condition and not statement.get("Condition", {}):
                        locations = [
                            Location(
                                access_patterns=("/Principal/AWS", "/Action"),
                                arn=(topic_arn),
                                values=(
                                    statement["Principal"]["AWS"],
                                    statement["Action"],
                                ),
                                description=t("f165.sns_can_anyone_subscribe"),
                            ),
                        ]
                        vulns = (
                            *vulns,
                            *build_vulnerabilities(
                                locations=locations,
                                method=(method),
                                aws_response=statement,
                            ),
                        )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    users_with_multiple_access_keys,
    root_has_access_keys,
    has_not_support_role,
    has_root_active_signing_certificates,
    dynamob_encrypted_with_aws_master_keys,
    eks_has_endpoints_publicly_accessible,
    rds_has_public_snapshots,
    not_uses_iam_authentication,
    redshift_has_public_clusters,
    redshift_not_requires_ssl,
    elasticache_uses_default_port,
    elasticache_is_transit_encryption_disabled,
    elasticache_is_at_rest_encryption_disabled,
    sns_is_server_side_encryption_disabled,
    sns_uses_default_kms_key,
    sqs_is_encryption_disabled,
    sqs_uses_default_kms_key,
    sqs_is_public,
    sns_can_anyone_publish,
    sns_can_anyone_subscribe,
)
