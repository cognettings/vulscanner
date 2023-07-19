from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb12",
                "DBInstanceArn": "arn:aws:iam::123456789012:db/mydb",
                "VpcSecurityGroupId": "sg-0f1774631f8rgf250",
                "VpcSecurityGroups": [
                    {
                        "VpcSecurityGroupId": "sg-0f1774631f8rgf250",
                        "Status": "active",
                    }
                ],
            }
        ],
        "DBClusters": [
            {
                "DBClusterArn": "arn:aws:iam::123456789012:dbc/mydbcluster",
            }
        ],
        "SecurityGroups": [
            {
                "Description": "fluidsecgroup",
                "GroupName": "fluidgroup",
                "GroupId": "sg-0f1774631f8rgf250",
                "IpPermissions": [
                    {
                        "FromPort": 443,
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "ToPort": 443,
                    },
                ],
            }
        ],
    }
