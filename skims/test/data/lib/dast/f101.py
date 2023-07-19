from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Buckets": [
            {
                "Name": "fluidbucket",
            },
        ],
        "ObjectLockConfiguration": {
            "ObjectLockEnabled": "Disabled",
            "Rule": {
                "DefaultRetention": {
                    "Mode": "GOVERNANCE",
                    "Days": 1,
                    "Years": 1,
                }
            },
        },
    }
