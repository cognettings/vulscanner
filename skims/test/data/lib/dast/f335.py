from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Buckets": [
            {
                "Name": "unsafeBucket",
            },
        ],
        "Status": "Suspended",
        "MFADelete": "Disabled",
    }
