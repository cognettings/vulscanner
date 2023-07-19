import asyncio
from asyncio import (
    sleep,
)
from collections.abc import (
    Callable,
)
import contextlib
import functools
import time
from typing import (
    Any,
    cast,
    TypeVar,
)

# pylint: disable=invalid-name
TVar = TypeVar("TVar")
# pylint: disable=invalid-name
TFun = TypeVar("TFun", bound=Callable[..., Any])


def retry_on_exceptions(
    *,
    exceptions: tuple[type[Exception], ...],
    max_attempts: int = 5,
    sleep_seconds: float = 0,
) -> Callable[[TVar], TVar]:
    def decorator(func: TVar) -> TVar:
        _func = cast(Callable[..., Any], func)
        if asyncio.iscoroutinefunction(_func):

            @functools.wraps(_func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(max_attempts - 1):
                    with contextlib.suppress(*exceptions):
                        return await _func(*args, **kwargs)

                    await sleep(sleep_seconds)

                return await _func(*args, **kwargs)

        else:

            @functools.wraps(_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(max_attempts - 1):
                    with contextlib.suppress(*exceptions):
                        return _func(*args, **kwargs)

                    time.sleep(sleep_seconds)

                return _func(*args, **kwargs)

        return cast(TVar, wrapper)

    return decorator
