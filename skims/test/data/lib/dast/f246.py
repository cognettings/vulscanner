from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "DBInstances": [
            {
                "DBInstanceArn": "arn:aws:iam::123456789012:db/unsafedb",
                "StorageEncrypted": False,
            },
            {
                "DBInstanceArn": "arn:aws:iam::123456789012:db/safedb",
                "StorageEncrypted": True,
            },
        ],
    }
