from context import (
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)
from typing import (
    Literal,
)

JWT_ALGORITHM = "RS512"
JWT_COOKIE_NAME = "integrates_session"
JWT_COOKIE_SAMESITE: Literal["lax"] = "lax"
JWT_SECRET = FI_JWT_SECRET
JWT_SECRET_API = FI_JWT_SECRET_API
