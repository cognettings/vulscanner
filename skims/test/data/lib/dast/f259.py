from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "TableNames": [
            "fluidbackup",
        ],
        "ContinuousBackupsDescription": {
            "ContinuousBackupsStatus": "DISABLED",
            "PointInTimeRecoveryDescription": {
                "PointInTimeRecoveryStatus": "DISABLED",
            },
        },
        "Table": {
            "TableName": "fluidbackup",
            "TableArn": "arn:aws:iam::123456789012:db/fluiddb",
            "DeletionProtection": False,
        },
    }
