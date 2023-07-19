from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
            }
        ],
        "Listeners": [
            {
                "ListenerArn": "arn:aws:iam::123456789012:list/unsafelistener",
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
                "Port": 123,
                "SslPolicy": "ELBSecurityPolicy-FS-1-2-Res-2019-08",
            },
            {
                "ListenerArn": "arn:aws:iam::123456789012:list/safelistener",
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
                "Port": 123,
                "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
            },
        ],
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
                "endpointPrivateAccess": True,
            },
        },
        "SecurityGroups": [
            {
                "Description": "fluidsecgroup1",
                "GroupName": "fluidsecuritygroup1",
                "OwnerId": "fluid",
                "GroupId": "secgroup1",
                "IpPermissions": [
                    {
                        "FromPort": 88,
                        "ToPort": 8808,
                    },
                ],
            },
        ],
    }
