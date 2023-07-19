# pylint: disable-all
# type: ignore

import aiohttp
import json
import os
from typing import (
    Any,
)


async def danger_func() -> Any:
    url = "test.com"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                headers={
                    "accept": "text/html",
                    "authorization": f"Basic {os.environ['API_TOKEN']}",
                },
                url=url,
            ) as response:
                if response.status == 200:
                    data = await response.text()
                    return [
                        json.loads(item) for item in data.split("\n") if item
                    ]
                return []
    except aiohttp.ClientError as exception:
        return print(exception)
