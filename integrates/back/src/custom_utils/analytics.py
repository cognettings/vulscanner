from aioextensions import (
    in_thread,
)
import aiohttp
import base64
from context import (
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from datetime import (
    date,
)
from decimal import (
    Decimal,
    InvalidOperation,
)
import json
import logging
import logging.config
from mixpanel import (
    Consumer,
    Mixpanel,
)
from settings import (
    LOGGING,
    MIXPANEL_API_SECRET,
    MIXPANEL_API_TOKEN,
)
from urllib.parse import (
    quote,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
MIXPANEL_EVENT_EXPORT_URL = "https://data.mixpanel.com/api/2.0/export"


def is_decimal(num: str) -> bool:
    try:
        Decimal(num)
        return True
    except InvalidOperation:
        with suppress(InvalidOperation):
            Decimal(num[:-1])
            return True
        return False


async def mixpanel_track(email: str, event: str, **extra: str) -> None:
    if FI_ENVIRONMENT == "production":
        mp_instance = Mixpanel(MIXPANEL_API_TOKEN, Consumer(request_timeout=5))

        await in_thread(
            mp_instance.track,
            email,
            event,
            {"integrates_user_email": email, **extra},
        )


async def get_mixpanel_events(
    event: list[str],
    from_date: date = date.today(),
    to_date: date = date.today(),
) -> list[dict[str, dict[str, str | int] | str]]:
    url = (
        f"{MIXPANEL_EVENT_EXPORT_URL}?"
        + f"from_date={from_date.isoformat()}&"
        + f"to_date={to_date.isoformat()}&"
        + f"event={quote(json.dumps(event))}"
    )
    encoding = "UTF-8"
    b64_payload = base64.b64encode(
        MIXPANEL_API_SECRET.encode(encoding)
    ).decode(encoding)
    error_msg = "Couldn't fetch mixpanel events. "

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                headers={
                    "accept": "text/plain",
                    "authorization": f"Basic {b64_payload}",
                },
                url=url,
            ) as response:
                if response.status == 200:
                    data = await response.text()
                    return [
                        json.loads(item) for item in data.split("\n") if item
                    ]
                LOGGER.error(
                    response.status,
                    extra=dict(extra=dict(error=error_msg, response=response)),
                )
                return []
    except aiohttp.ClientError as exception:
        LOGGER.error("%s %s", error_msg, exception)
        return []
