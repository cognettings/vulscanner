from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "123",
                    }
                ],
                "OwnerId": "fluidattacks",
            }
        ],
        "DisableApiTermination": {
            "Value": False,
        },
    }
