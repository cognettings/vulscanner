import asyncio
import builtins
from collections.abc import (
    Callable,
    Collection,
)
from opentelemetry.instrumentation.instrumentor import (  # type: ignore
    BaseInstrumentor,
)
from opentelemetry.instrumentation.utils import (
    unwrap,
)
from opentelemetry.trace import (
    get_tracer,
)
import os
import re
from telemetry.utils import (
    is_root_span,
)
import time
from types import (
    ModuleType,
)
from typing import (
    Any,
)
from wrapt import (
    wrap_function_wrapper,
)

SYNC_FUNCTIONS: list[tuple[ModuleType, str]] = [
    # CPU-bound
    (re, "search"),
    (re, "match"),
    (re, "fullmatch"),
    (re, "findall"),
    (re, "finditer"),
    (time, "sleep"),
    # I/O-bound
    (os, "link"),
    (os, "mkdir"),
    (os, "remove"),
    (os, "rename"),
    (os, "rmdir"),
    (os, "symlink"),
]


class StandardLibraryInstrumentor(BaseInstrumentor):
    """
    OpenTelemetry instrumentor for the python standard library

    Pending contribution to upstream
    https://github.com/open-telemetry/opentelemetry-python-contrib/
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return []

    def _instrument(self, **kwargs: Any) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._tracer = get_tracer(__name__)

        for module, function in SYNC_FUNCTIONS:
            wrap_function_wrapper(
                module,
                function,
                self._patched_basic_function,
            )

        wrap_function_wrapper(
            asyncio,
            "create_subprocess_exec",
            self._patched_asyncio_create_subprocess_exec,
        )
        wrap_function_wrapper(
            builtins,
            "open",
            self._patched_builtins_open,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        for module, function in SYNC_FUNCTIONS:
            unwrap(module, function)

        unwrap(asyncio, "create_subprocess_exec")
        unwrap(builtins, "open")

    def _patched_basic_function(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        if is_root_span():
            return original_func(*args, **kwargs)

        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name):
            return original_func(*args, **kwargs)

    def _patched_builtins_open(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        if is_root_span():
            return original_func(*args, **kwargs)

        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name):
            file_instance = original_func(*args, **kwargs)
            for method in ["close", "read", "seek", "write"]:
                wrap_function_wrapper(
                    file_instance,
                    method,
                    self._patched_basic_function,
                )
            return file_instance

    async def _patched_basic_coroutine(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        if is_root_span():
            return await original_func(*args, **kwargs)

        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name):
            return await original_func(*args, **kwargs)

    async def _patched_asyncio_create_subprocess_exec(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name):
            subprocess: asyncio.subprocess.Process = await original_func(
                *args, **kwargs
            )
            wrap_function_wrapper(
                subprocess,
                "communicate",
                self._patched_basic_coroutine,
            )
            return subprocess
