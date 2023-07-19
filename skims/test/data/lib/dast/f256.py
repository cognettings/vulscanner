from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb123",
                "DBInstanceArn": "arn:aws:iam::123456789012:db/mydb",
                "DeletionProtection": False,
                "BackupRetentionPeriod": 0,
            }
        ],
    }
