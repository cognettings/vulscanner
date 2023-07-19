from asyncio import (
    sleep,
)
from collections.abc import (
    Callable,
    Collection,
)
import functools
import inspect
from more_itertools import (
    mark_ends,
)
import sys
from time import (
    sleep as sleep_blocking,
)
import traceback
from typing import (
    Any,
    cast,
    TypeVar,
)
from utils.env import (
    guess_environment,
)
from utils.logs import (
    log,
    log_blocking,
    log_to_remote,
    log_to_remote_blocking,
)

# Constants
RAISE = object()
RATE_LIMIT_ENABLED: bool = guess_environment() == "production"
Tfun = TypeVar("Tfun", bound=Callable[..., Any])


class RetryAndFinallyReturn(Exception):
    """Mark an operation as failed but whose value can be the result.

    Raising this exception will make the `shield` decorator retry the task.
    Aditionally, in the last round the exception argument will be returned.
    """


class StopRetrying(Exception):
    """Raise this exception will make the `shield` decorator stop retrying."""


class SkimsCanNotOperate(Exception):
    """Skims cannot operate at this time."""


def get_id(function: Tfun) -> str:
    if isinstance(function, functools.partial):
        function_attributes = function.func
    else:
        function_attributes = function

    return f"{function_attributes.__module__}.{function_attributes.__name__}"


def get_signature(function: Tfun) -> inspect.Signature:
    signature: inspect.Signature = inspect.signature(
        function,
        follow_wrapped=True,
    )

    return signature


def get_dict_values(dict_val: dict, *keys: str) -> Collection | None:
    cur_dict = dict_val
    for key in keys:
        if key in cur_dict.keys():
            cur_dict = cur_dict[key]
        else:
            return None
    return cur_dict


def shield(  # NOSONAR
    *,
    on_error_return: object = RAISE,
    on_exceptions: tuple[type[BaseException], ...] = (
        BaseException,
        RetryAndFinallyReturn,
    ),
    retries: int = 1,
    sleep_between_retries: int = 0,
) -> Callable[[Tfun], Tfun]:
    if retries < 1:
        raise ValueError("retries must be >= 1")

    def decorator(function: Tfun) -> Tfun:
        @functools.wraps(function)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_id = get_id(function)

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return await function(*args, **kwargs)
                except on_exceptions as exc:
                    exc_type, exc_value, exc_taceback = sys.exc_info()
                    await log_to_remote(
                        msg=(exc_type, exc_value, exc_taceback),
                        severity="error",
                        function_id=function_id,
                        retry=number,  # type: ignore
                    )

                    msg: str = "Function: %s, %s: %s\n%s"
                    await log(
                        "warning",
                        msg,
                        function_id,
                        type(exc_type).__name__,
                        exc_value,
                        traceback.format_exc(),
                    )

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    await log("info", "retry #%s: %s", number, function_id)
                    await sleep(sleep_between_retries)

        return cast(Tfun, wrapper)

    return decorator


def shield_blocking(  # NOSONAR
    *,
    on_error_return: object = RAISE,
    on_exceptions: tuple[type[BaseException], ...] = (
        BaseException,
        RetryAndFinallyReturn,
    ),
    retries: int = 1,
    sleep_between_retries: int = 0,
) -> Callable[[Tfun], Tfun]:
    if retries < 1:
        raise ValueError("retries must be >= 1")

    def decorator(function: Tfun) -> Tfun:
        @functools.wraps(function)
        def wrapper(  # pylint: disable=inconsistent-return-statements
            *args: Any, **kwargs: Any
        ) -> Any:
            function_id = get_id(function)

            for _, is_last, number in mark_ends(range(retries)):
                try:
                    return function(*args, **kwargs)
                except on_exceptions as exc:
                    exc_type, exc_value, exc_taceback = sys.exc_info()
                    log_to_remote_blocking(
                        msg=(exc_type, exc_value, exc_taceback),
                        severity="error",
                        function_id=function_id,
                        retry=number,  # type: ignore
                    )

                    msg: str = "Function: %s, %s: %s\n%s"
                    log_blocking(
                        "warning",
                        msg,
                        function_id,
                        type(exc_type).__name__,
                        exc_value,
                        traceback.format_exc(),
                    )

                    if is_last or isinstance(exc, StopRetrying):
                        if isinstance(exc, RetryAndFinallyReturn):
                            return exc.args[0]
                        if on_error_return is RAISE:
                            raise exc
                        return on_error_return

                    log_blocking("info", "retry #%s: %s", number, function_id)
                    sleep_blocking(sleep_between_retries)

        return cast(Tfun, wrapper)

    return decorator
