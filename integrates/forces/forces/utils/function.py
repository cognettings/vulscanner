from asyncio import (
    sleep,
)
from collections.abc import (
    Callable,
)
from forces.utils.env import (
    guess_environment,
)
from forces.utils.logs import (
    log,
    log_to_remote,
)
import functools
from more_itertools import (
    mark_ends,
)
import re
from typing import (
    Any,
    cast,
    TypeVar,
)

# Constants
RAISE = object()
# pylint: disable=invalid-name
TFun = TypeVar("TFun", bound=Callable[..., Any])
RATE_LIMIT_ENABLED: bool = guess_environment() == "production"


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying."""


def shield(  # NOSONAR
    *,
    on_error_return: object = RAISE,
    on_exceptions: tuple[type[BaseException], ...] = (
        BaseException,
        RetryAndFinallyReturn,
    ),
    retries: int = 4,
    sleep_between_retries: int = 0,
) -> Callable[[TFun], TFun]:
    if retries < 1:  # pragma: no cover
        raise ValueError("retries must be >= 1")

    def decorator(function: TFun) -> TFun:
        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = f"{function.__module__}.{function.__name__}"

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return await function(*args, **kwargs)
                except on_exceptions as exc:  # pragma: no cover
                    msg: str = "Function: %s, %s: %s"
                    exc_msg: str = str(exc)
                    exc_type: str = type(exc).__name__
                    await log("warning", msg, function_id, exc_type, exc_msg)
                    await log_to_remote(
                        exc, function_id=function_id, retry=str(number)
                    )

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            # This attribute must be set here to avoid sending
                            # double reports to bugsnag
                            exc.skip_bugsnag = (  # type: ignore[attr-defined]
                                True
                            )
                            raise exc
                        return on_error_return

                    await log("info", "retry #%s: %s", number, function_id)
                    await sleep(sleep_between_retries)

        return cast(TFun, wrapper)

    return decorator


def remove_color_codes(text: str) -> str:
    color_code_pattern = r"\x1b\[[0-9;]+m"
    return re.sub(color_code_pattern, "", text)
