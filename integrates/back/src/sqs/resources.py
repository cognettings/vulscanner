import aioboto3
from aiobotocore.config import (
    AioConfig,
)
from context import (
    FI_AWS_REGION_NAME,
)
from contextlib import (
    AsyncExitStack,
)
from typing import (
    Any,
)

RESOURCE_OPTIONS = {
    "config": AioConfig(
        # The time in seconds till a timeout exception is thrown when
        # attempting to make a connection. [60]
        connect_timeout=60,
        # Maximum amount of simultaneously opened connections. [10]
        # https://docs.aiohttp.org/en/stable/client_advanced.html#limiting-connection-pool-size
        max_pool_connections=2000,
        # The time in seconds till a timeout exception is thrown when
        # attempting to read from a connection. [60]
        read_timeout=60,
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html
        retries={"max_attempts": 10, "mode": "standard"},
        # Signature version for signing URLs
        # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/sqs.html#generating-presigned-urls
    ),
    "region_name": FI_AWS_REGION_NAME,
    "service_name": "sqs",
    "use_ssl": True,
    "verify": True,
}
SESSION = aioboto3.Session()
CONTEXT_STACK = None
CLIENT = None


async def sqs_startup() -> None:
    # pylint: disable=global-statement
    global CONTEXT_STACK, CLIENT

    CONTEXT_STACK = AsyncExitStack()
    CLIENT = await CONTEXT_STACK.enter_async_context(
        SESSION.client(**RESOURCE_OPTIONS)
    )


async def sqs_shutdown() -> None:
    if CONTEXT_STACK:
        await CONTEXT_STACK.aclose()


async def get_sqs_resource() -> Any:
    if CLIENT is None:
        await sqs_startup()

    return CLIENT
