from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::123456789012:elbv2/myload",
                "LoadBalancerName": "myload",
            },
        ],
        "Listeners": [
            {
                "ListenerArn": "arn:aws:iam::123456789012:listener/lst",
                "LoadBalancerArn": "arn:aws:iam::123456789012:elbv2/myload",
                "Port": 1,
                "Protocol": "HTTP",
            }
        ],
        "DistributionList": {
            "Items": [
                {
                    "Id": "dlt-018de572ae43404d8",
                    "ARN": "arn:aws:iam::123456789012:distributionlist/mlt",
                }
            ],
        },
        "Distribution": {
            "Id": "string",
            "ARN": "string",
            "DistributionConfig": {
                "DefaultCacheBehavior": {
                    "TargetOriginId": "string",
                    "ViewerProtocolPolicy": "allow-all",
                },
                "CacheBehaviors": {
                    "Quantity": 1,
                    "Items": [
                        {
                            "ViewerProtocolPolicy": "allow-all",
                        }
                    ],
                },
            },
        },
    }
