"""Fluid Forces Integrates api client."""

from aiogqlc import (
    GraphQLClient,
)
import aiohttp
from aiohttp.client_exceptions import (
    ClientResponseError,
)
import asyncio
from collections.abc import (
    AsyncIterator,
    Mapping,
)
import contextlib
from forces.apis.integrates import (
    get_api_token,
)
from forces.utils.env import (
    ENDPOINT,
    guess_environment,
)
from forces.utils.logs import (
    blocking_log,
    log_to_remote,
)
from typing import (
    Any,
    TypeVar,
)

# Context
TVar = TypeVar("TVar")  # pylint: disable=invalid-name


class ApiError(Exception):
    def __init__(self, *errors: Mapping[str, Any]) -> None:
        self.messages: list[str] = []
        self.skip_bugsnag: bool = False
        for error in errors:
            if message := error.get("message"):
                self.messages.append(message)
                blocking_log("error", message)
        super().__init__(*errors)


@contextlib.asynccontextmanager
async def session(
    api_token: str = "",
    **kwargs: str,
) -> AsyncIterator[GraphQLClient]:
    """Returns an Async GraphQL Client."""
    api_token = api_token or get_api_token()
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            # A local integrates uses self-signed certificates,
            # but other than that the certificate should be valid,
            # particularly in production.
            verify_ssl=(guess_environment() == "production"),
        ),
        headers={
            "authorization": f"Bearer {api_token}",
            **kwargs,
        },
    ) as client_session:
        yield GraphQLClient(ENDPOINT, session=client_session)


async def execute(
    query: str,
    operation_name: str,
    variables: dict[str, Any] | None = None,
    default: object | None = None,
    **kwargs: Any,
) -> TVar:
    async with session(**kwargs) as client:
        result: dict
        response: aiohttp.ClientResponse

        try:
            response = await client.execute(
                query,
                variables=variables,
                operation=operation_name,
            )

            if response.status == 429 and (
                seconds := response.headers.get("retry-after")
            ):
                blocking_log(
                    "warning",
                    (
                        "API rate limit reached. Retrying in "
                        f"{int(seconds) + 1} seconds.."
                    ),
                )
                await log_to_remote(
                    ApiError(
                        *[
                            dict(
                                status=getattr(response, "status", "unknown"),
                                reason=getattr(response, "reason", "unknown"),
                                ok=getattr(response, "ok", False),
                            )
                        ]
                    ),
                )
                await asyncio.sleep(int(seconds) + 1)
            result = await response.json()
        except ClientResponseError as client_error:
            if response.status == 429 and (
                seconds := response.headers.get("retry-after")
            ):
                blocking_log(
                    "warning",
                    (
                        "API rate limit reached. Retrying in "
                        f"{int(seconds) + 1} seconds.."
                    ),
                )
                await log_to_remote(
                    ApiError(
                        *[
                            dict(
                                status=getattr(response, "status", "unknown"),
                                reason=getattr(response, "reason", "unknown"),
                                ok=getattr(response, "ok", False),
                            )
                        ]
                    ),
                )
                await asyncio.sleep(int(seconds) + 1)
            else:
                api_error = ApiError(
                    *[
                        dict(
                            status=getattr(response, "status", "unknown"),
                            reason=getattr(response, "reason", "unknown"),
                            message=getattr(response, "content", "unknown"),
                            ok=getattr(response, "ok", False),
                        )
                    ]
                )
                await log_to_remote(api_error)
                # Avoid double reports to bugsnag
                api_error.skip_bugsnag = True
                raise api_error from client_error
        if "errors" in result.keys():
            raise ApiError(*result["errors"])

        result = result.get("data", {})
        return result or default  # type: ignore
