# pylint: disable-all
# type: ignore

import aiohttp
import json
from typing import (
    Any,
)


async def danger_func() -> Any:
    url = "test.com"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                headers={
                    "accept": "*/*",
                    "authorization": "Basic YWUzYjQwODAwODA3Z3E5ZjdjTVkzOTFhOWM5ZWZiMjQ6",  # noqa: E501 pylint: disable=line-too-long
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
