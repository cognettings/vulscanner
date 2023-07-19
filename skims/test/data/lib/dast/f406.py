from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "FileSystems": [
            {
                "FileSystemArn": "arn:aws:iam::123456789012:fs/fluidunsafe",
                "LifeCycleState": "available",
                "PerformanceMode": "generalPurpose",
                "Encrypted": False,
            },
            {
                "FileSystemArn": "arn:aws:iam::123456789012:fs/fluidsafe",
                "LifeCycleState": "available",
                "PerformanceMode": "generalPurpose",
                "Encrypted": True,
            },
        ],
    }
