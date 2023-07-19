from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/myldbal",
                "DNSName": "string",
            }
        ],
        "Attributes": [
            {
                "Key": "deletion_protection.enabled",
                "Value": "false",
            },
        ],
    }
