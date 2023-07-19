# pylint: disable=invalid-name
"""
Populates the stakeholder enrolled attribute with data previosly stored
in the enrollment facet

Execution Time:    2023-06-20 at 01:21:07 UTC
Finalization Time: 2023-06-20 at 01:21:55 UTC
"""

from aioextensions import (
    run,
)
from custom_exceptions import (
    InvalidExpirationTime,
)
from custom_utils import (
    datetime as datetime_utils,
)
from datetime import (
    datetime,
)
import logging
import logging.config
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def main() -> None:
    # Current token. This is an example
    token = "eyJhbGciOTR1kyRE9JS21GNUcGNIeSDk0yJ9.QbqIfdGIVvTLxNZdk8zBEbxvEr5A"
    token_claims = sessions_domain.decode_token(token)
    LOGGER_CONSOLE.info(
        "Token claims",
        extra={"extra": {"Claims": token_claims}},
    )

    # Generate new token
    email = token_claims["user_email"]
    expiration_time = int(
        datetime_utils.get_now_plus_delta(days=180).timestamp()
    )

    token_data = sessions_utils.calculate_hash_token()

    if sessions_utils.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = sessions_domain.encode_token(
            expiration_time=expiration_time,
            payload={
                "user_email": email,
                "jti": token_data["jti"],
                "iat": iat,
            },
            subject="api_token",
            api=True,
        )
        access_token = dict(
            iat=iat,
            jti=token_data["jti_hashed"],
            salt=token_data["salt"],
        )
        print(f"\n Token= {session_jwt} \n Add to local data {access_token}")
    else:
        raise InvalidExpirationTime()


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
