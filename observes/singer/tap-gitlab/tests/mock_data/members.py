from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
)
from tap_gitlab.api.members import (
    Member,
    User,
    UserId,
)

mock_user_empty = (
    UserId(5234),
    User(
        "avatar",
        Maybe.empty(),
        "Aang",
        "active",
        datetime(1700, 1, 1),
    ),
)
mock_user_full = (
    UserId(5234),
    User(
        "avatar",
        Maybe.from_value("aang@airbender.com"),
        "Aang",
        "active",
        datetime(1700, 1, 1),
    ),
)
mock_member_empty = Member(mock_user_empty, "active")
mock_member_full = Member(mock_user_full, "active")
