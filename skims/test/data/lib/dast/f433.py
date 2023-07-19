from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Clusters": [
            {
                "ClusterIdentifier": "fluidRedShiftCluster",
                "KmsKeyId": "fluidkey/8888",
                "Encrypted": False,
            },
            {
                "ClusterIdentifier": "fluidRedShiftCluster",
                "KmsKeyId": "fluidkey/1111",
                "Encrypted": True,
            },
        ],
    }
