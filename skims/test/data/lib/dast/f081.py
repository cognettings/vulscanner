from collections.abc import (
    Collection,
)


def mock_data() -> dict[str, Collection]:
    content = (
        b"arn,mfa_active,password_enabled\n"
        b"myUser1,false,true\n"
        b"myUser2,true,false\n"
        b"myUser3,true,true"
    )
    return {
        "Content": content,
        "SummaryMap": {
            "AccountMFAEnabled": 0,
        },
        "Users": [
            {
                "UserName": "fluidattacks",
                "Arn": "arn:aws:iam::123456789012:user/fluidAttacks",
            },
        ],
        "MFADevices": [],
        "UserPools": [
            {
                "Id": "fluid_userpool123",
                "Name": "fluid_up",
                "Status": "Enabled",
            },
        ],
        "MfaConfiguration": "OFF",
    }
