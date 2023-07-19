from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    content = (
        b"arn,access_key_1_active,access_key_2_active,cert_1_active\n"
        b"myUser,true,true,true"
    )

    policy = """
        {"Statement": [
            {"Principal":"*"},
            {"Principal":"*", "Condition": "Anything"},
            {"Effect":"Allow", "Principal":{"AWS":"*"},
            "Action":"SNS:Publish","Resource": "arn:aws:fluidTopic/1234"},
            {"Effect":"Allow", "Principal":{"AWS":"*"},
            "Action":["SNS:Subscribe","SNS:Receive"],
            "Resource": "arn:aws:fluidTopic/1234"}
        ],
        "Version": "1.0"}
    """
    return {
        "Users": [
            {
                "UserName": "myUser",
                "UserId": "1234",
                "Arn": "arn:aws:iam::123456789012:user/myUser",
            },
        ],
        "AccessKeyMetadata": [
            {
                "UserName": "myUser",
                "AccessKeyId": "108745",
                "Status": "Active",
            },
            {
                "UserName": "myUser",
                "AccessKeyId": "37856",
                "Status": "Active",
            },
        ],
        "State": "STARTED",
        "Description": "string",
        "Content": content,
        "ReportFormat": "text/csv",
        "PolicyGroups": [],
        "PolicyUsers": [],
        "PolicyRoles": [],
        "TableNames": [
            "fluidTable",
        ],
        "Table": {
            "TableName": "fluidTable",
            "TableArn": "arn:aws:iam::aws:table/fluidTable",
            "SSEDescription": {
                "Status": "ENABLED",
                "SSEType": "AES256",
                "KMSMasterKeyArn": "arn:aws:iam::aws:key/fuildKey",
            },
        },
        "clusters": [
            "fluidcluster",
        ],
        "cluster": {
            "name": "fluidcluster",
            "arn": "arn:aws:iam::123456789012:cluster/fluidcl1",
            "resourcesVpcConfig": {
                "securityGroupIds": [
                    "fluidsecuritygroup1",
                ],
                "endpointPublicAccess": True,
                "endpointPrivateAccess": False,
            },
        },
        "DBInstances": [
            {
                "DBInstanceArn": "arn:aws:iam::123456789012:dbi/db1",
                "IAMDatabaseAuthenticationEnabled": False,
            }
        ],
        "DBSnapshots": [
            {
                "DBSnapshotIdentifier": "fluidsnapshot",
            }
        ],
        "DBSnapshotAttributesResult": {
            "DBSnapshotIdentifier": "fluidsnapshot",
            "DBSnapshotAttributes": [
                {
                    "AttributeName": "permissions",
                    "AttributeValues": [
                        "all",
                    ],
                },
            ],
        },
        "Clusters": [
            {
                "Name": "fluidCluster",
                "ClusterIdentifier": "fluidCluster123",
                "ClusterNamespaceArn": "arn:aws:iam::123456789012:Cluster/FC1",
                "PubliclyAccessible": True,
                "ClusterParameterGroups": [
                    {
                        "ParameterGroupName": "fluidParamGroup1",
                    },
                ],
            },
            {
                "Name": "fluidCluster2",
                "ClusterIdentifier": "fluidCluster456",
                "ClusterNamespaceArn": "arn:aws:iam::123456789012:Cluster/FC2",
                "PubliclyAccessible": False,
            },
        ],
        "Parameters": [
            {
                "ParameterName": "require_ssl",
                "ParameterValue": "false",
            },
        ],
        "CacheClusters": [
            {
                "CacheClusterId": "fluidCacheCluster1",
                "ARN": "arn:aws:fluidCacheCluster/1234",
                "Engine": "memcached",
                "ConfigurationEndpoint": {
                    "Address": "-1",
                    "Port": 11211,
                },
            },
            {
                "CacheClusterId": "fluidCacheCluster2",
                "ARN": "arn:aws:fluidCacheCluster/4567",
                "Engine": "redis",
                "AtRestEncryptionEnabled": False,
                "TransitEncryptionEnabled": False,
            },
            {
                "CacheClusterId": "fluidCacheCluster3",
                "ARN": "arn:aws:fluidCacheCluster/safe123",
                "Engine": "redis",
                "AtRestEncryptionEnabled": True,
                "TransitEncryptionEnabled": True,
            },
        ],
        "Topics": [
            {"TopicArn": "arn:aws:fluidTopic/1234"},
        ],
        "QueueUrls": [
            "https://localhost:8000",
        ],
        "Attributes": {
            "TopicArn": "arn:aws:fluidTopic/1234",
            "QueueArn": "arn:aws:fluidQueue/1234",
            "Policy": policy,
        },
    }
