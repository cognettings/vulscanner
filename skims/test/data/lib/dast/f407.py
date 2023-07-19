from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    return {
        "Volumes": [
            {
                "Encrypted": False,
                "Size": 123,
                "State": "in-use",
                "VolumeId": "fluidvolumeunsafe",
                "VolumeType": "standard",
                "FastRestored": False,
                "MultiAttachEnabled": False,
            },
            {
                "Size": 256,
                "State": "in-use",
                "VolumeId": "fluidvolumeunsafe2",
                "VolumeType": "standard",
                "FastRestored": False,
                "MultiAttachEnabled": False,
            },
            {
                "Encrypted": True,
                "Size": 123,
                "State": "in-use",
                "VolumeId": "fluidvolumesafe",
                "VolumeType": "standard",
                "FastRestored": False,
                "MultiAttachEnabled": False,
            },
        ],
    }
