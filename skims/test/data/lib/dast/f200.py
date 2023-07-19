from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection | bool]:
    return {
        "Vpcs": [
            {
                "State": "pending",
                "VpcId": "fluidvpc1",
                "OwnerId": "fluidattacks",
                "InstanceTenancy": "default",
            },
        ],
        "Clusters": [
            {
                "ClusterIdentifier": "fluidRedShiftCluster",
                "KmsKeyId": "fluidkey/8888",
                "ClusterParameterGroups": [
                    {
                        "ParameterGroupName": "fluidParamGroup1",
                    },
                ],
            },
        ],
        "LoggingEnabled": False,
        "Parameters": [
            {
                "ParameterName": "enable_user_activity_logging",
                "ParameterValue": "false",
            },
            {
                "ParameterName": "enable_user_activity_logging",
                "ParameterValue": "true",
            },
        ],
    }
