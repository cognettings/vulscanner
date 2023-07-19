from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection | bool]:
    return {
        "Keys": [
            {"KeyId": "123", "KeyArn": "arn:aws:iam::123456789012:key/myKey"},
        ],
        "KeyRotationEnabled": False,
        "SecretList": [
            {
                "Name": "fluidsecret",
            },
        ],
        "RotationEnabled": False,
        "ARN": "arn:aws:iam::123456789012:secret/mysecret",
    }
